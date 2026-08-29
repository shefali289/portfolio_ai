# Skill: Extract Resume Content

**Used by:** Developer Agent
**When:** populating or amending `content/*.json`

## The rule that overrides everything

**Never invent.** No employer, date, metric, title, technology or achievement
that is not in the source resume. If the portfolio needs a field the resume does
not supply, write `"TODO: <what is needed>"` and surface it in the handoff.

Inventing content is the one failure that makes the whole portfolio unusable in
an interview - it must be defensible line by line.

## Steps

1. Read the resume section. Extract only what it states.
2. Map into the target file: `profile` / `experience` / `skills` / `projects` /
   `engineering-notes`.
3. Keep the resume's own numbers and wording for metrics. Do not round, inflate,
   or restate "hours to minutes" as a percentage.
4. Every skill entry must name where it was used - skills are evidence-linked,
   so an unsupported skill has nowhere to point.
5. Add the matching Pydantic model and TS type.
6. Validate: load through `ContentService` and confirm it parses.
7. List every `TODO` placeholder in the handoff.

## Done when

Content parses, every claim traces to a resume line, and TODOs are reported.
