---
description: Following requests, state changes, and operational handoffs through HyperQuote, Stockroom, Waymark, and Leafmark.
---
# Following a request through a system

A screen shows an action. The useful engineering question is what that action commits the system to doing, which records it changes, and who depends on the result.

An accounting background makes those questions familiar. A record has a purpose, a responsible person, and consequences for the next step. Software needs the same clarity, including when an action fails or is retried.

## Begin with the handoff

In HyperQuote, a material request connects customer planning to quotation, stock, payment, dispatch, and delivery. Those are different responsibilities around related records. The interface has to make the current task clear without losing the context needed by the next team.

Modern applies the same idea to a smaller journey. A visitor exploring a construction service should reach the inquiry with that context carried forward. The handoff begins before the form is submitted.

[Explore the career-project gallery](https://github.com/yaqyn-dev) for the public showcases and their scope.

## Separate a suggestion from a committed change

Stockroom's local warehouse prototype can suggest a storage place. That suggestion leaves balances unchanged. Confirmation rechecks capacity and contents inside a write transaction, then records the balance change and movement history together.

Those are separate operations with separate meanings. The prototype also associates a request identifier with a confirmed movement so an unchanged retry does not become a second stock movement.

The prototype remains private and is not intended for live inventory use. The workflow is useful evidence; it does not establish production readiness or an implemented Odoo integration.

## Preserve work when a save fails

Two browser views can act on the same record. Waymark checks revisions when a link is edited; Leafmark rejects a stale note save rather than silently replacing newer text.

A rejected save needs a useful outcome in the interface. Leafmark preserves the draft and lets it be downloaded as Markdown, so a server-side refusal does not mean losing the writing.

[Explore Leafmark](https://github.com/yaqyn/leafmark-notebook) or [read Waymark's request-diagnosis walkthrough](https://github.com/yaqyn/waymark-link-shortener/blob/main/docs/observability.md).

## Use the checks that answer the question

A parser change needs examples of valid and invalid input. A stock movement needs capacity, balance, and retry checks. A layout change needs a narrow viewport and keyboard use. A deployment needs verification of the exact published commit and the behavior served to a visitor.

The working loop is:

1. Define the task, operating constraints, and intended result.
2. Model the records, permissions, transitions, and failure cases.
3. Implement the interface and server behavior around the same rules.
4. Run relevant checks and inspect the complete journey.
5. Document the result and distinguish what was verified locally, in CI, and live.

Claude Code and Codex support implementation, debugging, and review within that process. Requirements, decisions, and the resulting work remain my responsibility.

[Explore the projects](/projects/) or [return to the notes](/notes/).
