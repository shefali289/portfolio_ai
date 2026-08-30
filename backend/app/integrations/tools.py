"""The portfolio tool layer.

Six plain callables. This is the capability; MCP and HTTP are both thin adapters
over it, so a tool is written and tested once rather than twice.

`search_resume` reads through the existing retriever. It is a *reader* of RAG,
never a writer: no repository text is indexed and no retrieval parameter is
changed from here (HARNESS-RULES rule 15).
"""

from __future__ import annotations

from typing import Any

from app.integrations.github import GitHubClient
from app.rag.retriever import Retriever
from app.services.content import ContentService

TOOL_NAMES = (
    "get_profile",
    "get_projects",
    "search_projects",
    "search_resume",
    "get_skills",
    "get_github_projects",
)


class PortfolioTools:
    """Portfolio capability, exposed once and adapted twice."""

    def __init__(
        self,
        *,
        content: ContentService,
        retriever: Retriever,
        github: GitHubClient,
    ) -> None:
        self._content = content
        self._retriever = retriever
        self._github = github

    def get_profile(self) -> dict[str, Any]:
        """Return the portfolio owner's profile: name, title, location, summary."""
        return self._content.profile.model_dump(mode="json")

    def get_projects(self) -> list[dict[str, Any]]:
        """List every project in the portfolio."""
        return [p.model_dump(mode="json") for p in self._content.projects.projects]

    def search_projects(self, query: str) -> list[dict[str, Any]]:
        """Find portfolio projects matching a term, by name, description or technology."""
        needle = query.strip().lower()
        if not needle:
            return []
        matches = []
        for project in self._content.projects.projects:
            haystack = " ".join(
                [project.name, project.description or "", *project.technologies]
            ).lower()
            if needle in haystack:
                matches.append(project.model_dump(mode="json"))
        return matches

    def search_resume(self, query: str, k: int = 4) -> list[dict[str, Any]]:
        """Search the resume and portfolio content for passages relevant to a query."""
        return [
            {
                "text": hit.chunk.text,
                "source": hit.chunk.source,
                "type": hit.chunk.type,
                "score": round(hit.score, 4),
            }
            for hit in self._retriever.retrieve(query, k=k)
        ]

    def get_skills(self) -> list[dict[str, Any]]:
        """List the portfolio's skill groups and the skills in each."""
        return [g.model_dump(mode="json") for g in self._content.skills.groups]

    def get_github_projects(self) -> dict[str, Any]:
        """List the portfolio owner's public GitHub repositories, live.

        Returns `reason` instead of raising when GitHub is unavailable, so a
        caller can say why the list is empty rather than failing.
        """
        result = self._github.list_repos()
        return {
            "repos": [
                {
                    "name": r.name,
                    "description": r.description,
                    "url": r.url,
                    "language": r.language,
                    "topics": r.topics,
                    "pushed_at": r.pushed_at,
                }
                for r in result.repos
            ],
            "reason": result.reason,
        }
