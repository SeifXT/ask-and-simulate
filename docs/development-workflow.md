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

- Follow the team's agreed policy in `docs/ai-tool-policy.md`.
- The team has acknowledged the policy's risk acceptance for sharing project-related sensitive information and active API keys in AI/team chats.
- This risk acceptance does not permit committing credentials to GitHub. Keep real credentials in local untracked environment files or approved secrets storage.
- No AI usage log is required by the team.
- Read and understand generated code before committing it.
- Do not accept generated calculations without tests or independent checks.
- Simulator expected values in core unit tests must be hand-calculated by a human.
- The product LLM may interpret and explain; deterministic code owns calculations, SQL enforcement, simulation and solver construction.
- Contributors must be able to explain their own work and its limitations.

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
