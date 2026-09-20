"""Section-aware Markdown chunking for the individual retrieval experiment."""

from __future__ import annotations

import re

from .chunking import RecursiveChunker


class HeadingChunker:
    """Keep Markdown sections separate and repeat their heading hierarchy.

    ATX headings (``#`` through ``######``) define section boundaries. A child
    section carries its parent headings into every chunk, including when a long
    body needs recursive splitting. Fenced code is treated as body text.

    Line endings are normalized to ``\n`` and outer whitespace is stripped from
    each section/body fragment. All non-whitespace body content is retained.
    If headings leave less than one quarter of the limit for body text,
    recursively split the complete section instead. This avoids repeating a
    very long heading for every few characters and keeps all content bounded;
    individual fallback chunks may not include the complete headings.
    """

    _HEADING = re.compile(r"^[ \t]{0,3}(#{1,6})[ \t]+(\S.*)$")
    _FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})(.*)$")

    def __init__(self, chunk_size: int = 500) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text.strip():
            return []

        chunks: list[str] = []
        headings: list[tuple[int, str]] = []
        body: list[str] = []
        fence_character = ""
        fence_length = 0

        for line in text.splitlines():
            fence = self._FENCE.match(line)
            if fence:
                marker, suffix = fence.groups()
                if not fence_character:
                    fence_character, fence_length = marker[0], len(marker)
                elif (
                    marker[0] == fence_character
                    and len(marker) >= fence_length
                    and not suffix.strip()
                ):
                    fence_character = ""
                body.append(line)
                continue

            heading = None if fence_character else self._HEADING.match(line)
            if heading is None:
                body.append(line)
                continue

            level = len(heading.group(1))
            section_body = "\n".join(body).strip()
            # Do not emit a separate heading-only parent before its child.
            # Do retain an empty section when its next heading is a sibling.
            if section_body or (headings and level <= headings[-1][0]):
                chunks.extend(self._section_chunks(headings, section_body))
            body = []
            headings = [(depth, title) for depth, title in headings if depth < level]
            headings.append((level, line.strip()))

        chunks.extend(self._section_chunks(headings, "\n".join(body).strip()))
        return chunks

    def _section_chunks(self, headings: list[tuple[int, str]], body: str) -> list[str]:
        context = "\n".join(title for _, title in headings)
        if not context and not body:
            return []
        prefix = context + "\n\n" if context and body else ""
        body_budget = self.chunk_size - len(prefix)

        if not body or body_budget < max(1, self.chunk_size // 4):
            section = context + ("\n\n" + body if body else "")
            return [
                fragment.strip()
                for fragment in RecursiveChunker(chunk_size=self.chunk_size).chunk(section)
                if fragment.strip()
            ]

        return [
            prefix + fragment.strip()
            for fragment in RecursiveChunker(chunk_size=body_budget).chunk(body)
            if fragment.strip()
        ]
