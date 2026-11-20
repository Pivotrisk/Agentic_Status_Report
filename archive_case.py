import argparse
import json
import re
import shutil
from pathlib import Path


WORKSPACE_DIR = Path(__file__).resolve().parent
CURRENT_DIR = WORKSPACE_DIR
CASE_TYPES_DIR = WORKSPACE_DIR / "case_types"
DEFAULT_CASE_TYPE = "property"


def default_current_dir() -> Path:
    return CURRENT_DIR


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
        default=default_current_dir(),
        help="Workspace directory containing current_input/ and current_output/.",
    )
    parser.add_argument(
        "--keep-current",
        action="store_true",
        help="Keep files in the current input/output folders after archiving.",
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


def clear_directory_contents(path: Path) -> None:
    if not path.exists():
        return

    resolved = path.resolve()
    allowed_roots = {
        (CURRENT_DIR / "current_input").resolve(),
        (CURRENT_DIR / "current_output").resolve(),
    }
    if resolved not in allowed_roots:
        raise ValueError(f"Refusing to clear unexpected current directory: {path}")

    for child in path.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def main() -> None:
    args = parse_args()
    case_dir = resolve_case_dir(args.case_type, args.case_dir)
    current_output_dir = args.current_dir / "current_output"
    current_input_dir = args.current_dir / "current_input"
    cases_dir = case_dir / "archive_cases"

    data_file = current_output_dir / "data.json"
    ocr_file = current_output_dir / "ocr_output.txt"
    report_file = current_output_dir / "final_report.md"
    word_report_file = current_output_dir / "final_report.docx"

    data = load_data(data_file)

    insured_name = str(data.get("name_of_insured", "")).strip()
    claim_number = str(data.get("claim_number", "")).strip()

    insured_slug = slugify(insured_name, "unknown_insured")
    claim_slug = slugify(claim_number, "no_claim_number")
    named_report_file = current_output_dir / f"{insured_slug}_status_report.md"
    named_word_report_file = current_output_dir / f"{insured_slug}_status_report.docx"

    archive_dir = cases_dir / f"{insured_slug}__{claim_slug}"
    archive_dir = unique_path(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    input_archive_dir = archive_dir / "input"
    output_archive_dir = archive_dir / "output"
    input_archive_dir.mkdir()
    output_archive_dir.mkdir()

    archived_files = []

    word_report_source = (
        named_word_report_file
        if named_word_report_file.exists()
        else word_report_file
    )
    report_source = (
        named_report_file
        if named_report_file.exists()
        else report_file
    )

    file_map = {
        data_file: output_archive_dir / f"data_{insured_slug}.json",
        ocr_file: output_archive_dir / f"ocr_{insured_slug}.txt",
        report_source: output_archive_dir / f"status_report_{insured_slug}.md",
        word_report_source: output_archive_dir / f"status_report_{insured_slug}.docx",
    }

    for source, destination in file_map.items():
        if source.exists():
            shutil.copy2(source, destination)
            archived_files.append(destination)

    copied_output_sources = {source.resolve() for source in file_map if source.exists()}
    if current_output_dir.exists():
        for source in current_output_dir.iterdir():
            if source.resolve() in copied_output_sources:
                continue
            destination = unique_path(output_archive_dir / source.name)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            archived_files.append(destination)

    if current_input_dir.exists():
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
        summary_lines.append(f"- `{archived_file.relative_to(archive_dir).as_posix()}`")

    unique_path(output_archive_dir / "archive_summary.md").write_text(
        "\n".join(summary_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Case archived to: {archive_dir}")
    for archived_file in archived_files:
        print(f"- {archived_file}")

    if args.keep_current:
        print("Current input/output folders kept.")
        return

    clear_directory_contents(current_input_dir)
    clear_directory_contents(current_output_dir)
    print(f"Cleared current input folder: {current_input_dir}")
    print(f"Cleared current output folder: {current_output_dir}")


if __name__ == "__main__":
    main()
