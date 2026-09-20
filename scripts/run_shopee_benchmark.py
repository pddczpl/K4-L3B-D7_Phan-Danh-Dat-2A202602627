"""Reproduce the Shopee-orders retrieval experiment without fabricating grading.

Offline smoke: python -m scripts.run_shopee_benchmark --provider mock
Real RAG: python -m scripts.run_shopee_benchmark --provider gemini --llm gemini

Real runs require GEMINI_API_KEY or GOOGLE_API_KEY in the environment/.env.
No remote failure falls back to mock embeddings or extractive output.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Any

from dotenv import load_dotenv

from src import Document, EmbeddingStore, FixedSizeChunker, KnowledgeBaseAgent, MockEmbedder, RecursiveChunker

ROOT = Path(__file__).resolve().parents[1]
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 3072
STRATEGY_CONFIGS = {
    "heading": {"chunk_size": 500},
    "fixed_size": {"chunk_size": 350, "overlap": 50},
    "recursive": {"chunk_size": 500},
}


class DataValidationError(ValueError):
    """A safe, locally constructed validation message."""


class RemoteCallError(RuntimeError):
    """An API error with request details and credentials removed."""


def digest(value: Any) -> str:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def normalize(vector: list[float], dimensions: int) -> list[float]:
    values = [float(value) for value in vector]
    if len(values) != dimensions or any(not math.isfinite(value) for value in values):
        raise ValueError("Embedding has an invalid dimension or non-finite values")
    length = math.sqrt(sum(value * value for value in values))
    if not length:
        raise ValueError("Embedding must have nonzero length")
    return [value / length for value in values]


def load_documents(data_dir: Path) -> list[Document]:
    """Parse flat, JSON-quoted Markdown frontmatter; embed only its body."""
    documents = []
    for path in sorted(data_dir.glob("*.md")):
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        if not lines or lines[0] != "---":
            raise DataValidationError(f"Missing frontmatter: {path.name}")
        try:
            end = lines.index("---", 1)
        except ValueError:
            raise DataValidationError(f"Unclosed frontmatter: {path.name}") from None
        metadata = {}
        for line in lines[1:end]:
            if not line.strip():
                continue
            key, separator, value = line.partition(":")
            if not separator or not key.strip() or key.strip() in metadata:
                raise DataValidationError(f"Invalid or duplicate metadata field: {path.name}")
            try:
                decoded = json.loads(value.strip())
            except json.JSONDecodeError:
                raise DataValidationError(f"Metadata values must be JSON-quoted strings: {path.name}") from None
            if not isinstance(decoded, str) or not decoded.strip():
                raise DataValidationError(f"Metadata values must be nonempty strings: {path.name}")
            metadata[key.strip()] = decoded
        for field in ("source_url", "retrieved_at", "document_version"):
            if field not in metadata:
                raise DataValidationError(f"Missing {field}: {path.name}")
        body = "\n".join(lines[end + 1:]).strip()
        if not body:
            raise DataValidationError(f"Empty document body: {path.name}")
        metadata.setdefault("doc_id", path.stem)
        metadata["source_file"] = path.name
        documents.append(Document(metadata["doc_id"], body, metadata))
    if not 5 <= len(documents) <= 10:
        raise DataValidationError("The corpus must contain 5–10 Markdown documents")
    if len({doc.id for doc in documents}) != len(documents):
        raise DataValidationError("Corpus doc_id values must be unique")
    return documents


def normalized_text(text: str) -> str:
    return " ".join(text.casefold().split())


def load_queries(path: Path, documents: list[Document]) -> list[dict]:
    try:
        queries = json.loads(path.read_text(encoding="utf-8-sig"))["queries"]
    except (KeyError, TypeError, json.JSONDecodeError):
        raise DataValidationError("Invalid benchmark_queries.json schema") from None
    if not isinstance(queries, list) or len(queries) != 5:
        raise DataValidationError("The benchmark must contain exactly five queries")
    by_id = {doc.id: doc for doc in documents}
    ids = []
    for query in queries:
        if not isinstance(query, dict) or any(
            not isinstance(query.get(field), str) or not query[field].strip()
            for field in ("id", "question", "gold_answer")
        ):
            raise DataValidationError("Every query needs a nonempty id, question, and gold_answer")
        ids.append(query["id"])
        filters = query.get("metadata_filter")
        if filters is not None and not isinstance(filters, dict):
            raise DataValidationError("metadata_filter must be an object or null")
        evidence = query.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise DataValidationError("Every query needs at least one evidence entry")
        for item in evidence:
            if not isinstance(item, dict) or item.get("doc_id") not in by_id:
                raise DataValidationError("Evidence must refer to a corpus doc_id")
            phrases = item.get("required_phrases")
            if not isinstance(phrases, list) or not phrases or any(
                not isinstance(phrase, str) or not phrase.strip() for phrase in phrases
            ):
                raise DataValidationError("Evidence required_phrases must be nonempty strings")
            if not all(normalized_text(phrase) in normalized_text(by_id[item["doc_id"]].content) for phrase in phrases):
                raise DataValidationError("An evidence phrase is absent from its source document")
        if filters and not any(all(doc.metadata.get(key) == value for key, value in filters.items()) for doc in documents):
            raise DataValidationError("A metadata filter excludes the entire corpus")
    if len(set(ids)) != len(ids):
        raise DataValidationError("Query IDs must be unique")
    if not any(query.get("metadata_filter") for query in queries):
        raise DataValidationError("At least one query must exercise metadata filtering")
    return queries


def answer_bearing(result: dict, evidence: list[dict]) -> bool:
    content = normalized_text(result["content"])
    return any(
        result["metadata"]["doc_id"] == item["doc_id"]
        and all(normalized_text(phrase) in content for phrase in item["required_phrases"])
        for item in evidence
    )


def annotate_results(results: list[dict], evidence: list[dict]) -> list[dict]:
    return [
        {**result, "rank": rank, "source_url": result["metadata"]["source_url"],
         "answer_bearing": answer_bearing(result, evidence)}
        for rank, result in enumerate(results, start=1)
    ]


class GeminiService:
    """Explicit Gemini calls with bounded timeouts and content-addressed caches."""

    def __init__(self, cache_dir: Path, llm_model: str) -> None:
        from google import genai
        from google.genai import types

        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise DataValidationError("GEMINI_API_KEY or GOOGLE_API_KEY is required")
        self.types = types
        self.client = genai.Client(api_key=api_key, http_options=types.HttpOptions(
            timeout=45000, retry_options=types.HttpRetryOptions(attempts=1),
        ))
        self.cache_dir = cache_dir
        self.llm_model = llm_model
        self.counts = {"embedding_requests": 0, "generation_requests": 0,
                       "embedding_cache_hits": 0, "answer_cache_hits": 0}

    @staticmethod
    def remote_call(function, **kwargs):
        try:
            return function(**kwargs)
        except Exception as exc:
            code = getattr(exc, "code", None)
            code = code if isinstance(code, int) else "unavailable"
            error_type = re.sub(r"[^A-Za-z0-9_]", "", type(exc).__name__)
            raise RemoteCallError(f"Gemini API failed: {error_type}; code={code}") from None

    def embed_many(self, texts: list[str], task_type: str) -> dict[str, list[float]]:
        vectors = {}
        pending = []
        for text in dict.fromkeys(texts):
            key = digest([EMBEDDING_MODEL, task_type, EMBEDDING_DIMENSIONS, text])
            path = self.cache_dir / "embeddings" / f"{key}.json"
            if path.exists():
                value = json.loads(path.read_text(encoding="utf-8"))
                vectors[text] = normalize(value["vector"], EMBEDDING_DIMENSIONS)
                self.counts["embedding_cache_hits"] += 1
            else:
                pending.append((text, path))
        for start in range(0, len(pending), 64):
            batch = pending[start:start + 64]
            response = self.remote_call(
                self.client.models.embed_content, model=EMBEDDING_MODEL,
                contents=[text for text, _ in batch],
                config=self.types.EmbedContentConfig(
                    task_type=task_type, output_dimensionality=EMBEDDING_DIMENSIONS,
                ),
            )
            self.counts["embedding_requests"] += 1
            if not response.embeddings or len(response.embeddings) != len(batch):
                raise RemoteCallError("Gemini returned an unexpected number of embeddings")
            for (text, path), embedding in zip(batch, response.embeddings):
                vector = normalize(embedding.values, EMBEDDING_DIMENSIONS)
                vectors[text] = vector
                write_json(path, {"model": EMBEDDING_MODEL, "task_type": task_type,
                                  "dimensions": EMBEDDING_DIMENSIONS, "vector": vector})
        return vectors

    def generate(self, prompt: str) -> str:
        settings = {"temperature": 0, "max_output_tokens": 2048,
                    "automatic_function_calling": {"disable": True}}
        if self.llm_model.removeprefix("models/") == "gemini-2.5-flash":
            settings.update(max_output_tokens=768, thinking_config={"thinking_budget": 0})
        path = self.cache_dir / "answers" / f"{digest([self.llm_model, settings, prompt])}.json"
        if path.exists():
            cached = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(cached.get("answer"), str) or not cached["answer"].strip():
                raise ValueError("Invalid cached answer")
            self.counts["answer_cache_hits"] += 1
            return cached["answer"]
        response = self.remote_call(
            self.client.models.generate_content, model=self.llm_model, contents=prompt,
            config=self.types.GenerateContentConfig(**settings),
        )
        self.counts["generation_requests"] += 1
        answer = response.text
        if not isinstance(answer, str) or not answer.strip():
            raise RemoteCallError("Gemini returned no answer text")
        write_json(path, {"model": self.llm_model, "settings": settings, "answer": answer})
        return answer

    def close(self) -> None:
        self.client.close()


class PreparedEmbeddings:
    """Keep document/query task vectors separate even for identical input text."""

    def __init__(self, document_vectors: dict, query_vectors: dict) -> None:
        self.document_vectors = document_vectors
        self.query_vectors = query_vectors
        self.ingesting = True

    def __call__(self, text: str) -> list[float]:
        return (self.document_vectors if self.ingesting else self.query_vectors)[text]


class RetrievedContext:
    """Pass already filtered results through the lab's KnowledgeBaseAgent."""

    def __init__(self, results: list[dict]) -> None:
        self.results = results

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        return deepcopy(self.results[:top_k])


