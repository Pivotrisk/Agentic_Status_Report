import argparse
import json
import re
from pathlib import Path
from zipfile import BadZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


BASE_DIR = Path(__file__).resolve().parent.parent
CASE_TYPES_DIR = BASE_DIR / "Working_3" / "case_types"
CURRENT_DIR = BASE_DIR / "Working_3" / "current"
DEFAULT_CASE_TYPE = "property"
DEFAULT_TEMPLATE = BASE_DIR / "draft" / "Status Report" / "TR INTERNATIONAL ,SITAPAILA.docx"


def default_current_output_dir() -> Path:
    return CURRENT_DIR / "output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Word status report for one insurance case type portfolio."
    )
    parser.add_argument("--case-type", default=DEFAULT_CASE_TYPE)
    parser.add_argument(
        "--case-dir",
        type=Path,
        help="Optional explicit case directory. Defaults to Working_3/case_types/<case-type>.",
    )
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    return parser.parse_args()


def resolve_case_dir(case_type: str, case_dir: Path | None) -> Path:
    return case_dir if case_dir else CASE_TYPES_DIR / case_type


def resolve_template(case_dir: Path, requested_template: Path) -> Path:
    if requested_template != DEFAULT_TEMPLATE:
        return requested_template

    format_dir = case_dir / "format"
    candidates = [
        format_dir / "template.docx",
        format_dir / "word_template.docx",
        case_dir / "template.docx",
    ]
    candidates.extend(sorted(format_dir.glob("*.docx")))

    return next((path for path in candidates if path.exists()), requested_template)


def slugify(value: str, default: str = "insured") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip()).strip("_").lower()
    return cleaned or default


def load_insured_slug(current_output_dir: Path) -> str:
    data_file = current_output_dir / "data.json"
    if not data_file.exists():
        return "insured"

    try:
        payload = json.loads(data_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "insured"

    insured_name = ""
    if isinstance(payload, dict):
        insured_name = str(payload.get("name_of_insured", "")).strip()

    return slugify(insured_name)


def load_case_data(current_output_dir: Path) -> dict:
    data_file = current_output_dir / "data.json"
    if not data_file.exists():
        return {}

    try:
        payload = json.loads(data_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}

    return payload if isinstance(payload, dict) else {}


def value(data: dict, key: str, default: str = "") -> str:
    raw_value = data.get(key, default)
    if raw_value is None:
        return ""
    if isinstance(raw_value, list):
        return "\n".join(str(item).strip() for item in raw_value if str(item).strip())
    return str(raw_value).strip()


def prefixed(label: str, text: str) -> str:
    return f"{label}{text}" if text else label.rstrip()


def markdown_bullet_list(data: dict, key: str) -> str:
    raw_value = data.get(key, "")
    if raw_value is None:
        return ""

    if isinstance(raw_value, list):
        return "\n".join(f"- {str(item).strip().lstrip('- ').strip()}" for item in raw_value if str(item).strip())

    lines = []
    for line in str(raw_value).splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if cleaned.startswith("- "):
            lines.append(cleaned)
        else:
            lines.append(f"- {cleaned.lstrip('- ').strip()}")
    return "\n".join(lines)


def has_placeholders(document: Document) -> bool:
    body_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    table_text = "\n".join(
        cell.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
    )
    return "{{" in body_text or "{{" in table_text


def default_markdown_path(current_output_dir: Path) -> Path:
    insured_slug = load_insured_slug(current_output_dir)
    named_path = current_output_dir / f"{insured_slug}_status_report.md"
    if named_path.exists():
        return named_path
    return current_output_dir / "final_report.md"


def default_output_path(current_output_dir: Path) -> Path:
    insured_slug = load_insured_slug(current_output_dir)
    return current_output_dir / f"{insured_slug}_status_report.docx"


def clear_document(document: Document) -> None:
    body = document._body._element
    for child in list(body):
        if child.tag.endswith("sectPr"):
            continue
        body.remove(child)


def load_document(template_path: Path) -> Document:
    if template_path.exists():
        try:
            document = Document(template_path)
            clear_document(document)
        except (PermissionError, BadZipFile, OSError) as exc:
            print(f"Could not load Word template: {template_path}")
            print(f"Reason: {exc}")
            print("Continuing with a blank Word document.")
            document = Document()
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


def set_paragraph_text(paragraph, text: str) -> None:
    """Replace paragraph text while keeping the paragraph and first-run styling."""
    if paragraph.runs:
        paragraph.runs[0].text = text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(text)


def set_cell_text(cell, text: str) -> None:
    paragraph = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()
    set_paragraph_text(paragraph, text)
    for extra_paragraph in cell.paragraphs[1:]:
        set_paragraph_text(extra_paragraph, "")


def replace_placeholders_in_text(text: str, context: dict[str, str]) -> str:
    def replacement(match: re.Match) -> str:
        return context.get(match.group(1).strip(), "")

    return re.sub(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}", replacement, text)


def replace_placeholders_in_paragraph(paragraph, context: dict[str, str]) -> None:
    original = paragraph.text
    if "{{" not in original:
        return
    set_paragraph_text(paragraph, replace_placeholders_in_text(original, context))


def replace_placeholders(document: Document, context: dict[str, str]) -> None:
    for paragraph in document.paragraphs:
        replace_placeholders_in_paragraph(paragraph, context)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_placeholders_in_paragraph(paragraph, context)

    for section in document.sections:
        for container in (section.header, section.footer):
            for paragraph in container.paragraphs:
                replace_placeholders_in_paragraph(paragraph, context)
            for table in container.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            replace_placeholders_in_paragraph(paragraph, context)


def split_items(items_text: str) -> list[str]:
    parts = re.split(r"\r?\n|;", items_text)
    if len(parts) == 1:
        parts = re.split(r",|\band\b", items_text)
    return [part.strip(" -") for part in parts if part.strip(" -")]


def parse_estimated_claim_rows(data: dict) -> list[list[str]]:
    rows_text = value(data, "estimated_claim_table_rows")
    rows: list[list[str]] = []
    for line in rows_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("*`") for cell in line.strip("|").split("|")]
        if len(cells) >= 6:
            rows.append(cells[:6])
        elif len(cells) >= 3:
            rows.append([cells[0], cells[1], "", "", "", cells[2]])

    if rows:
        return rows

    return [
        [str(index), item, "", "", "", ""]
        for index, item in enumerate(split_items(value(data, "items_damaged")), start=1)
    ]


