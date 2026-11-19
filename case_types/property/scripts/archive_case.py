import argparse
import json
import re
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = BASE_DIR / "Working_3" / "current"
CASE_TYPES_DIR = BASE_DIR / "Working_3" / "case_types"
DEFAULT_CASE_TYPE = "property"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive one insurance case type portfolio output."
    )
    parser.add_argument("--case-type", default=DEFAULT_CASE_TYPE)
    parser.add_argument(
        "--case-dir",
        type=Path,
        help="Optional explicit case directory. Defaults to Working_3/case_types/<case-type>.",
    )
    parser.add_argument(
        "--current-dir",
        type=Path,
        default=CURRENT_DIR,
        help="Current working case directory containing input/ and output/.",
    )
    return parser.parse_args()


def resolve_case_dir(case_type: str, case_dir: Path | None) -> Path:
    return case_dir if case_dir else CASE_TYPES_DIR / case_type


def slugify(value: str, default: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip()).strip("_").lower()
    return cleaned or default


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 2
    while True:
        candidate = path.with_name(f"{path.name}_{counter}")
        if not candidate.exists():
            return candidate
        counter += 1


def load_data(data_file: Path) -> dict:
    if not data_file.exists():
        raise FileNotFoundError(f"Missing JSON file: {data_file}")

    with data_file.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError(f"{data_file} must contain a JSON object.")

    return payload


def main() -> None:
    args = parse_args()
    case_dir = resolve_case_dir(args.case_type, args.case_dir)
    current_output_dir = args.current_dir / "output"
    current_input_dir = args.current_dir / "input"
    cases_dir = case_dir / "archives" / "cases"

    data_file = current_output_dir / "data.json"
    ocr_file = current_output_dir / "output.txt"
    report_file = current_output_dir / "final_report.md"
    word_report_file = current_output_dir / "final_report.docx"

    data = load_data(data_file)

    insured_name = str(data.get("name_of_insured", "")).strip()
    claim_number = str(data.get("claim_number", "")).strip()

    insured_slug = slugify(insured_name, "unknown_insured")
    claim_slug = slugify(claim_number, "no_claim_number")

    archive_dir = cases_dir / f"{insured_slug}__{claim_slug}"
    archive_dir = unique_path(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)

    archived_files = []

    file_map = {
        data_file: archive_dir / f"data_{insured_slug}.json",
        ocr_file: archive_dir / f"ocr_{insured_slug}.txt",
        report_file: archive_dir / f"status_report_{insured_slug}.md",
        word_report_file: archive_dir / f"status_report_{insured_slug}.docx",
    }

    for source, destination in file_map.items():
        if source.exists():
            shutil.copy2(source, destination)
            archived_files.append(destination)

    if current_input_dir.exists():
        input_archive_dir = archive_dir / "input_documents"
        shutil.copytree(current_input_dir, input_archive_dir, dirs_exist_ok=True)
        archived_files.append(input_archive_dir)

    summary_lines = [
        "# Case Archive",
        "",
        f"- Case type: {args.case_type}",
        f"- Insured name: {insured_name or 'Unknown'}",
        f"- Claim number: {claim_number or 'Unknown'}",
        "",
        "## Saved Files",
    ]

    for archived_file in archived_files:
        summary_lines.append(f"- `{archived_file.name}`")

    (archive_dir / "README.md").write_text(
        "\n".join(summary_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Case archived to: {archive_dir}")
    for archived_file in archived_files:
        print(f"- {archived_file}")


if __name__ == "__main__":
    main()
