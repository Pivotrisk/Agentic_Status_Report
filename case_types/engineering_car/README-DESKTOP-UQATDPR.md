# Engineering CAR Case Type

This folder contains the engineering Contractor's All Risk insurance workflow assets.

Included now:

- `format/engineering_car_format.md` as the editable engineering CAR survey report format
- `format/format.md` retained as a compatibility copy of the engineering CAR format
- `format/template.docx` based on the Jaljala-Ambarshanti-Prayan Joint Venture engineering CAR Word example
- `examples/example_output.md` converted from the Jaljala-Ambarshanti-Prayan Joint Venture sample report
- `prompt_manual.md` as the engineering CAR manual workflow prompt
- `Working_3/prompt/prompt_engineering_car` as the reusable root prompt for Codex chat
- `fields.json` as the engineering CAR extraction schema
- `scripts/` helper scripts copied from the property workflow and defaulted to `engineering_car`
- `examples/` for sample engineering CAR documents
- `previous_inputs/`, `previous_outputs/`, and `archives/` for portfolio history

Daily active work belongs in `Working_3/current/input/` and `Working_3/current/output/`. Use `Working_3/case_types/engineering_car/fields.json` to map OCR text from CAR policy schedules, intimation/deputation records, claim forms, stock and equipment lists, estimates, photographs, and other supporting documents into the report format.
