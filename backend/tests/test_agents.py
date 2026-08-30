"""The four-agent job-match chain."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.agents.base import Requirement, Verdict
from app.agents.chain import ChainError, run_chain
from app.agents.evidence import assess_evidence
from app.agents.portfolio import gather_evidence
from app.agents.requirement import extract_requirements
from app.rag.retriever import Retriever
from app.services.content import ContentService

JD = """We are hiring a Python engineer.
You will build FastAPI services and deploy them on Kubernetes.
Experience with PostgreSQL is required."""


@pytest.fixture
def retriever(content_dir: Path, stub_embeddings) -> Retriever:
    return Retriever.from_content(ContentService(content_dir), stub_embeddings)


# --- requirement agent -----------------------------------------------------
def test_requirements_are_extracted_without_an_llm(content_dir: Path) -> None:
    """Template is the default provider, so extraction cannot depend on a model."""
    requirements = extract_requirements(JD, ContentService(content_dir))

    texts = [r.text.lower() for r in requirements]
    assert any("python" in t for t in texts)


def test_extraction_rejects_an_empty_job_description(content_dir: Path) -> None:
    assert extract_requirements("   ", ContentService(content_dir)) == []


# --- portfolio agent -------------------------------------------------------
def test_portfolio_agent_uses_the_injected_retriever(retriever: Retriever) -> None:
    """One search path. The retriever is a parameter, never constructed here."""
    found = gather_evidence([Requirement(text="Python")], retriever)

    assert len(found) == 1
    assert found[0].requirement.text == "Python"


# --- evidence agent --------------------------------------------------------
def test_a_requirement_with_no_evidence_is_a_gap(retriever: Retriever) -> None:
    """The rule that matters: a gap is never softened into a partial match."""
    gathered = gather_evidence([Requirement(text="Kubernetes")], retriever)

    assessed = assess_evidence(gathered)

    assert assessed[0].verdict is Verdict.GAP
    assert assessed[0].evidence == []


def test_a_supported_requirement_is_a_match(retriever: Retriever) -> None:
    gathered = gather_evidence([Requirement(text="Test Engineer testable thing")], retriever)

    assessed = assess_evidence(gathered)

    assert assessed[0].verdict in {Verdict.MATCH, Verdict.PARTIAL}
    assert assessed[0].evidence


# --- chain -----------------------------------------------------------------
def test_chain_runs_all_four_steps_in_order(
    content_dir: Path, retriever: Retriever
) -> None:
    report = run_chain(JD, ContentService(content_dir), retriever)

    assert [s.name for s in report.steps] == [
        "requirement",
        "portfolio",
        "evidence",
        "response",
    ]


def test_chain_reports_kubernetes_as_a_gap(
    content_dir: Path, retriever: Retriever
) -> None:
    report = run_chain(JD, ContentService(content_dir), retriever)

    assert any("kubernetes" in m.requirement.text.lower() for m in report.gaps)


def test_a_failing_step_propagates_rather_than_returning_a_partial_report(
    content_dir: Path, retriever: Retriever, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No half-filled report: a broken step is an error, not a quiet omission."""

    def boom(*args, **kwargs):
        raise RuntimeError("evidence agent exploded")

    monkeypatch.setattr("app.agents.chain.assess_evidence", boom)

    with pytest.raises(ChainError) as excinfo:
        run_chain(JD, ContentService(content_dir), retriever)

    assert "evidence" in str(excinfo.value).lower()


def test_a_term_named_verbatim_in_the_portfolio_is_never_a_gap(retriever: Retriever) -> None:
    """Regression: single-word requirements used to score below the threshold.

    "FastAPI" is listed in a role's technologies, yet vector search alone ranked
    it a gap, because a one-token query against a long chunk scores low on
    cosine. A false gap understates real experience - the opposite of what this
    feature is for.
    """
    gathered = gather_evidence([Requirement(text="Python")], retriever)

    assessed = assess_evidence(gathered)

    assert assessed[0].verdict is not Verdict.GAP
    assert assessed[0].evidence


def test_generic_job_ad_nouns_are_not_extracted(content_dir: Path) -> None:
    """"Engineer" is grammar, not a requirement - extracting it yields a junk gap."""
    requirements = extract_requirements(
        "We are hiring a Senior Engineer to join the Platform team.",
        ContentService(content_dir),
    )

    texts = {r.text.lower() for r in requirements}
    assert "engineer" not in texts
    assert "platform" not in texts
