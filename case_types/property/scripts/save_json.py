import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Database.database import (
    connect,
    initialize_database,
    save_case_report,
    save_insurance_case,
)


BASE_DIR = PROJECT_ROOT
CASE_TYPES_DIR = BASE_DIR / "Working_3" / "case_types"
CURRENT_DIR = BASE_DIR / "Working_3" / "current"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and save extracted insurance JSON."
    )
    parser.add_argument("--case-type", default=DEFAULT_CASE_TYPE)
    parser.add_argument(
        "--case-dir",
        type=Path,
        help="Optional explicit case directory. Defaults to Working_3/case_types/<case-type>.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Optional path to a file containing the model's JSON response.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Where to save the validated JSON. Defaults to Working_3/current/output/data.json.",
    )
    parser.add_argument(
        "--database-url",
        help="Optional PostgreSQL URL. Defaults to DATABASE_URL or Database/database.py's placeholder URL.",
    )
    parser.add_argument(
        "--save-db",
        action="store_true",
        help="Also save the validated data into the database.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional Markdown report to save with the database case. Defaults to Working_3/current/output/final_report.md.",
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


def read_raw_text(input_path: Path | None) -> str:
    if input_path:
        return input_path.read_text(encoding="utf-8").strip()

    print("Paste the JSON response below, then press Ctrl+Z and Enter to save.")
    return sys.stdin.read().strip()


def extract_json_block(raw_text: str) -> str:
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in the provided text.")

    return cleaned[start : end + 1]


def validate_payload(payload: object, fields: list[str]) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("The JSON response must be an object.")

    missing_fields = [field for field in fields if field not in payload]
    extra_fields = [field for field in payload if field not in fields]

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    if extra_fields:
        raise ValueError(f"Unexpected fields found: {', '.join(extra_fields)}")

    normalized = {}
    for field in fields:
        value = payload[field]
        if value is None:
            value = ""
        elif not isinstance(value, str):
            value = str(value)
        normalized[field] = value.strip()

    return normalized


def main() -> None:
    args = parse_args()
    case_dir = resolve_case_dir(args.case_type, args.case_dir)
    fields = load_fields(case_dir)
    output_path = args.output or CURRENT_DIR / "output" / "data.json"
    report_path = args.report or CURRENT_DIR / "output" / "final_report.md"

    raw_text = read_raw_text(args.input)

    if not raw_text:
        raise ValueError("No input received.")

    json_text = extract_json_block(raw_text)
    payload = json.loads(json_text)
    normalized = validate_payload(payload, fields)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Validated JSON saved to: {output_path}")

    if args.save_db:
        with connect(args.database_url) as connection:
            initialize_database(connection, fields)
            case_id = save_insurance_case(connection, normalized, fields)
            if report_path and report_path.exists():
                report_content = report_path.read_text(encoding="utf-8")
                report_id = save_case_report(
                    connection,
                    case_id,
                    report_content,
                    str(report_path),
                )
                print(f"Final report saved to database report id: {report_id}")
            elif report_path:
                print(f"Report file not found, skipped database report save: {report_path}")
        print(f"Validated JSON saved to database case id: {case_id}")


if __name__ == "__main__":
    main()
