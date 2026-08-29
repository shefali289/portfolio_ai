# Skill: TDD Cycle

**Used by:** Test Agent, Developer Agent
**When:** every behavioural change

## Steps

1. Write the smallest test that captures the required behaviour.
2. **Run it.** Capture the output.
3. Confirm it fails *for the expected reason* - not an import error, not a typo.
   A test that passes now is testing nothing. A test failing for the wrong
   reason is a broken test. Fix either before continuing.
4. Record the failure output in `handoffs/3-test.md`. That is the RED evidence.
5. Implement the minimum that makes it pass.
6. Run again. Confirm GREEN.
7. Refactor only if it improves clarity, with tests still green.

## Do not

- Write implementation before the test for the same behaviour.
- Test styling, class names, colours or animation timing.
- Assert a test passed without having run it.

## Done when

The test failed for the right reason, then passed, and the failure output is
recorded in the handoff.
