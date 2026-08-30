"""Chunking, indexing and retrieval."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.rag.chunk import build_chunks
from app.rag.index import IndexMismatchError, VectorIndex
from app.rag.retriever import Retriever
from app.services.content import ContentService


def test_chunks_are_built_from_every_content_area(content_dir: Path) -> None:
    chunks = build_chunks(ContentService(content_dir))

    types = {c.type for c in chunks}
    assert {"role", "project", "profile"} <= types
    assert all(c.text.strip() for c in chunks)
    assert all(c.source for c in chunks)


def test_a_role_chunk_keeps_the_role_together(content_dir: Path) -> None:
    """One coherent idea per chunk — a role is not split mid-thought."""
    chunks = build_chunks(ContentService(content_dir))
    role = next(c for c in chunks if c.type == "role")

    assert "Test Engineer" in role.text
    assert "Test Company" in role.text
    assert "Did a testable thing." in role.text


def test_index_round_trips(tmp_path: Path, stub_embeddings) -> None:
    index = VectorIndex.build(
        texts=["alpha beta", "gamma delta"],
        metadata=[{"source": "a"}, {"source": "b"}],
        provider=stub_embeddings,
    )
    index.save(tmp_path / "idx")

    loaded = VectorIndex.load(tmp_path / "idx", provider=stub_embeddings)
    assert loaded.size == 2


def test_index_refuses_a_provider_mismatch(tmp_path: Path, stub_embeddings) -> None:
    """Gemini and MiniLM vectors are not interchangeable — refuse, never guess."""
    VectorIndex.build(["alpha"], [{"source": "a"}], stub_embeddings).save(tmp_path / "idx")

    from tests.conftest import StubEmbeddingProvider

    other = StubEmbeddingProvider(name="different-provider", dim=256)
    with pytest.raises(IndexMismatchError) as excinfo:
        VectorIndex.load(tmp_path / "idx", provider=other)

    assert "different-provider" in str(excinfo.value)


def test_index_refuses_a_dimension_mismatch(tmp_path: Path, stub_embeddings) -> None:
    VectorIndex.build(["alpha"], [{"source": "a"}], stub_embeddings).save(tmp_path / "idx")

    from tests.conftest import StubEmbeddingProvider

    with pytest.raises(IndexMismatchError):
        VectorIndex.load(tmp_path / "idx", provider=StubEmbeddingProvider(name="stub", dim=512))


def test_retrieval_finds_the_relevant_role(content_dir: Path, stub_embeddings) -> None:
    retriever = Retriever.from_content(ContentService(content_dir), stub_embeddings)

    hits = retriever.retrieve("What testable thing did the Test Engineer do?", k=3)

    assert hits
    assert any("Test Engineer" in h.chunk.text for h in hits)


def test_out_of_scope_question_scores_below_the_threshold(
    content_dir: Path, stub_embeddings
) -> None:
    """The grounding guarantee starts here: nothing relevant is retrieved."""
    retriever = Retriever.from_content(ContentService(content_dir), stub_embeddings)

    hits = retriever.retrieve("What is the capital of France?", k=3)

    assert not retriever.is_grounded(hits)
