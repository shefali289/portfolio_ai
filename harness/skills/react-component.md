# Skill: Add a React Component

**Used by:** Developer Agent (with Test Agent for step 1)
**When:** any new UI surface

## Steps

1. **Failing test** - `<Name>.test.tsx`: renders expected content, plus the
   three states below where the component fetches data. Run it, confirm RED.
2. **Types** - content types in `src/types/content.ts`, matching the Pydantic
   model exactly.
3. **API** - if it needs data, add one method to `src/lib/api.ts`. Components
   never call `fetch` directly.
4. **Component** - `src/components/<Name>.tsx`. Props typed, no `any`.
5. **States** - handle all three explicitly: **loading**, **error**, **empty**.
   Each must be reachable and covered by the test.
6. **Content** - render from `content/*.json` via the API. Never hardcode copy.
7. **Responsive + a11y** - see `a11y-responsive.md`.
8. **Run** - `npm test -- --run` and `npx tsc --noEmit`.

## Done when

Tests green, typecheck clean, all three states reachable, no hardcoded copy.
