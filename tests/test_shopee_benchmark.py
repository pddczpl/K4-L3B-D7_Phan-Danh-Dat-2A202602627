"""Offline checks for evidence scoring, provenance, filtering, and API boundaries."""

import json
import math
from types import SimpleNamespace

import pytest

from scripts.run_shopee_benchmark import (
    DataValidationError,
    EMBEDDING_DIMENSIONS,
    GeminiService,
    RemoteCallError,
    answer_bearing,
    build_chunks,
    load_documents,
    load_queries,
    run_benchmark,
)


@pytest.fixture
def corpus(tmp_path):
    queries = []
    for index in range(5):
        metadata = {
            "doc_id": f"doc{index}", "source_url": f"https://example.org/order/{index}",
            "retrieved_at": "2026-09-20", "document_version": "not-stated",
            "audience": "seller" if index == 4 else "buyer", "language": "vi",
        }
        header = "\n".join(f"{key}: {json.dumps(value)}" for key, value in metadata.items())
        (tmp_path / f"doc{index}.md").write_text(
            f"---\n{header}\n---\n# Order {index}\n\n## Procedure\nAnswer marker {index}. Common phrase.\n",
            encoding="utf-8",
        )
        queries.append({
            "id": f"Q{index}", "question": f"Question {index}?", "gold_answer": f"Answer marker {index}",
            "metadata_filter": {"audience": "seller", "language": "vi"} if index == 4 else None,
            "evidence": [{"doc_id": f"doc{index}", "required_phrases": [f"Answer marker {index}", "Common phrase"]}],
        })
    (tmp_path / "benchmark_queries.json").write_text(json.dumps({"queries": queries}), encoding="utf-8")
    return tmp_path


def test_metadata_is_preserved_but_not_embedded(corpus):
    documents = load_documents(corpus)
    chunks, _ = build_chunks(documents)
    assert all("source_url:" not in doc.content for doc in documents)
    for strategy, items in chunks.items():
        for item in items:
            assert item.metadata["source_url"].startswith("https://example.org/")
            assert item.metadata["document_version"] == "not-stated"
            assert item.metadata["strategy"] == strategy
            assert isinstance(item.metadata["chunk_index"], int)
    assert all("## Procedure" in item.content for item in chunks["heading"])


def test_evidence_requires_all_phrases_in_same_chunk_and_doc():
    evidence = [{"doc_id": "a", "required_phrases": ["Chờ phản hồi", "Đã hủy"]}]
    assert answer_bearing({"content": "CHỜ PHẢN HỒI\n Đã   hủy", "metadata": {"doc_id": "a"}}, evidence)
    assert not answer_bearing({"content": "Chờ phản hồi", "metadata": {"doc_id": "a"}}, evidence)
    assert not answer_bearing({"content": "Đã hủy", "metadata": {"doc_id": "a"}}, evidence)
    assert not answer_bearing({"content": "Chờ phản hồi. Đã hủy", "metadata": {"doc_id": "b"}}, evidence)


def test_validation_rejects_wrong_query_count_and_invented_evidence(corpus):
    path = corpus / "benchmark_queries.json"
    payload = json.loads(path.read_text())
    payload["queries"][0]["evidence"][0]["required_phrases"] = ["Not present in source"]
    path.write_text(json.dumps(payload))
    with pytest.raises(DataValidationError, match="absent"):
        load_queries(path, load_documents(corpus))
    payload["queries"].pop()
    path.write_text(json.dumps(payload))
    with pytest.raises(DataValidationError, match="exactly five"):
        load_queries(path, load_documents(corpus))


