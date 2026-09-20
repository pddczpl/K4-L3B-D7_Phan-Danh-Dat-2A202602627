"""Check section boundaries, retained context, and bounded fallback chunks."""

import pytest

from src import HeadingChunker


@pytest.mark.parametrize("text", ["", " \n\t\r\n "])
def test_blank_markdown_has_no_chunks(text):
    assert HeadingChunker().chunk(text) == []


def test_child_section_keeps_parents_but_not_sibling_heading():
    text = (
        "# Shopee\n"
        "## Delivery\n"
        "### Tracking\nFind the delivery status.\n"
        "### Late order\nContact the carrier.\n"
        "## Returns\nAttach a photograph."
    )
    assert HeadingChunker().chunk(text) == [
        "# Shopee\n## Delivery\n### Tracking\n\nFind the delivery status.",
        "# Shopee\n## Delivery\n### Late order\n\nContact the carrier.",
        "# Shopee\n## Returns\n\nAttach a photograph.",
    ]


def test_long_section_repeats_context_and_retains_body_in_order():
    heading = "# Shopee\n## Order status"
    body = "Track shipment. Check carrier. " * 20
    chunks = HeadingChunker(chunk_size=100).chunk(heading + "\n" + body)
    prefix = heading + "\n\n"
    assert len(chunks) > 1
    assert all(chunk.startswith(prefix) and len(chunk) <= 100 for chunk in chunks)
    reconstructed_words = " ".join(chunk[len(prefix):] for chunk in chunks).split()
    assert reconstructed_words == body.split()


def test_preamble_and_empty_sections_are_retained():
    text = "Introduction.\n# Empty\n# Orders\nOrder details.\n## Empty child"
    assert HeadingChunker().chunk(text) == [
        "Introduction.",
        "# Empty",
        "# Orders\n\nOrder details.",
        "# Orders\n## Empty child",
    ]


def test_hash_lines_inside_fenced_code_are_not_section_boundaries():
    text = "# Guide\n```python\n# Code comment\nprint('order')\n```\nMore instructions."
    assert HeadingChunker().chunk(text) == [
        "# Guide\n\n```python\n# Code comment\nprint('order')\n```\nMore instructions."
    ]


def test_oversized_heading_falls_back_without_losing_content():
    text = "# " + "heading" * 12 + "\n" + "body" * 30
    chunks = HeadingChunker(chunk_size=20).chunk(text)
    assert all(0 < len(chunk) <= 20 for chunk in chunks)
    assert "".join("".join(chunks).split()) == "".join(text.split())


def test_long_heading_does_not_repeat_for_every_few_body_characters():
    text = "# " + "h" * 32 + "\n" + "b" * 100
    chunks = HeadingChunker(chunk_size=40).chunk(text)
    assert len(chunks) <= 5
    assert all(0 < len(chunk) <= 40 for chunk in chunks)
    assert "".join("".join(chunks).split()) == "".join(text.split())


def test_document_without_headings_uses_recursive_body_splitting():
    text = "First paragraph.\n\n" + "x" * 83
    chunks = HeadingChunker(chunk_size=30).chunk(text)
    assert all(0 < len(chunk) <= 30 for chunk in chunks)
    assert "".join("".join(chunks).split()) == "".join(text.split())


@pytest.mark.parametrize("chunk_size", [0, -1])
def test_nonpositive_chunk_size_is_rejected(chunk_size):
    with pytest.raises(ValueError, match="chunk_size"):
        HeadingChunker(chunk_size=chunk_size)
