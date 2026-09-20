"""Regression tests for data loss, filtering, deletion, and grounded RAG.

All embeddings and LLM responses are deterministic; no API key is required.
The original 42 lab tests remain unchanged in test_solution.py.
"""

import importlib
import os
from unittest.mock import Mock

import pytest


solution = importlib.import_module(os.getenv("LAB_SOLUTION_PACKAGE", "src"))


@pytest.mark.parametrize("text", ["", " \t\n  "])
def test_sentence_chunker_ignores_empty_input(text):
    assert solution.SentenceChunker().chunk(text) == []


def test_sentence_chunker_preserves_punctuation_and_final_sentence():
    text = "  Một.  Hai!\nBa?\tBốn. \nNăm  "
    assert solution.SentenceChunker(max_sentences_per_chunk=2).chunk(text) == [
        "Một. Hai!",
        "Ba? Bốn.",
        "Năm",
    ]


@pytest.mark.parametrize("separators", [None, [], ["\n\n"], [" ", ""]])
def test_recursive_chunker_preserves_content_and_enforces_size(separators):
    text = "Mục 1. Giữ dấu câu!\n\nMục 2\n" + "x" * 31 + "  Kết thúc."
    chunks = solution.RecursiveChunker(separators=separators, chunk_size=13).chunk(text)
    assert "".join(chunks) == text
    assert all(0 < len(chunk) <= 13 for chunk in chunks)


def test_recursive_chunker_merges_adjacent_short_lines():
    text = "a\n" * 20
    chunks = solution.RecursiveChunker(chunk_size=10).chunk(text)
    assert "".join(chunks) == text
    assert len(chunks) <= 5  # One chunk per short line would lose useful context.


def test_empty_comparison_has_no_chunks_or_division_by_zero():
    comparison = solution.ChunkingStrategyComparator().compare("", chunk_size=20)
    assert set(comparison) == {"fixed_size", "by_sentences", "recursive"}
    for stats in comparison.values():
        assert stats == {"count": 0, "avg_length": 0.0, "chunks": []}


def test_cosine_is_scale_invariant_and_accepts_empty_vectors():
    assert solution.compute_similarity([2.0, 4.0], [10.0, 20.0]) == pytest.approx(1.0)
    assert solution.compute_similarity([], []) == 0.0


def test_cosine_rejects_different_dimensions_instead_of_truncating():
    with pytest.raises(ValueError):
        solution.compute_similarity([1.0, 0.0], [1.0])


def make_store():
    return solution.EmbeddingStore("edge_cases", embedding_fn=lambda text: [1.0, 0.0])


def test_store_copies_metadata_on_ingest_and_on_search():
    store = make_store()
    metadata = {"audience": "buyer", "doc_id": "policy"}
    store.add_documents([solution.Document("policy#0", "Chính sách", metadata)])
    metadata["audience"] = "seller"
    first_result = store.search("query")[0]
    assert first_result["metadata"]["audience"] == "buyer"
    assert first_result["metadata"]["doc_id"] == "policy"
    assert "embedding" not in first_result
    first_result["metadata"]["audience"] = "seller"
    assert store.search("query")[0]["metadata"]["audience"] == "buyer"


def test_store_defaults_doc_id_without_mutating_document_metadata():
    store = make_store()
    doc = solution.Document("original", "Nội dung")
    store.add_documents([doc])
    assert store.search("query")[0]["metadata"]["doc_id"] == "original"
    assert doc.metadata == {}


def test_duplicate_ids_append_and_delete_removes_every_matching_record():
    store = make_store()
    store.add_documents([solution.Document("same", "First")])
    store.add_documents([solution.Document("same", "Second")])
    assert store.get_collection_size() == 2
    assert {result["content"] for result in store.search("query")} == {"First", "Second"}
    assert store.delete_document("same") is True
    assert store.get_collection_size() == 0
    assert store.delete_document("same") is False


def test_delete_uses_original_doc_id_and_keeps_other_documents():
    store = make_store()
    store.add_documents([
        solution.Document("policy#0", "First", {"doc_id": "policy"}),
        solution.Document("policy#1", "Second", {"doc_id": "policy"}),
        solution.Document("other#0", "Keep", {"doc_id": "other"}),
    ])
    assert store.delete_document("policy") is True
    assert store.get_collection_size() == 1
    assert [result["content"] for result in store.search("query")] == ["Keep"]


def test_filter_all_fields_before_ranking_and_top_k():
    vectors = {
        "query": [1.0, 0.0],
        "seller": [1.0, 0.0],
        "buyer_en": [0.8, 0.6],
        "buyer_vi": [0.6, 0.8],
        "missing_metadata": [1.0, 0.0],
    }
    store = solution.EmbeddingStore("filter_edges", embedding_fn=vectors.__getitem__)
    store.add_documents([
        solution.Document("s", "seller", {"audience": "seller", "language": "vi"}),
        solution.Document("be", "buyer_en", {"audience": "buyer", "language": "en"}),
        solution.Document("bv", "buyer_vi", {"audience": "buyer", "language": "vi"}),
        solution.Document("m", "missing_metadata"),
    ])
    results = store.search_with_filter(
        "query", top_k=1, metadata_filter={"audience": "buyer", "language": "vi"}
    )
    assert [result["content"] for result in results] == ["buyer_vi"]
    assert results[0]["score"] == pytest.approx(0.6)
    assert store.search_with_filter("query", metadata_filter={"language": "fr"}) == []


@pytest.mark.parametrize("top_k", [0, -1])
def test_nonpositive_top_k_returns_no_results(top_k):
    store = make_store()
    store.add_documents([solution.Document("d", "Content", {"audience": "buyer"})])
    assert store.search("query", top_k=top_k) == []
    assert store.search_with_filter(
        "query", top_k=top_k, metadata_filter={"audience": "buyer"}
    ) == []


def test_agent_passes_retrieved_context_source_and_question_to_llm():
    store = Mock()
    store.search.return_value = [{
        "content": "Người mua được đổi trả trong 7 ngày.",
        "metadata": {"source_url": "https://example.org/policy", "doc_id": "policy"},
        "score": 0.8,
    }]
    llm = Mock(return_value="Trong 7 ngày [1].")
    agent = solution.KnowledgeBaseAgent(store=store, llm_fn=llm)
    question = "Thời hạn đổi trả là bao lâu?"
    assert agent.answer(question, top_k=1) == "Trong 7 ngày [1]."
    store.search.assert_called_once_with(question, top_k=1)
    llm.assert_called_once()
    prompt = llm.call_args.args[0]
    assert "Question:" in prompt and question in prompt
    assert "Context:" in prompt and store.search.return_value[0]["content"] in prompt
    assert "[1]" in prompt and "source=" in prompt
    assert "https://example.org/policy" in prompt


def test_agent_with_empty_store_does_not_call_llm():
    llm = Mock(return_value="This answer must never be generated.")
    answer = solution.KnowledgeBaseAgent(store=make_store(), llm_fn=llm).answer("Question?")
    assert isinstance(answer, str) and answer.strip()
    llm.assert_not_called()
