# Development workflow

## Branches and pull requests

- Keep `main` stable.
- Create short-lived branches such as `feat/sql-validator`, `feat/inventory-twin` or `docs/semantic-layer`.
- Open a pull request for each coherent change.
- Require at least one peer review from the agreed reviewer pair.
- Link the relevant Trello card(s) in the PR description.
- Do not merge with failing tests or unresolved review feedback.

## Definition of done

A task is complete only when:

1. Its Trello acceptance criteria are met.
2. Tests cover the behaviour and important failure cases.
3. Documentation/contracts are updated where relevant.
4. The author can explain the implementation and its limitations.
5. A reviewer has checked the code and evidence.
6. No secrets, private data or unapproved raw datasets are included.

## AI-assisted development

- Follow university AI-use rules and the team's agreed AI-tool policy.
- Do not paste secrets, credentials or personal data into AI tools.
- Record generated assistance, human changes and verification in the project AI usage log.
- Do not accept generated calculations without tests or independent checks.
- Simulator expected values in core unit tests must be hand-calculated by a human.
- The product LLM may interpret and explain; deterministic code owns calculations, SQL enforcement and solver construction.

## Testing expectations

- Unit tests for each module.
- Fixed fixtures and deterministic seeds for simulation tests.
- Contract tests for `/ask`, `/simulate` and `/optimize`.
- Security tests for destructive/multi-statement SQL, out-of-scope access, prompt injection, invalid parameters and out-of-catalog optimizer requests.
- Evaluation sets must be human-written or independently verified.
- CI runs tests on every pull request.

## Data handling

- Keep raw/local datasets in `data/raw/`, which is git-ignored.
- Commit data dictionaries, transformation scripts, small synthetic fixtures and provenance notes where permitted.
- Verify dataset licence and redistribution terms before committing any data extract.
- Label WWI-derived synthetic data and Egyptian financial assumptions accurately.
