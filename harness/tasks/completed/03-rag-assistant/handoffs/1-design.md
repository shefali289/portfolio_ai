# Handoff: Design -> Planning

## Done
Two parts: **(A)** strip the evidence/provenance layer so the app shows the
resume as it is, then **(B)** the RAG assistant. (A) runs first — it changes what
the UI renders, and (B)'s citation UI depends on the open question below.

## Part A — resume as it is
`visual-design` added a layer presenting *information about the content* beside
the content. The user rejected it: show the resume, assume nothing. **Remove,
do not restyle:**

- `App.tsx:113` "◆ Evidence-backed portfolio" eyebrow; the footer source line
- `Profile.tsx:39-46` derived counts; `:53` "Explore the evidence" → "View work"
- `SkillsExplorer.tsx:42` "N of M skills evidenced"; `:80-115` the evidence
  expansion, `data-proven`, "Evidence not yet documented…"
- `.provenance` footers in `ProjectGallery` and `Contact`

`SkillsExplorer` becomes a **plain grouped skill list** — the resume lists skills
in categories, so that is what renders. Its evidence tests go with the feature.

**Also inferred, therefore also out:** the `evidence` refs in `skills.json` were
the agent's inference — the resume never says "Python was used at Spark". Deleting
them and the `todo` notes also removes `_validate_evidence_refs` and its test.

Tokens, dark scheme, timeline, project cards and reveal **stay** — only the
meta-layer goes. `.provenance`/`.meta` remain for dates and locations.

## Part B — RAG
Per `docs/plan.md` and the two skills: chunk via `ContentService`,
`EmbeddingProvider` (Gemini | local), FAISS with provider+dim stamped and a
**refused mismatch**, `AIProvider` (Gemini | Ollama | template), and `POST
/api/ai/chat` returning answer + timings.

## You need to know
1. **Grounding is not negotiable** — rule 18 and this phase's own criterion: an
   out-of-scope question is refused, never answered. That is anti-hallucination,
   not presentation, and it survives Part A whatever we decide below.
2. **`template` is the default fallback** so the demo works with no API key.
3. **No new dependency**: `faiss-cpu`, `numpy`, `httpx` are pinned;
   `sentence-transformers` stays local-only (torch ≈1 GB vs the 500 MB limit).
4. **Removing `evidence` is content surgery** — go via the models and
   `ContentService`, then re-ingest.

## Files
- `frontend/src/components/{Profile,SkillsExplorer,ProjectGallery,Contact,AskPortfolio}.tsx`, `App.tsx`
- `content/skills.json`, `backend/app/services/content{,_models}.py` + tests
- `backend/app/rag/{chunk,embeddings,index,retriever,ingest}.py`, `app/ai/{provider,prompts}.py`, `app/api/{routes,schemas}.py`

## Do NOT re-read
`docs/architecture.md`, `docs/plan.md`, both RAG skills, `index.css`.

## Open questions
**Do AI answers still show source chips?** "No source of evidence" clearly covers
the portfolio UI. For a *generated* answer a citation is the reader's only way to
check the model invented nothing, and the brief requires it. Planning assumes
**chips stay on AI answers only**. Affects step 10 only.

## New learnings
- A provenance layer reads as the tool talking about itself. Show the content.
