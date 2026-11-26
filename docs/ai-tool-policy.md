# Team AI-tool and data-handling policy

**Status:** Draft for team review  
**Project:** Ask & Simulate  
**Applies to:** All six project members and anyone contributing to the repository  
**Last updated:** 2026-11-21

This policy records the team's agreed approach to AI-assisted project work and information sharing. Not every AI tool has identical privacy, retention or security protections. Each contributor is responsible for understanding the risks of the services and channels they use.

## 1. Approved AI tools and project context

- Team members may use AI tools they consider useful, subject to the safeguards in this policy.
- The team may create a project/workspace in an AI tool and provide it with project context, including project documentation, specifications, source code and other materials the team decides are appropriate to share.
- Team members may use AI tools to discuss project implementation, debug code, review designs, analyse information and help produce documentation.
- AI-generated output is a suggestion and must be reviewed and verified by a team member before it is relied on or committed.
- Before using a tool, contributors should consider its data retention, model-training, access-control and account-sharing settings. Providers do not guarantee that submitted information will stay confidential.
- Do not connect an AI tool to GitHub, cloud storage, email or other accounts unless the project owner (Seif) has approved the integration and its permissions.

## 2. Sensitive information and credentials: agreed risk

The team has agreed that project-related sensitive information and real, active API keys may be shared in AI chats/projects and team communication channels when needed for project work. The team understands and accepts the additional exposure risk associated with this decision.

This is an explicit team risk acceptance, not a claim that sharing credentials or sensitive information is secure. Information submitted to an external AI provider or messaging service may be processed, stored, reviewed or retained under that provider's terms and settings. Removing a key from a chat later may not remove all copies or records.

The following safeguards still apply:

- **Never commit API keys, access tokens, passwords, private keys, database credentials or other secrets to GitHub.** This applies to public and private repositories, branches, commits, pull requests, issues, Actions logs and release assets.
- Keep credentials in local, untracked `.env` files or an approved secret manager. The repository's `.gitignore` must exclude real secret files. `.env.example` may contain variable names and harmless placeholders only.
- Check every change before staging, committing or pushing. Do not assume a secret is safe to push because the repository is private or because it will be deleted in a later commit.
- Prefer scoped, least-privilege keys with usage limits and expiration where the provider supports them. Avoid sharing administrator or production credentials when a restricted development key will work.
- Share a credential only when the person or tool receiving it needs it for the project. Do not repost it unnecessarily or include it in documentation, screenshots, examples or test fixtures.
- If a credential is exposed somewhere it should not be, notify the project lead promptly. The project lead (Seif) is responsible for coordinating revocation or rotation of shared project API keys and investigating where they may have been retained. Deleting the visible message or file is not sufficient.
- Do not use real personal, customer, employee, university or third-party information unless the team has the necessary authority to use and share it. The team's risk acceptance does not override laws, contracts, data-owner restrictions or university requirements.

## 3. Project data rules

- Use the approved Wide World Importers (WWI) dataset and document its source and licence.
- Keep raw/local data in the repository's ignored `data/raw/` location. Do not commit raw extracts unless their licence and the project lead explicitly permit it.
- The team may include project data or sensitive project information in an AI project context when the team has decided to do so and has authority to share it, while accepting the provider-specific risks described above.
- Do not use real customer or employee data in this project unless separately authorised by the relevant data owner and permitted by applicable requirements.
- Label Egyptian cost inputs as sourced values or explicit assumptions. Do not present assumptions or synthetic-data results as real business evidence.
- Commit only approved code, documentation, data dictionaries and small synthetic test fixtures. Secrets and credentials are never approved for Git commits.

## 4. Rules for AI-generated code and analysis

AI output is a suggestion, not evidence that something works.

Every contributor must:

1. Read and understand generated code before committing it.
2. Run the relevant tests and inspect failures; do not claim tests passed unless they were run.
3. Independently verify important calculations, SQL results, optimisation constraints and simulation behaviour.
4. Check generated dependencies, licences, security implications and compatibility before adding them.
5. Check for hallucinated APIs, fabricated citations, unsafe SQL, prompt injection and unintended data exposure.
6. Be able to explain their contribution and its limitations during review and the project defence.

Project-specific controls:

- Deterministic Python code, not the language model, owns calculations, SQL enforcement and solver construction.
- The product LLM must not write or execute arbitrary solver code or change simulator logic.
- Simulator expected values in core unit tests must be hand-calculated by a human.
- SQL must be enforced as read-only in code; a prompt telling the model to be safe is not sufficient.
- AI-generated evaluation questions or expected answers must be human-written or independently verified.

## 5. Academic integrity and disclosure

- If the university or course sets rules for AI assistance, citation or disclosure, follow them.
- Do not submit AI-generated work as wholly human-authored if disclosure is required.
- Never invent sources, citations, experiments, test results or implementation progress.


## 6. Repository and credential security

- Never commit secrets, credentials, private keys, `.env` files, database dumps or personal data.
- Keep local secrets in untracked environment files. `.env.example` may contain variable names and harmless placeholders only.
- Do not put secrets in source code, notebooks, screenshots, issue descriptions, pull requests, commit messages or CI logs.
- Enable repository secret scanning and push protection where the repository's GitHub plan and settings support them. CI scanning is an additional layer, not a replacement.
- If a secret is exposed in GitHub, tell the project lead immediately. The project lead (Seif) is responsible for coordinating revocation or rotation of shared project API keys; the exposed secret must then be removed from repository history as appropriate. Deleting the visible line alone does not invalidate a leaked credential.
- Do not attempt to test with real credentials in shared logs or CI output.

## 7. Pull-request checklist

Before opening or approving a pull request, confirm:

- [ ] No API keys, credentials, private keys, `.env` files or other secrets are included.
- [ ] No data or material is committed without the required permission or licence.
- [ ] Any AI-generated contribution has been reviewed and understood by the author.
- [ ] Relevant tests have been run and their results are accurately reported.
- [ ] Calculations, SQL and optimisation behaviour have been independently checked where applicable.
- [ ] Relevant documentation has been updated.
- [ ] The author can explain the change and its limitations.

## 8. Team acknowledgement

The project lead confirmed on 2026-11-21 that all six members have read and acknowledged this policy, including the risk acceptance in Section 2.

**Team acknowledgement: confirmed by the project lead for all six members on 2026-11-21.**