def test_rag_uses_filtered_context_original_query_embeddings_and_only_15_answers(corpus):
    class FakeService:
        def __init__(self):
            self.batches = []
            self.prompts = []
            self.counts = {"embedding_requests": 0, "generation_requests": 0}

        def embed_many(self, texts, task_type):
            self.batches.append((task_type, texts))
            self.counts["embedding_requests"] += 1
            return {text: [1.0, 0.0] for text in texts}

        def generate(self, prompt):
            self.prompts.append(prompt)
            self.counts["generation_requests"] += 1
            return "Captured-context answer [1]"

    service = FakeService()
    result = run_benchmark(corpus, "gemini", "gemini", "fake-test-model", corpus / ".cache", service)
    assert [task for task, _ in service.batches] == ["RETRIEVAL_DOCUMENT", "RETRIEVAL_QUERY"]
    assert service.batches[1][1] == [f"Question {index}?" for index in range(5)]
    assert len(service.prompts) == 15
    for index, strategy in enumerate(("heading", "fixed_size", "recursive")):
        query = result["results"][strategy]["queries"][-1]
        assert query["hit_at_3"] is True
        assert query["without_filter"]["hit_at_3"] is False
        assert "người bán" in query["generation_question"]
        assert query["question"] == "Question 4?"
        assert len(query["top3"]) == 1
        assert query["top3"][0]["metadata"]["audience"] == "seller"
        prompt = service.prompts[index * 5 + 4]
        assert "source=https://example.org/order/4" in prompt
        assert "source=https://example.org/order/0" not in prompt
        assert query["generation_question"] in prompt
        assert query["top3"][0]["content"] in prompt


def test_mock_output_is_explicitly_an_offline_non_llm_smoke(corpus):
    result = run_benchmark(corpus, "mock", "extractive", "unused", corpus / ".cache")
    assert result["llm"]["is_language_model"] is False
    assert result["methodology"]["quality_warning"]
    assert result["api_usage_this_run"]["generation_requests"] == 0
    assert all("không gọi LLM" in query["answer"] for strategy in result["results"].values() for query in strategy["queries"])


def test_embedding_cache_is_separated_by_task_and_vectors_are_normalized(tmp_path):
    calls = []

    def embed_content(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(embeddings=[SimpleNamespace(values=[3.0, 4.0] + [0.0] * (EMBEDDING_DIMENSIONS - 2))
                                           for _ in kwargs["contents"]])

    service = GeminiService.__new__(GeminiService)
    service.cache_dir = tmp_path
    service.counts = {"embedding_requests": 0, "embedding_cache_hits": 0}
    service.types = SimpleNamespace(EmbedContentConfig=lambda **kwargs: SimpleNamespace(**kwargs))
    service.client = SimpleNamespace(models=SimpleNamespace(embed_content=embed_content))
    first = service.embed_many(["same text", "same text"], "RETRIEVAL_DOCUMENT")
    second = service.embed_many(["same text"], "RETRIEVAL_DOCUMENT")
    service.embed_many(["same text"], "RETRIEVAL_QUERY")
    assert len(calls) == 2
    assert first == second
    assert math.isclose(sum(value * value for value in first["same text"]), 1.0)
    assert calls[0]["config"].output_dimensionality == 3072
    assert calls[1]["config"].task_type == "RETRIEVAL_QUERY"
    assert len(list((tmp_path / "embeddings").glob("*.json"))) == 2


def test_api_errors_never_expose_response_or_key():
    class ClientFailure(Exception):
        code = 429

    def fail():
        raise ClientFailure("secret API key and private HTTP request")

    with pytest.raises(RemoteCallError) as captured:
        GeminiService.remote_call(fail)
    assert str(captured.value) == "Gemini API failed: ClientFailure; code=429"
    assert "secret" not in str(captured.value)


def test_generation_cache_preserves_model_settings_and_disables_function_calls(tmp_path):
    calls = []

    def generate_content(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(text="Trả lời từ nguồn [1].")

    service = GeminiService.__new__(GeminiService)
    service.cache_dir = tmp_path
    service.llm_model = "gemini-3.1-flash-lite"
    service.counts = {"generation_requests": 0, "answer_cache_hits": 0}
    service.types = SimpleNamespace(GenerateContentConfig=lambda **kwargs: SimpleNamespace(**kwargs))
    service.client = SimpleNamespace(models=SimpleNamespace(generate_content=generate_content))
    assert service.generate("Context and question") == service.generate("Context and question")
    assert len(calls) == 1
    assert calls[0]["model"] == "gemini-3.1-flash-lite"
    assert calls[0]["config"].automatic_function_calling == {"disable": True}
    assert calls[0]["config"].max_output_tokens == 2048
    assert calls[0]["config"].temperature == 0
    assert service.counts == {"generation_requests": 1, "answer_cache_hits": 1}
    assert b"\r\n" not in next((tmp_path / "answers").glob("*.json")).read_bytes()
