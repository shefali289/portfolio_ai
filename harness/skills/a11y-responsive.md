# Skill: Accessibility + Responsive Pass

**Used by:** Developer Agent, Review Agent
**When:** any UI change, before review

## Steps

1. **375px** - no horizontal scroll, nothing clipped, tap targets >=44px.
2. **Keyboard** - tab through: everything interactive reachable, focus visible,
   order logical. No keyboard trap in the chat or modal.
3. **Semantics** - real `<button>`/`<a>`, one `<h1>`, headings not skipped,
   landmarks present.
4. **Images** - meaningful `alt`; decorative images `alt=""`.
5. **Contrast** - body text >=4.5:1, large text >=3:1.
6. **Motion** - honour `prefers-reduced-motion`.
7. **Live regions** - streaming AI answers and agent progress announce via
   `aria-live="polite"`.
8. **States** - loading has a visible indicator; errors state what to do next.

## Do not

Test these values in unit tests. This is a manual pass; tests cover behaviour.

## Done when

375px and desktop both clean, keyboard-navigable, reduced motion honoured.
