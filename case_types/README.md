# Case Type Workspace

This folder is the future home for insurance-type-specific report assets.

Each case type can contain:

- `previous_inputs/` - older input sets for that portfolio.
- `previous_outputs/` - older outputs for that portfolio.
- `format/` - report templates and sample reports for that portfolio.
- `archives/` - archived completed cases for that portfolio.
- `fields.json` - fields to extract for that insurance type.
- `example_output.md` - sample completed report, when available.
- `prompt_manual.md` - prompt/instructions specific to that insurance type.
- `examples/` - sample input documents for that insurance type.
- `scripts/` - optional case-type-specific scripts or legacy references.

Current priority case types:

- `property`
- `marine`
- `motor`
- `engineering_car`

Additional folders are prepared for:

- `agriculture`
- `miscellaneous`

The current property workflow has been copied into `property/` as the starting point. Other case types are intentionally left as scaffolds until their formats, sample documents, and extraction requirements are provided.

Daily work uses `Working_3/current/input/` and `Working_3/current/output/`. The case type folders provide schemas, formats, examples, and archives.

The main scripts in `Working_3/` default to the `property` portfolio where a case type is needed and accept `--case-type` for other portfolios. For example:

`python Working_3/ocr.py`

`python Working_3/extract.py --case-type property`

`python Working_3/archive_case.py --case-type property`