def remove_table_row(table, row_index: int) -> None:
    row = table.rows[row_index]
    row._element.getparent().remove(row._element)


def remove_paragraph(paragraph) -> None:
    paragraph._element.getparent().remove(paragraph._element)


def remove_sample_photo_section(document: Document) -> None:
    start_index = None
    for index, paragraph in enumerate(document.paragraphs):
        if paragraph.text.strip().upper() == "PHOTOGRAPHS":
            start_index = index
            break

    if start_index is None:
        return

    for paragraph in list(document.paragraphs[start_index:]):
        remove_paragraph(paragraph)


def ensure_table_rows(table, row_count: int) -> None:
    while len(table.rows) < row_count:
        table.add_row()
    while len(table.rows) > row_count:
        remove_table_row(table, len(table.rows) - 1)


def ensure_table_columns(table, column_count: int) -> None:
    while len(table.columns) < column_count:
        table.add_column(Inches(1.0))


def fill_key_value_table(table, updates: dict[str, str]) -> None:
    for row in table.rows:
        if len(row.cells) < 2:
            continue
        label = row.cells[0].text.strip()
        if label in updates:
            set_cell_text(row.cells[1], updates[label])


def join_sentence_parts(parts: list[str]) -> str:
    return " ".join(part for part in parts if part).strip()


def build_reference_paragraph(data: dict) -> str:
    insured = value(data, "name_of_insured", "the insured")
    damaged = value(data, "items_damaged", "the reported insured property")
    place = value(data, "place_of_loss") or value(data, "insured_property_address")
    cause = value(data, "cause_of_loss", "the reported incident")
    loss_date = value(data, "date_of_loss")
    survey_date = value(data, "survey_date")

    first = (
        f"This is in reference to the appointment as a surveyor for the assessment "
        f"of loss/damage to {damaged} at the premises of {insured} due to {cause}"
    )
    if loss_date:
        first += f" on {loss_date}"
    first += "."

    second = ""
    if survey_date or place:
        second = "We conducted the preliminary survey"
        if survey_date:
            second += f" on {survey_date}"
        if place:
            second += f" at {place}"
        second += (
            " and carried out inspection to verify the nature and extent of the reported damage."
        )

    third = (
        "The preliminary survey report has been prepared based on the available "
        "documents, policy particulars, and the present status of the loss."
    )
    return join_sentence_parts([first, second, third])


def build_incident_narrative(data: dict) -> str:
    insured = value(data, "name_of_insured", "The insured")
    damaged = value(data, "items_damaged", "insured property")
    cause = value(data, "cause_of_loss", "the reported cause of loss")
    loss_date = value(data, "date_of_loss")
    place = value(data, "place_of_loss") or value(data, "insured_property_address")

    text = f"According to the intimation, {insured} suffered loss and damage to {damaged} due to {cause}."
    if loss_date or place:
        text += " The loss"
        if loss_date:
            text += f" occurred on {loss_date}"
        if place:
            text += f" at {place}"
        text += "."
    text += " The present status report records the reported incident and the visible damage for further verification and assessment."
    return text


