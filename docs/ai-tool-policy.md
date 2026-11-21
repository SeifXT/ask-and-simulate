# Team AI-tool and data-handling policy

**Status:** Draft for team review  
**Project:** Ask & Simulate  
**Applies to:** All six project members and anyone contributing to the repository  
**Last updated:** 2026-11-21

This policy sets the minimum rules for using AI assistants and handling project information. University rules, dataset licences and repository-owner instructions take priority whenever they are stricter.

## 1. Approved AI tools

- Use an AI assistant only when its use is permitted by the university and the relevant course/supervisor.
- The team must agree which tools are approved before treating any provider or account as officially approved. Record the agreed list below.
- Until that agreement is recorded, use AI only for non-sensitive tasks and do not upload project files or datasets.
- Do not connect an AI tool to the GitHub repository, cloud storage, email or other accounts unless the project owner has explicitly approved the integration and its permissions.
- Review the provider's privacy, retention and training settings. Do not assume that a paid account, private chat or disabled training setting makes sensitive information safe to share.

### Team-approved tools register

Complete this section after team review. A tool is approved only for the stated use.

| Tool | Approved use | Restrictions | Approval |
|---|---|---|---|
| ChatGPT | Pending team and university confirmation | Non-sensitive prompts only until approved | Pending |
| Claude | Pending team and university confirmation | Non-sensitive prompts only until approved | Pending |
| GitHub Copilot / other coding assistants | Pending team and university confirmation | No secrets, private data or unapproved dataset uploads | Pending |

## 2. Information that must never be pasted into AI tools

Never submit any of the following, whether in a prompt, file upload, screenshot, chat, code snippet or connected-app context:

- API keys, access tokens, passwords, private keys, recovery codes, session cookies or database credentials.
- Contents of .env files, credential stores, secret managers or private configuration files.
- Personal or identifiable information about customers, employees, students, supervisors or team members unless the university has explicitly approved that exact processing and the data has been appropriately protected.
- Confidential university, employer, client or third-party material that the team is not authorised to disclose.
- Private repository content or raw datasets unless the data owner, licence and university rules explicitly permit that use.

When asking for help, replace sensitive values with obvious placeholders such as YOUR_API_KEY or DB_PASSWORD. Prefer small, synthetic examples.

## 3. Project data rules

- Use the approved Wide World Importers (WWI) dataset and document its source and licence.
- Keep raw/local data in the repository's ignored data/raw/ location. Do not commit raw extracts unless their licence and the project lead explicitly permit it.
- Do not upload raw data to AI tools by default. A public or synthetic dataset is not automatically approved for every third-party upload.
- Do not use real customer or employee data in this project.
- Label Egyptian cost inputs as sourced values or explicit assumptions. Do not present assumptions or synthetic-data results as real business evidence.
- Commit only approved code, documentation, data dictionaries and small synthetic test fixtures.

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

- Follow the university's current rules for AI assistance, citation and disclosure.
- Do not submit AI-generated work as wholly human-authored if disclosure is required.
- Keep a concise project AI usage log. Record meaningful AI assistance, what the team changed, and how the result was verified.
- Never invent sources, citations, experiments, test results or implementation progress.

Suggested log fields: date, contributor, tool, task, type of assistance, files/sections affected, human changes, verification performed.

## 6. Repository and credential security

- Never commit secrets, credentials, private keys, .env files, database dumps or personal data.
- Keep local secrets in untracked environment files. .env.example may contain variable names and harmless placeholders only.
- Do not put secrets in source code, notebooks, screenshots, issue descriptions, pull requests or commit messages.
- Enable repository secret scanning and push protection where the repository's GitHub plan and settings support them. CI scanning is an additional layer, not a replacement.
- If a secret is exposed, tell the repository owner immediately, revoke or rotate it at the provider, then remove it from the repository history as appropriate. Deleting the visible line alone does not invalidate a leaked credential.
- Do not attempt to test with real credentials in shared logs or CI output.

## 7. Pull-request checklist

Before opening or approving a pull request, confirm:

- [ ] No secrets, credentials, personal data or unapproved raw data are included.
- [ ] Any AI-generated contribution has been reviewed and understood by the author.
- [ ] Relevant tests have been run and their results are accurately reported.
- [ ] Calculations, SQL and optimisation behaviour have been independently checked where applicable.
- [ ] Documentation and the AI usage log have been updated where relevant.
- [ ] The author can explain the change and its limitations.

## 8. Team acknowledgement

Each of the six members must read this policy, raise any concerns, and explicitly confirm agreement. Record the final approved tool list and any amendments in the repository.

| Member | GitHub username | Read and agreed | Date |
|---|---|---|---|
| Member 1 | Pending | Pending | |
| Member 2 | Pending | Pending | |
| Member 3 | Pending | Pending | |
| Member 4 | Pending | Pending | |
| Member 5 | Pending | Pending | |
| Member 6 | Pending | Pending | |

**This draft is not fully approved until all six members have acknowledged it.**
