import argparse
import json
import textwrap
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = Path(__file__).resolve().parent
CASE_TYPES_DIR = BASE_DIR / "Working_3" / "case_types"
DEFAULT_CASE_TYPE = "property"

DEFAULT_FIELDS = [
    "name_of_insurer_company",
    "address_of_insurer_company",
    "type_of_policy",
    "name_of_insured",
    "bank_name",
    "insured_company_address",
    "insured_contact_number",
    "policy_number",
    "claim_number",
    "survey_report_number",
    "policy_insured_date",
    "period_of_insurance",
    "total_sum_insured",
    "breakdown_sum_insured",
    "endorsement_number",
    "cause_of_loss",
    "items_damaged",
    "deputation_date",
    "survey_date",
    "premium_amount",
    "subject_matter_insured",
    "insured_property_address",
    "nature_of_insured_property",
    "nature_of_building",
    "date_of_loss",
    "place_of_loss",
    "insured_location_from_policy",
    "date_of_intimation",
    "place_of_survey",
    "surveyor_name",
    "submitted_by",
    "surveyor_firm",
    "surveyor_license_number",
    "report_submission_date",
    "building_owner",
    "enclosed_documents",
    "incident_effect_summary",
    "spot_survey_observation",
    "estimated_claim_amount",
    "total_damaged_quantity",
    "estimated_claim_table_rows",
]


def default_current_output_dir() -> Path:
    return CURRENT_DIR / "current_output"


def parse_args() -> argparse.Namespace:
    current_output_dir = default_current_output_dir()
    parser = argparse.ArgumentParser(
        description="Build an extraction prompt for one insurance case type portfolio."
    )
    parser.add_argument("--case-type", default=DEFAULT_CASE_TYPE)
    parser.add_argument(
        "--case-dir",
        type=Path,
        help="Optional explicit case directory. Defaults to Working_3/case_types/<case-type>.",
    )
    parser.add_argument(
        "--ocr",
        type=Path,
        default=current_output_dir / "ocr_output.txt",
        help="OCR text file for the current case.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=current_output_dir / "prompt.txt",
        help="Prompt output file.",
    )
    return parser.parse_args()


def resolve_case_dir(case_type: str, case_dir: Path | None) -> Path:
    return case_dir if case_dir else CASE_TYPES_DIR / case_type


def load_fields(case_dir: Path) -> list[str]:
    fields_file = case_dir / "fields.json"
    if not fields_file.exists():
        return DEFAULT_FIELDS

    payload = json.loads(fields_file.read_text(encoding="utf-8"))
    fields = payload.get("fields", [])
    if not isinstance(fields, list) or not all(isinstance(field, str) for field in fields):
        raise ValueError(f"Invalid fields list in {fields_file}")
    return fields


def build_empty_schema(fields: list[str]) -> str:
    lines = ["{"]
    for index, field in enumerate(fields):
        comma = "," if index < len(fields) - 1 else ""
        lines.append(f'  "{field}": ""{comma}')
    lines.append("}")
    return "\n".join(lines)


def load_optional_example(case_dir: Path) -> str:
    candidates = [
        case_dir / "format" / "example_output.md",
        case_dir / "example_output.md",
    ]
    example_file = next((path for path in candidates if path.exists()), None)
    if not example_file:
        return ""

    content = example_file.read_text(encoding="utf-8").strip()
    if not content:
        return ""

    return f"""
Reference example:
- Use the example below only to understand domain terminology and the kinds of facts that commonly appear in these insurance documents.
- Do not copy the example values into the new output.
- Still return only the JSON object requested for the current OCR text.

{content}
"""


def build_prompt(document_text: str, fields: list[str], case_type: str, case_dir: Path) -> str:
    field_list = "\n".join(f"- {field}" for field in fields)
    schema = build_empty_schema(fields)
    example_section = load_optional_example(case_dir)

    return textwrap.dedent(
        f"""
        You are an expert insurance survey assistant.

        Task:
        Extract the required structured data for the `{case_type}` insurance portfolio from the OCR text and return ONLY valid JSON.

        Output requirements:
        - Return one JSON object only.
        - Use exactly the field names given below.
        - If a value is not available, return "".
        - Do not hallucinate.
        - Prefer exact values from the document.
        - If the same field appears in multiple places, choose the clearest and most authoritative source.
        - Keep dates exactly as written when possible.
        - Keep numbers, claim numbers, policy numbers, endorsement numbers, and addresses exactly as written.
        - If text is noisy because of OCR, infer carefully only when the intended value is still clear from the context.

        Required fields:
        {field_list}

        JSON schema:
        {schema}
        {example_section}
        OCR text begins below.

        OCR_TEXT_START
        {document_text}
        OCR_TEXT_END
        """
    ).strip() + "\n"


def main() -> None:
    args = parse_args()
    case_dir = resolve_case_dir(args.case_type, args.case_dir)
    input_file = args.ocr
    prompt_file = args.output

    if not input_file.exists():
        raise FileNotFoundError(f"OCR output not found: {input_file}")

    fields = load_fields(case_dir)
    document_text = input_file.read_text(encoding="utf-8")
    prompt = build_prompt(document_text, fields, args.case_type, case_dir)

    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(prompt, encoding="utf-8")

    print(f"Prompt saved to: {prompt_file}")
    print(
        "Next step: paste that prompt into Codex chat and save the JSON with "
        f"Working_3/save_json.py --case-type {args.case_type}"
    )


if __name__ == "__main__":
    main()
