---
name: personal-memory-engine
description: Build and review an evidence-backed personal collaboration profile from natural Codex use. Use when processing the private memory inbox, extracting durable preferences or corrections, updating concept-level cognitive boundaries, reconciling counterevidence, producing a shadow-mode review, or preparing a candidate profile for user confirmation.
---

# Personal Memory Engine

Build revisable hypotheses from evidence without turning casual language into identity claims.

## Load the contract

Read `references/inference-policy.md` and `references/store-contract.md` completely before processing any inbox record.

## Process a batch

1. Read `runtime/mode.json` and stop any profile activation when `mode` is `shadow`.
2. Read unprocessed JSONL records from `private-inbox/`; deduplicate by `event_id`.
3. Select only evidence that could materially improve future collaboration.
4. Separate the minimal source quote, factual observation, and inferred claim.
5. Append immutable evidence records to `evidence/events.jsonl`.
6. Update the narrowest relevant hypothesis file. Preserve uncertainty and counterevidence.
7. Write a dated review report that makes every inference traceable.
8. Run `python3 scripts/validate_store.py <memory-root>`.

## Apply safeguards

- Treat questions as requests for help, not proof of ignorance.
- Treat one-turn instructions as local unless the user explicitly makes them durable.
- Keep new hypotheses as `candidate` during shadow mode.
- Never edit `runtime/active-profile.md` during shadow mode.
- Let the current request override every stored preference.
- Ask for confirmation before any high-impact claim would change decisions, values framing, or substantial work.

## Report results

State how many events were processed, which candidates changed, what evidence supports or refutes them, and which uncertain claims need user review. Do not claim that personalization is active while `personalization_enabled` is false.