def build_survey_narrative(data: dict) -> str:
    surveyor = value(data, "surveyor_name", "our insurance surveyor")
    survey_date = value(data, "survey_date")
    place = value(data, "place_of_survey") or value(data, "place_of_loss")
    cause = value(data, "cause_of_loss", "the reported incident")
    damaged = value(data, "items_damaged", "the affected insured property")

    text = f"The field survey has been carried out by {surveyor}"
    if survey_date:
        text += f" on {survey_date}"
    if place:
        text += f" at {place}"
    text += f". During the survey, the site and submitted records indicated damage to {damaged} connected with {cause}."
    text += " The detailed quantity, value, and admissibility of the claimed items remain subject to supporting documents and final verification."
    return text


def build_claim_summary(data: dict) -> str:
    amount = value(data, "estimated_claim_amount")
    cause = value(data, "cause_of_loss", "the reported incident")
    if amount:
        return f"As per our site visit observation, total estimated claim of loss from {cause} on insured property is NRs {amount}."
    return f"As per our site visit observation, the estimated claim of loss from {cause} on insured property is subject to verification from the submitted claim documents."


def build_observation(data: dict) -> str:
    cause = value(data, "cause_of_loss", "the reported incident")
    place = value(data, "place_of_loss") or value(data, "insured_property_address")
    damaged = value(data, "items_damaged", "the reported damaged property")

    text = (
        "We have prepared this status report based on the currently available "
        "documents from the insured and the preliminary survey information."
    )
    details = []
    if cause:
        details.append(f"the cause of loss is recorded as {cause}")
    if place:
        details.append(f"the affected location is {place}")
    if damaged:
        details.append(f"the damaged items presently noted are {damaged}")
    if details:
        text += " At this stage, " + ", ".join(details) + "."
    text += " Further verification may be required to establish exact quantity, value, condition, and policy response before final assessment."
    return text


def build_property_context(data: dict) -> dict[str, str]:
    context = {key: value(data, key) for key in data}
    context.update(
        {
            "submitted_by": value(data, "submitted_by", "Insurance Surveyor"),
            "surveyor_firm": value(data, "surveyor_firm", "Pivot Risk Pvt. Ltd"),
            "enclosed_documents": markdown_bullet_list(data, "enclosed_documents"),
            "reference_paragraph": build_reference_paragraph(data),
            "incident_narrative": build_incident_narrative(data),
            "survey_narrative": build_survey_narrative(data),
            "claim_summary": build_claim_summary(data),
            "observation_narrative": build_observation(data),
            "insured_address": value(data, "insured_company_address") or value(data, "insured_property_address"),
            "sum_insured_machinery_fixed_assets": value(data, "sum_insured_machinery_fixed_assets"),
            "sum_insured_raw_materials_finished_goods": value(data, "sum_insured_raw_materials_finished_goods") or value(data, "breakdown_sum_insured"),
        }
    )
    return context


def fill_estimated_claim_table(document: Document, data: dict) -> None:
    if len(document.tables) < 3:
        return

    claim_rows = parse_estimated_claim_rows(data)
    total = value(data, "estimated_claim_amount")
    total_damaged_quantity = value(data, "total_damaged_quantity")
    table = document.tables[2]
    ensure_table_columns(table, 6)
    ensure_table_rows(table, max(2, len(claim_rows) + 2))
    headers = ["SN", "Item Description", "Invoice Quantity", "Damage Quantity", "Rate", "Amount"]
    for column_index, header in enumerate(headers):
        set_cell_text(table.rows[0].cells[column_index], header)

    for row_index, row_values in enumerate(claim_rows, start=1):
        cells = table.rows[row_index].cells
        for column_index, cell_value in enumerate(row_values[:6]):
            set_cell_text(cells[column_index], cell_value)

    total_row = table.rows[len(claim_rows) + 1]
    set_cell_text(total_row.cells[0], "")
    set_cell_text(total_row.cells[0], "Total")
    set_cell_text(total_row.cells[1], "")
    set_cell_text(total_row.cells[2], "")
    set_cell_text(total_row.cells[3], total_damaged_quantity)
    set_cell_text(total_row.cells[4], "")
    set_cell_text(total_row.cells[5], total)


