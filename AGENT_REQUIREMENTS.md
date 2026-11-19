# One-click insurance report agent

Status: requirements and implementation plan. The automatic runner and correction learning described below are not implemented yet.

## Intended daily workflow

1. Prepare or update the approved base format for the selected insurance type.
2. Select the case type and place the current case documents in its input folder. Add survey notes or other facts that are not present in those documents.
3. Click **Generate report**. The application checks inputs, runs OCR, extracts facts, loads applicable saved rules, writes report narratives, validates the result, and generates Word plus a review summary.
4. Review and correct the result. Click **Save corrections** and choose whether each correction applies to this case, this case type, or all reports. Default factual edits to this case only.
5. The next generation loads the saved corrections and applicable rules automatically. Every run keeps its own version.

One click covers generation after setup and input selection. Reviewing a report and explaining a new correction are separate user actions.

## What the existing folder already provides

| Existing component | Current behavior |
| --- | --- |
| `ocr.py` | Reads PDFs and images using Tesseract with English and Nepali; writes combined text with document and PDF page markers. |
| `extract.py` | Builds an extraction prompt; does not call a model or extract JSON automatically. |
| `save_json.py` | Checks field names and saves JSON; optionally saves to a database. |
| `generate_word_report.py` | Creates Word reports, including a special property template path. |
| `archive_case.py` | Copies case inputs and outputs to an archive and normally clears current folders. |
| `case_types/*/fields.json` | Defines portfolio field names; these are field lists, not complete typed JSON Schemas. |
| `case_types/*/format/` | Contains report formats and Word templates for the prepared portfolios. |
| `prompt/prompt_property` | Describes a manual chat workflow that assumes OCR has already run. |
| Examples and archives | Provide reference cases, but have no explicit approval or reusable-correction metadata. |

Review scope: inspected folder inventory, root workflow scripts, active property prompt, property schema and Markdown format, and portfolio documentation. Historical PDFs and Word reports were not individually audited or visually verified.

## Fix these before adding the button

1. **Unify report content.** In `generate_word_report.py`, the property path reads JSON directly and builds narratives separately from Markdown. A corrected Markdown paragraph may never reach Word. Generate one structured report containing facts and final section text, then render both formats from it.
2. **Remove position-based template filling.** The property fallback writes to numbered paragraphs such as 81 and 86. Adding paragraphs to the base format can move those targets. Use named placeholders and named table anchors, and reject unsupported templates with a useful error.
3. **Fix the optional database dependency.** `save_json.py` imports `Database.database` at startup, but `../Database/database.py` was absent at inspection. Move database imports behind the optional database operation, or replace the dependency. Local report generation must work without a database.
4. **Choose canonical assets.** Property formats exist in several locations, and script copies exist under portfolios and in machine-conflict copies. Explicitly select the root scripts and one approved template configuration per portfolio. Keep legacy files out of runtime discovery.
5. **Make paths independent of launch location.** Prompts use `Working_3/...`, which assumes launching from the parent directory. Resolve paths from the project root in the runner and pass explicit input/output directories to each stage.
6. **Complete dependency setup.** The parent `requirements.txt` inspected does not list `pypdfium2`, `pytesseract`, or `python-docx`, although root scripts import them. Add a tested dependency manifest and check Tesseract plus `eng` and `nep` language data. Make its executable path configurable.
7. **Detect partial OCR failure.** OCR currently logs some failures and continues. Record success/failure per document and page; document/page labels alone must not count as usable extracted text. Surface missing pages before marking a report ready.
8. **Prevent unsupported survey claims.** Some template sentences assert that a survey occurred even with missing survey facts. Render such sentences only when current documents or user-entered survey notes support them.
9. **Declare portfolio readiness.** Marine and engineering assets exist, while some READMEs are outdated and other portfolios are scaffolds. Enable a case type only after its schema, template, and representative outputs pass validation.

## Components to add

Suggested names below are planned files, not existing working commands.

| Component | Responsibility |
| --- | --- |
| `app.py` | Local interface: case type, documents, survey notes, Generate report, progress, outputs, and Save corrections. |
| `run_agent.py` | Orchestrate preflight → OCR → extraction → saved rules → narratives → validation → rendering → run record. |
| `agent/model_client.py` | Selected model connection, structured response handling, timeouts, bounded retries, and usage limits. |
| `agent/feedback.py` | Compare generated and corrected content; save factual overrides and explicit reusable rules. |
| `agent/memory.py` | Retrieve only active rules matching the case type, field/section, and stated conditions. |
| `agent/validation.py` | Validate schema, source references, missing data, conflicts, calculations, and unresolved placeholders. |
| `agent/render.py` | Render Word and Markdown from the same approved report content. |
| `config/settings.json` | Paths, enabled case types, model selection, execution limits, and template selection. No secrets. |
| `config/surveyor_profile.json` | User-maintained firm, surveyor, license, and contact details; record these as profile facts rather than extracted facts. |
| `memory/rules.json` | Versioned reusable rules, scope, conditions, source correction, active status, and superseded rule IDs. |
| `memory/feedback.jsonl` | Append-only correction history including before, after, reason, scope, case/run ID, and date. |
| `runs/<case_id>/<run_id>/` | Input manifest, OCR, data, evidence, report content, Word/Markdown, validation results, and execution log. |
| `Start Agent.cmd` | Windows launcher using the configured environment; handles paths with spaces and reports setup errors. |
| `requirements.txt` and setup guide | Reproducible installation and configuration instructions. |
| `tests/fixtures/` | Selected approved cases and corrections for regression checks. |

