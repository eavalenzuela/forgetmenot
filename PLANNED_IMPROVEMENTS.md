# forgetmenot — Planned Improvements & Feature Roadmap

Scope: `forgetmenot` is one of the author's own security-research utilities. This is a **planning
roadmap only** — an engineering scoping document. Every item below is oriented toward code quality,
robustness, testability, documentation, and — importantly for a dual-use tool — **authorization and
responsible-use guardrails**. Nothing here describes or enhances covert-collection technique; the
emphasis is on making the tool safer, better-engineered, and harder to misuse.

## Improvements (existing behavior / quality / robustness / safety)

1. **Authorization gate as a hard precondition.** Refuse to run without an explicit
   `--authorized` flag plus an engagement/scope identifier, mirroring the safe-by-default pattern
   used by the author's other tools (stagehand/oauthive). *Rationale:* prevents accidental or
   unauthorized use and records intent.
2. **Structured, append-only audit logging.** Record every action (what, when, target, operator,
   outcome) to a local audit log. *Rationale:* accountability and chain-of-custody for authorized
   engagements.
3. **Safe-by-default configuration.** All potentially-sensitive behavior disabled unless explicitly
   enabled in config; ship conservative defaults. *Rationale:* least-surprise, least-harm.
4. **Replace hardcoded endpoints/paths with validated config.** Move any hardcoded addresses or
   paths into a config file with input validation and clear errors. *Rationale:* correctness and no
   embedded environment-specific assumptions.
5. **Robust error handling and timeouts.** Wrap all IO/network calls with timeouts, bounded retries,
   and explicit failure reporting instead of silent failure. *Rationale:* reliability and honest
   status.
6. **Structured, leveled logging** (replace `print`) with timestamps and redaction of sensitive
   values. *Rationale:* operable diagnostics without leaking captured data into logs.
7. **Python 3 modernization + linting.** Ensure clean `python3` execution, add `ruff`/`flake8`
   config, type hints on public functions. *Rationale:* maintainability.
8. **Automated test suite.** Unit tests with mocked IO covering argument parsing, config loading,
   error paths, and the authorization gate. *Rationale:* regression safety.
9. **Packaging + hygiene.** Add `.gitignore`, `pyproject.toml`/requirements, and remove any tracked
   sample artifacts; document a clean install. *Rationale:* reproducible, tidy repo.
10. **Documentation overhaul.** README with an explicit **authorized-use-only** scope statement, a
    threat-model/responsible-use note, and clear operator instructions. *Rationale:* set expectations
    and legal/ethical boundaries up front.

## New Features

1. **Dry-run / preview mode** that reports exactly what *would* happen without performing any action.
   *Rationale:* verification and safer operator workflow.
2. **Consent/scope manifest binding** — require the run to match a signed, reviewer-approved scope
   file (hosts/paths/authorization). *Rationale:* enforce blast-radius limits.
3. **Retention & cleanup controls** — configurable retention window with an automatic purge of any
   locally-stored data. *Rationale:* data minimization.
4. **Redaction/minimization toggle** for anything captured, on by default. *Rationale:* privacy and
   reduced sensitive-data footprint.
5. **Self-verification command** that checks config validity, authorization state, and environment
   preconditions and prints a green/red readiness summary. *Rationale:* fail fast, fail safe.