def fill_property_template(document: Document, data: dict) -> Document:
    if has_placeholders(document):
        replace_placeholders(document, build_property_context(data))
        fill_estimated_claim_table(document, data)
        remove_sample_photo_section(document)
        return document

    paragraphs = document.paragraphs

    paragraph_updates = {
        4: value(data, "name_of_insurer_company"),
        15: value(data, "bank_name"),
        16: f"A/C {value(data, 'name_of_insured')}".strip(),
        17: value(data, "insured_company_address") or value(data, "insured_property_address"),
        18: prefixed("Contact No: ", value(data, "insured_contact_number")),
        21: prefixed("Policy No: ", value(data, "policy_number")),
        22: prefixed("Claim No: ", value(data, "claim_number")),
        23: prefixed("Survey Report No: ", value(data, "survey_report_number")),
        31: f"Date: {value(data, 'report_submission_date')}",
        32: value(data, "name_of_insurer_company"),
        33: value(data, "address_of_insurer_company"),
        34: prefixed("Report No: ", value(data, "survey_report_number")),
        37: build_reference_paragraph(data),
        81: build_incident_narrative(data),
        86: build_survey_narrative(data),
        89: build_claim_summary(data),
        92: build_observation(data),
        28: value(data, "submitted_by", "Insurance Surveyor"),
        29: value(data, "surveyor_firm", "Pivot Risk Pvt. Ltd"),
        30: prefixed("License No: ", value(data, "surveyor_license_number")),
        53: value(data, "surveyor_name"),
        55: prefixed("License No: ", value(data, "surveyor_license_number")),
        96: value(data, "surveyor_firm", "Pivot Risk Pvt. Ltd."),
        97: prefixed("Surveyor License No: ", value(data, "surveyor_license_number")),
    }

    if value(data, "surveyor_name"):
        paragraph_updates[95] = value(data, "surveyor_name")

    for index, text in paragraph_updates.items():
        if index < len(paragraphs):
            set_paragraph_text(paragraphs[index], text)

    if len(document.tables) >= 1:
        fill_key_value_table(
            document.tables[0],
            {
                "Survey Report No": value(data, "survey_report_number"),
                "Policy Type": value(data, "type_of_policy"),
                "Insurer": value(data, "name_of_insurer_company"),
                "Bank": value(data, "bank_name"),
                "Insured": value(data, "name_of_insured"),
                "Claim No.": value(data, "claim_number"),
                "Policy No": value(data, "policy_number"),
                "Policy Issued Date": value(data, "policy_insured_date"),
                "Period of Insurance": value(data, "period_of_insurance"),
                "Total Sum Insured": value(data, "total_sum_insured"),
                "Machinery & Fixed Assets": value(data, "sum_insured_machinery_fixed_assets"),
                "Raw materials  & Water plant,bottle,jar and finished goods": value(data, "sum_insured_raw_materials_finished_goods") or value(data, "breakdown_sum_insured"),
                "Premium Amount": value(data, "premium_amount"),
                "Subject matter Insured": value(data, "subject_matter_insured"),
                "Subject Matter Insured": value(data, "subject_matter_insured"),
                "Owner of Building": value(data, "building_owner"),
                "Type of Building": value(data, "nature_of_building"),
                "Address of Insured Property": value(data, "insured_property_address"),
                "Nature of Insured Property": value(data, "nature_of_insured_property"),
                "Nature of Building": value(data, "nature_of_building"),
            },
        )

    if len(document.tables) >= 2:
        fill_key_value_table(
            document.tables[1],
            {
                "Date of Loss": value(data, "date_of_loss"),
                "Place of Loss": value(data, "place_of_loss"),
                "Insured Location from Policy": value(data, "insured_location_from_policy"),
                "Date of Intimation": value(data, "date_of_intimation"),
                "Date of Deploy/Deputation": value(data, "deputation_date"),
                "Date of Survey": value(data, "survey_date"),
                "Place of Survey": value(data, "place_of_survey"),
                "Cause of loss": value(data, "cause_of_loss"),
            },
        )

    fill_estimated_claim_table(document, data)

    remove_sample_photo_section(document)
    return document


def is_property_template(template_path: Path, case_type: str) -> bool:
    return case_type.lower() == "property" and template_path.exists()


def build_property_template_document(data: dict, template_path: Path) -> Document:
    document = Document(template_path)
    return fill_property_template(document, data)


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

        if line.strip().startswith("<!--"):
            while index < len(lines) and "-->" not in lines[index]:
                index += 1
            index += 1
            continue

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
    current_output_dir = default_current_output_dir()
    input_path = args.input or default_markdown_path(current_output_dir)
    output_path = args.output or default_output_path(current_output_dir)
    template_path = resolve_template(case_dir, args.template)

    case_data = load_case_data(current_output_dir)
    if is_property_template(template_path, args.case_type) and case_data:
        document = build_property_template_document(case_data, template_path)
    else:
        markdown_text = input_path.read_text(encoding="utf-8")
        document = build_document(markdown_text, template_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    saved_path = save_document(document, output_path)
    print(f"Word report saved to: {saved_path}")


if __name__ == "__main__":
    main()