def extractive_answer(results: list[dict]) -> str:
    return "Chế độ trích xuất nguyên văn; không gọi LLM. Các đoạn truy xuất:\n\n" + "\n\n".join(
        f"[{index}] {result['content']}" for index, result in enumerate(results, 1)
    )


def generation_question(query: dict) -> str:
    """Apply the requested audience to generation without altering retrieval."""
    filters = query.get("metadata_filter")
    if not filters:
        return query["question"]
    audience = {"buyer": "người mua", "seller": "người bán"}.get(filters.get("audience"))
    scope = f"Vai trò của người hỏi: {audience}. " if audience else ""
    return query["question"] + "\n" + scope + "Phạm vi tài liệu: " + json.dumps(filters, ensure_ascii=False, sort_keys=True)


def build_chunks(documents: list[Document]) -> tuple[dict[str, list[Document]], dict]:
    from src import HeadingChunker

    chunkers = {"heading": HeadingChunker(**STRATEGY_CONFIGS["heading"]),
                "fixed_size": FixedSizeChunker(**STRATEGY_CONFIGS["fixed_size"]),
                "recursive": RecursiveChunker(**STRATEGY_CONFIGS["recursive"])}
    chunks = {name: [] for name in chunkers}
    comparisons = {}
    for doc_index, doc in enumerate(documents):
        stats = {}
        for name, chunker in chunkers.items():
            parts = chunker.chunk(doc.content)
            stats[name] = {"count": len(parts), "avg_length": sum(map(len, parts)) / len(parts) if parts else 0,
                           "max_length": max(map(len, parts), default=0)}
            for index, content in enumerate(parts):
                metadata = {**doc.metadata, "doc_id": doc.id, "chunk_index": index, "strategy": name}
                chunks[name].append(Document(f"{doc.id}:{name}:{index}", content, metadata))
        if doc_index < 3:
            comparisons[doc.id] = {"source_url": doc.metadata["source_url"],
                                   "characters": len(doc.content), "strategies": stats}
    return chunks, comparisons


