# Store contract

Use `~/.codex/personal-memory` as the default root, or the root explicitly provided by the user.

- Read `private-inbox/*.jsonl` as immutable captured events and deduplicate by `event_id`.
- Append valid evidence objects to `evidence/events.jsonl`, following `schemas/evidence.schema.json` and pointing to source event IDs.
- Update only the relevant file under `hypotheses/`. Preserve supporting evidence, refuting evidence, confidence, scope, uncertainty, and proposed behavior change.
- Write a dated Markdown report under `reviews/` with processed IDs, changed candidates, exact evidence and counterevidence, false-positive risks, hypothetical answer changes, and questions for user confirmation.
- Do not edit `runtime/active-profile.md` while shadow mode is enabled.