For a first version, local files are sufficient for memory. A hosted database is optional. Do not build multiple independent agents merely to connect this predictable sequence of steps.

## What “learn from my corrections” means

Implement persistent correction memory loaded on every run. Editing an output file alone does not automatically teach a model, and retraining is not required for this first version.

Classify each saved change:

| Kind of change | How to retain it |
| --- | --- |
| Corrected name, amount, policy number, address, or date | Override for this case, with the user's correction recorded as its source. Never apply its literal value to other cases. |
| Wording preference | Reusable rule for the chosen section and portfolio, or global scope if explicitly selected. |
| Layout change | New version of the canonical template. Future runs use it automatically. |
| Extraction interpretation | Conditional rule stating which source and situation it applies to; test it against an approved example. |
| Missing survey information | Structured notes attached to this case; do not pretend the information came from OCR. |

Example reusable rule: “For property reports, show the location stated in the policy separately from the reported loss location when they differ.”

Example case-only correction: “For case CASE-001, replace the loss location with the corrected address entered by the surveyor.”

Store the original output before accepting edits. If edits are made in Word, provide an **Import corrected Word report** action that compares text and tables against that original. Require scope selection where reuse is ambiguous; arbitrary Word layout edits cannot reliably be converted into template rules automatically.

Explicit current-case instructions override reusable preferences. A template defines presentation, not case facts. Conflicting rules need an explicit replacement/supersession record; do not silently select one. Allow disabling a rule and regenerating an earlier version. Keep generated reports out of approved examples until the user marks them approved.

## Base format requirements

- Select one canonical layout per portfolio. If Word appearance is the priority, make the placeholder Word template the layout authority and use Markdown for preview.
- Use stable field placeholders, for example `{{policy_number}}`, plus section placeholders such as `{{incident_narrative}}`.
- Define dynamic table columns and an explicit repeating-row anchor. Do not depend on paragraph or table numbers.
- List mandatory fields, optional fields, missing-value wording, and conditional sections in the schema/configuration.
- Separate template guidance from printed report text.
- Validate template placeholders against supported fields before running OCR or spending model usage.
- Snapshot the template and its version/hash for every run. User format changes take effect on subsequent runs without overwriting earlier reports.
- Keep literal customer details and sample observations out of reusable templates.

## Reliability requirements

- Retain source filename, page where available, and supporting text for extracted facts in a separate evidence file.
- Distinguish extracted facts, profile defaults, user corrections, and derived narrative text.
- Flag conflicting source values and missing mandatory facts in the review summary; leave unsupported values empty or use the configured missing-value wording.
- Calculate numeric totals in code using decimal arithmetic where the underlying quantities, units, and currency support it. Flag mismatches rather than replacing quoted source totals silently.
- Preserve original date strings and distinguish calendar systems when stated. Do not silently convert uncertain dates.
- Give each run an isolated output folder; never consume stale `data.json` or OCR from another case.
- Prevent concurrent runs from overwriting shared state; save files atomically and preserve completed stages for safe retry.
- Record input hashes, selected model, prompt/template/rule versions, stage status, errors, and output paths.
- Treat document contents as evidence, not instructions for the software. Keep credentials outside templates, logs, and shared files.
- Keep draft/needs-review/approved status explicit. Generation should not send reports to anyone. Archiving should preserve working inputs by default and follow the review workflow.
- Render and visually check representative Word outputs, including long names, missing values, Nepali text, and multi-page tables.

## Information needed to implement

1. Confirm the first portfolio; property is the practical starting point based on the active prompt and existing assets.
2. Supply the approved base Word format and identify mandatory versus optional sections.
3. Choose the execution environment: a standalone local application needs a configured model service or local model; a workflow inside an existing agent environment needs its supported invocation mechanism. Verify that mechanism before choosing the launcher implementation.
4. For a hosted model, configure credentials and usage limits and decide which case content may be processed by that service. For local execution, establish hardware capacity and acceptable quality using representative cases.
5. Provide surveyor profile values, survey notes input fields, and preferred date/currency presentation.
6. Choose the correction interface: structured fields and section text in the app is easiest to compare; Word import can be added for your existing editing habits.
7. Select a small set of reviewed input/output pairs and examples of corrections that should apply to later reports.

## Implementation order and completion checks

**First: reliable property generation.** Fix paths and dependencies, choose canonical templates, remove fragile template indexing, connect automatic extraction/narrative generation, and produce consistent JSON, Markdown, and Word from one report object. A single click must reach either reviewable outputs or a clear stage-specific error without manual prompt copying.

**Second: correction memory.** Add structured editing, before/after history, scope selection, rule retrieval, and versioned reruns. Verify that a wording correction applies to a later matching case, while a corrected customer name does not leak into it. Verify that disabling a rule stops its future application.

**Third: broader coverage.** Add corrected Word import, portfolio-specific checks, and approved-case regression coverage. Extend to marine and engineering only after each portfolio's formats and examples are validated.

Acceptance scenarios: changed base template; missing mandatory field; contradictory policy/claim values; one failed OCR page; table total mismatch; long claim table; rerun after correction; failed model call; unsupported case type; simultaneous Generate clicks. No failure should overwrite the last successful report or be labelled approved.
