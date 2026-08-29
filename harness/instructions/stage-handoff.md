# Stage Handoff

How one lifecycle stage passes to the next.

## The rule

**A stage never dead-stops.** It ends by naming the next stage and asking
whether to continue — and continues in the same turn if the answer is yes.

```
/plan ──> /build ──> /review ──> /complete ──> /plan <next phase>
      ask         ask          ask           ask
```

Telling the user to "run `/build` next" and stopping is not a handoff. It makes
the human the message bus between stages that already know what follows them,
and the cost of that is paid on every stage of every phase.

## Ask, or continue silently?

| Situation | Behaviour |
|---|---|
| Normal end of a stage, gate passed | **Ask**, then continue if yes |
| User said "run the phase end to end" / "don't ask between stages" | **Continue**, no ask |
| Gate blocked, or findings are blocking | **Stop.** Report, and hand *back*, not forward |
| An open question the user still owes an answer to | **Stop.** The question comes first |
| A commit or push is staged and unapproved | **Stop.** See below |

## What a handoff must never do

- **Never approve a commit or push.** `harness/instructions/approval-gate.md` is
  not weakened by this file. "Continue to the next stage" is permission to keep
  working, never permission to write history. Those are separate questions and
  the second one is always asked on its own.
- **Never skip a blocking question.** If the stage produced a decision the user
  owes, that question is the end of the turn — not the handoff.
- **Never start the next phase over an unfinished one.** Rule 2 — one active
  feature at a time. `/complete` hands off only once the current task is in
  `tasks/completed/`.
- **Never relax a gate to keep the chain moving.** A blocked gate ends the
  chain; that is the gate working.

## Why ask rather than run the whole lifecycle unattended

Design and planning are cheap to redirect and expensive to undo once built on.
The ask between stages is where the user redirects for one sentence's worth of
effort. It costs one line and it is the last cheap moment before code exists.

Standing permission removes the ask — say so once ("run it end to end") and the
chain flows until it hits a gate, a blocking question, or a commit.
