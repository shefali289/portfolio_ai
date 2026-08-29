# Harness Skills

Reusable procedures agents invoke instead of re-deriving them each feature.

A **skill** is a repeatable *how*. An **agent** is a *role*. Agents call skills.

## Why they exist

Without skills, the Developer Agent works out how to add an endpoint from
scratch every time, and does it slightly differently each time. Skills make the
procedure explicit and identical, which keeps the codebase consistent and stops
the agent spending tokens rediscovering a settled pattern.

## Rules

- A skill is **procedural** - numbered steps someone can follow. Not an essay.
- Under 45 lines. Longer means it is two skills.
- It states its own **Done when** condition.
- If a skill and `learning/conventions.md` disagree, conventions win and the skill
  is corrected at `/complete`.
- Add a skill only when a procedure has been repeated. Do not pre-invent them.

## Index

See `harness/AGENT-MANIFEST.md` for which agent uses which skill.
