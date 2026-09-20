"""Reproduce individual warm-up, chunking comparison and similarity results.

Run from the repository root:
    python -m scripts.run_individual_checks --provider mock
    python -m scripts.run_individual_checks --provider gemini

These similarity experiments complement the separate Shopee retrieval benchmark.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from src import ChunkingStrategyComparator, FixedSizeChunker, GeminiEmbedder, MockEmbedder, compute_similarity

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("mock", "gemini"), default="mock")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env", override=False)
    predictions = json.loads((ROOT / "report/similarity_predictions.json").read_text(encoding="utf-8"))
    pairs = predictions["pairs"]
    texts = list(dict.fromkeys(text for pair in pairs for text in (pair["a"], pair["b"])))

    if args.provider == "gemini":
        # One small batch; SDK/API failures remain failures, never labelled as real results.
        from google.genai import types

        try:
            embedder = GeminiEmbedder()
            with embedder.client as client:
                response = client.models.embed_content(
                    model=embedder.model_name,
                    contents=texts,
                    config=types.EmbedContentConfig(
                        task_type="SEMANTIC_SIMILARITY",
                        http_options=types.HttpOptions(timeout=30000),
                    ),
                )
            vectors = [list(embedding.values) for embedding in response.embeddings]
            if len(vectors) != len(texts) or any(not vector for vector in vectors):
                raise ValueError("Unexpected number of embeddings or empty vector")
        except Exception as exc:
            # SDK exception text can contain request details: do not print it or credentials.
            print(f"Gemini failed: {type(exc).__name__}; code={getattr(exc, 'code', None)}")
            return 1
        backend = embedder.model_name
        task_type = "SEMANTIC_SIMILARITY"
    else:
        embedder = MockEmbedder()
        vectors = [embedder(text) for text in texts]
        backend = embedder._backend_name
        task_type = "mock (no semantic meaning)"

    vector_by_text = dict(zip(texts, vectors))
    measured_pairs = [
        {**pair, "cosine_similarity": compute_similarity(vector_by_text[pair["a"]], vector_by_text[pair["b"]])}
        for pair in pairs
    ]
    comparisons = {}
    for path in sorted((ROOT / "data/shopee-orders").glob("*.md"))[:3]:
        relative_path = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8").split("---", 2)[2].strip()
        stats = ChunkingStrategyComparator().compare(text, chunk_size=200)
        comparisons[relative_path] = {
            name: {"count": item["count"], "avg_length": item["avg_length"]}
            for name, item in stats.items()
        }

    result = {
        "student": {"name": "Phan Danh Đạt", "student_id": "2A202602627", "group_size": 3},
        "group": "G23",
        "topic": "Đơn hàng Shopee",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "provider": args.provider,
        "backend": backend,
        "task_type": task_type,
        "embedding_dimensions": len(vectors[0]),
        "warm_up": {
            "length": 10000, "chunk_size": 500,
            "overlap_50_count": len(FixedSizeChunker(500, 50).chunk("a" * 10000)),
            "overlap_100_count": len(FixedSizeChunker(500, 100).chunk("a" * 10000)),
        },
        "comparison_settings": {"chunk_size": 200, "fixed_overlap": 20, "sentences_per_chunk": 3},
        "chunking_comparison": comparisons,
        "predicted_highest_pair": predictions["predicted_highest_pair"],
        "predicted_lowest_pair": predictions["predicted_lowest_pair"],
        "actual_highest_pair": max(measured_pairs, key=lambda pair: pair["cosine_similarity"])["id"],
        "actual_lowest_pair": min(measured_pairs, key=lambda pair: pair["cosine_similarity"])["id"],
        "pairs": measured_pairs,
    }
    destination = ROOT / "report" / f"individual_results_{args.provider}.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"Saved report/{destination.name} ({backend}, {len(vectors[0])} dimensions)")
    for pair in measured_pairs:
        print(f"Pair {pair['id']}: cosine={pair['cosine_similarity']:.6f}")
    print(f"Highest: pair {result['actual_highest_pair']}; lowest: pair {result['actual_lowest_pair']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