def run_benchmark(data_dir: Path, provider: str, llm: str, llm_model: str,
                  cache_dir: Path, service=None) -> dict:
    documents = load_documents(data_dir)
    queries = load_queries(data_dir / "benchmark_queries.json", documents)
    chunks, comparisons = build_chunks(documents)
    document_texts = list(dict.fromkeys(doc.content for items in chunks.values() for doc in items))
    query_texts = list(dict.fromkeys(query["question"] for query in queries))
    owns_service = service is None and (provider == "gemini" or llm == "gemini")
    if owns_service:
        service = GeminiService(cache_dir, llm_model)
    try:
        if provider == "gemini":
            document_vectors = service.embed_many(document_texts, "RETRIEVAL_DOCUMENT")
            query_vectors = service.embed_many(query_texts, "RETRIEVAL_QUERY")
            backend = EMBEDDING_MODEL
        else:
            mock = MockEmbedder()
            document_vectors = {text: mock(text) for text in document_texts}
            query_vectors = {text: mock(text) for text in query_texts}
            backend = "MockEmbedder (offline smoke only; no semantic quality claim)"
        results = {}
        for strategy, items in chunks.items():
            lookup = PreparedEmbeddings(document_vectors, query_vectors)
            store = EmbeddingStore(f"shopee-{strategy}", embedding_fn=lookup)
            store.add_documents(items)
            lookup.ingesting = False
            query_results = []
            for query in queries:
                retrieved = store.search_with_filter(query["question"], 3, query.get("metadata_filter"))
                top3 = annotate_results(retrieved, query["evidence"])
                llm_fn = service.generate if llm == "gemini" else lambda prompt, rows=top3: extractive_answer(rows)
                effective_question = generation_question(query)
                answer = KnowledgeBaseAgent(RetrievedContext(top3), llm_fn).answer(effective_question, top_k=3)
                item = {**query, "top3": top3, "hit_at_3": any(row["answer_bearing"] for row in top3),
                        "generation_question": effective_question, "answer": answer, "answer_mode": llm}
                if query.get("metadata_filter"):
                    unfiltered = annotate_results(store.search(query["question"], 3), query["evidence"])
                    item["without_filter"] = {"top3": unfiltered,
                                               "hit_at_3": any(row["answer_bearing"] for row in unfiltered)}
                query_results.append(item)
            hits = sum(item["hit_at_3"] for item in query_results)
            results[strategy] = {"chunk_count": store.get_collection_size(),
                                 "document_chunk_counts": {doc.id: sum(chunk.metadata["doc_id"] == doc.id for chunk in items) for doc in documents},
                                 "hit_at_3": {"hits": hits, "queries": len(queries), "rate": hits / len(queries)},
                                 "queries": query_results}
        return {
            "schema_version": 1,
            "student": {"name": "Phan Danh Đạt", "student_id": "2A202602627", "group_size": 3},
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "provider": provider, "backend": backend,
            "embedding_dimensions": len(next(iter(document_vectors.values()))),
            "embedding_tasks": ["RETRIEVAL_DOCUMENT", "RETRIEVAL_QUERY"] if provider == "gemini" else ["mock"],
            "similarity": "dot product of L2-normalized vectors (cosine similarity)",
            "llm": {"provider": llm, "model": llm_model if llm == "gemini" else None,
                    "is_language_model": llm == "gemini"},
            "methodology": {
                "hit_at_3": "At least one top-3 chunk has the evidence doc_id and ALL required phrases of one evidence entry in that SAME chunk; casefold and whitespace normalization.",
                "filters": "Exact AND metadata filtering before ranking; filtered questions also retrieve without a filter.",
                "answer_grading": "No automatic claim of answer correctness; gold answers are supplied for human review.",
                "scope": "One student's three configurations, not results from three group members.",
                "quality_warning": "Mock embeddings are deterministic test vectors, not evidence of semantic retrieval quality." if provider == "mock" else None,
            },
            "corpus": {"documents": [{"id": doc.id, "characters": len(doc.content), "body_sha256": digest(doc.content),
                                       "metadata": doc.metadata} for doc in documents],
                       "queries_sha256": digest(queries)},
            "strategy_configs": STRATEGY_CONFIGS,
            "chunking_comparison_first_three_documents": comparisons,
            "results": results,
            "api_usage_this_run": dict(service.counts) if service else {"embedding_requests": 0, "generation_requests": 0},
        }
    finally:
        if owns_service:
            service.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("mock", "gemini"), default="mock")
    parser.add_argument("--llm", choices=("extractive", "gemini"), default="extractive")
    parser.add_argument("--llm-model", default="gemini-3.1-flash-lite")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data/shopee-orders")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    load_dotenv(ROOT / ".env", override=False)
    try:
        result = run_benchmark(args.data_dir, args.provider, args.llm, args.llm_model, ROOT / ".cache/shopee-orders")
        destination = args.output or ROOT / "report" / f"shopee_benchmark_{args.provider}_{args.llm}.json"
        write_json(destination, result)
    except (DataValidationError, RemoteCallError) as exc:
        print(str(exc))
        return 1
    except Exception as exc:
        # Never print arbitrary SDK, request, or environment error details.
        print(f"Benchmark failed: {type(exc).__name__}; no fallback results were written.")
        return 1
    print(f"Saved {destination.name}; embeddings={args.provider}; answer_mode={args.llm}")
    for name, item in result["results"].items():
        print(f"{name}: {item['chunk_count']} chunks; hit@3={item['hit_at_3']['hits']}/5")
    if args.provider == "mock":
        print("Offline smoke only: mock scores do not measure semantic retrieval quality.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
