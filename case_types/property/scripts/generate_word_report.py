import argparse
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


WORKSPACE_DIR = Path(__file__).resolve().parents[3]
CASE_TYPES_DIR = WORKSPACE_DIR / "case_types"
CURRENT_DIR = WORKSPACE_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Word status report for one insurance case type portfolio."
    )
    parser.add_argument(
        "--case-type", required=True,
        choices=sorted(path.name for path in CASE_TYPES_DIR.iterdir() if path.is_dir()),
        help="Insurance case type; selects format/<case-type>_template.docx.",
    )
    parser.add_argument(
        "--case-dir",
        type=Path,
        help="Optional explicit case directory. Defaults to Working_3/case_types/<case-type>.",
    )
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--template", type=Path, help="Optional Word template override for the selected case type.")
    return parser.parse_args()


def resolve_case_dir(case_type: str, case_dir: Path | None) -> Path:
    return case_dir if case_dir else CASE_TYPES_DIR / case_type


def resolve_template(case_dir: Path, requested_template: Path | None, case_type: str) -> Path:
    template_path = (
        requested_template
        if requested_template is not None
        else case_dir / "format" / f"{case_type}_template.docx"
    )
    if not template_path.is_file():
        raise FileNotFoundError(
            f"Word template for case type '{case_type}' not found: {template_path}. "
            "Add the matching template or specify --template PATH."
        )
    return template_path


def clear_document(document: Document) -> None:
    body = document._body._element
    for child in list(body):
        if child.tag.endswith("sectPr"):
            continue
        body.remove(child)


def load_document(template_path: Path) -> Document:
    if template_path.exists():
        document = Document(template_path)
        clear_document(document)
    else:
        document = Document()

    section = document.sections[0]
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    normal_style = document.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11)
    return document


def add_runs_with_bold(paragraph, text: str) -> None:
    parts = text.split("**")
    for index, part in enumerate(parts):
        if not part:
            continue
        run = paragraph.add_run(part)
        run.bold = index % 2 == 1


def add_markdown_paragraph(document: Document, line: str, cover_mode: bool) -> None:
    if line.startswith("# "):
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(line[2:].strip())
        run.bold = True
        run.font.size = Pt(20)
        return

    if line.startswith("## "):
        paragraph = document.add_paragraph()
        paragraph.style = "Heading 1"
        run = paragraph.add_run(line[3:].strip())
        run.bold = True
        return

    if line.startswith("- "):
        paragraph = document.add_paragraph()
        paragraph.paragraph_format.left_indent = Inches(0.25)
        paragraph.paragraph_format.first_line_indent = Inches(-0.15)
        paragraph.add_run("- ")
        add_runs_with_bold(paragraph, line[2:].strip())
        return

    paragraph = document.add_paragraph()
    if cover_mode:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_runs_with_bold(paragraph, line.strip())


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(set(cell) <= {"-", ":", " "} for cell in cells)


def parse_table(lines: list[str], start_index: int) -> tuple[list[list[str]], int]:
    rows = []
    index = start_index
    while index < len(lines) and lines[index].strip().startswith("|"):
        line = lines[index].strip()
        if not is_table_separator(line):
            rows.append([cell.strip() for cell in line.strip("|").split("|")])
        index += 1
    return rows, index


def add_table(document: Document, rows: list[list[str]]) -> None:
    if not rows:
        return

    table = document.add_table(rows=1, cols=len(rows[0]))
    table.style = "Table Grid"

    for column_index, value in enumerate(rows[0]):
        cell = table.rows[0].cells[column_index]
        cell.text = value
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True

    for row_values in rows[1:]:
        cells = table.add_row().cells
        for column_index, value in enumerate(row_values):
            if column_index < len(cells):
                cells[column_index].text = value

    document.add_paragraph()


def build_document(markdown_text: str, template_path: Path) -> Document:
    document = load_document(template_path)
    lines = markdown_text.splitlines()
    index = 0
    cover_mode = True

    while index < len(lines):
        line = lines[index].rstrip()

        if not line.strip():
            document.add_paragraph()
            index += 1
            continue

        if line.startswith("## "):
            cover_mode = False

        if line.strip().startswith("|"):
            rows, index = parse_table(lines, index)
            add_table(document, rows)
            continue

        add_markdown_paragraph(document, line, cover_mode)
        index += 1

    return document


def unique_output_path(path: Path) -> Path:
    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def save_document(document: Document, output_path: Path) -> Path:
    try:
        document.save(output_path)
        return output_path
    except PermissionError:
        fallback_path = unique_output_path(output_path)
        document.save(fallback_path)
        print(f"Could not overwrite locked file: {output_path}")
        return fallback_path


def main() -> None:
    args = parse_args()
    case_dir = resolve_case_dir(args.case_type, args.case_dir)
    input_path = args.input or CURRENT_DIR / "current_output" / "final_report.md"
    output_path = args.output or CURRENT_DIR / "current_output" / "final_report.docx"

    template_path = resolve_template(case_dir, args.template, args.case_type)
    markdown_text = input_path.read_text(encoding="utf-8")
    document = build_document(markdown_text, template_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    saved_path = save_document(document, output_path)
    print(f"Word report saved to: {saved_path}")


if __name__ == "__main__":
    main()
