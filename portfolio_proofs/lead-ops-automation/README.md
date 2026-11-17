# Lead Operations Automation | evidence-gated request triage

**Independent public portfolio demonstration for AI operations, forward-deployed and business analytics internships.**
**Status:** locally tested synthetic prototype. Not a deployed product, not a live LLM/AI agent, and **not source code from private RUIYA CallAssist**.

## Problem and approach

Commercial operations teams receive vague requests. A workflow can fail if it silently assumes a quantity, material or contact. This example demonstrates a *human-in-the-loop* intake workflow:

1. Ingest a fictional business request and preserve its original ID.
2. Detect one unambiguous material, quantity in kg and contact email.
3. Route incomplete or ambiguous requests to clarification.
4. Route complete requests to a human to validate facts and prepare any commercial quote.
5. Keep evidence snippets, missing fields and the next action in structured output.

The implementation is intentionally **deterministic and rule-based** (standard-library Python, no external calls). This is a reliability proof, not a claim of advanced LLM engineering.

## Evidence and reproducibility

Run with Python 3.10+:

```sh
python portfolio_proofs/lead-ops-automation/demo.py
cd portfolio_proofs/lead-ops-automation
python -m unittest -v
```

Validation on 17 November 2026: **8/8 local tests passed**. The four fictional input examples produce 2 `ready_for_human_review` and 2 `needs_clarification` outcomes. Checks include missing data, ambiguous materials, duplicate IDs, invalid input and required human approval. This is a controlled fixture, not a real-world accuracy or business-impact statistic.

## Job-relevant skills demonstrated

- Operations intake and exception triage
- Structured data extraction with explicit evidence
- Reproducible testing, negative cases and traceability
- Clear handoff boundaries: no automatic quoting, sending, payments or business commitments

**Limitations:** recognizes only a small fixed list of materials and quantities expressed in kg; does not interpret free-form ambiguity beyond these rules, authenticate users, handle personal-data retention or deploy to production. An LLM extension would require measured extraction accuracy, adversarial cases, privacy review, human audit and observed real-world process outcomes.

## Relationship to RUIYA CallAssist

RUIYA CallAssist is a **separate private prelaunch business system**. The public demonstration above was written independently from scratch using fictional request data; no RUIYA source files, provider settings, credentials, customer records or proprietary architecture are published. RUIYA's provider voice-call integration has not been represented as operational.

## Interview walkthrough

Explain the problem -> run the example -> inspect the evidence map -> show the 8 tests -> demonstrate the ambiguous-material failure case -> discuss when to add LLMs, evaluation and real-user testing.

Prepared as a portfolio proof, November 2026. Please inspect the implementation and be ready to explain every decision in an interview.
