import argparse
import os
from pathlib import Path

import pypdfium2 as pdfium
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = BASE_DIR / "Working_3" / "current"


def default_input_dir() -> Path:
    return CURRENT_DIR / "input"


def default_output_file() -> Path:
    return CURRENT_DIR / "output" / "output.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run OCR for the current insurance case workspace."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input_dir(),
        help="Folder containing the current case documents.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output_file(),
        help="OCR text output file.",
    )
    return parser.parse_args()


def process_pdf(file_path):
    try:
        pdf = pdfium.PdfDocument(file_path)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

    text = ""

    try:
        for i, page in enumerate(pdf):
            try:
                # Render at 300 DPI for reliable OCR of scanned documents.
                image = page.render(scale=300 / 72).to_pil()
                page_text = pytesseract.image_to_string(image, lang="eng+nep")
                text += f"\n--- Page {i + 1} ---\n"
                text += page_text
            except Exception as e:
                print(f"OCR error on page {i + 1}: {e}")
            finally:
                page.close()
    finally:
        pdf.close()

    return text


def process_image(file_path):
    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image, lang="eng+nep")
    except Exception as e:
        print(f"Error processing image {file_path}: {e}")
        return ""


def get_doc_type(filename):
    name = filename.lower()

    if "claim" in name:
        return "Claim Form"
    if "deputation" in name:
        return "Deputation"
    if "police" in name:
        return "Police Report"
    if "policy" in name:
        return "Policy Document"
    if "quotation" in name:
        return "Quotation"
    if "agreement" in name:
        return "Written Agreement"
    return "Unknown Document"


def main():
    args = parse_args()
    input_folder = args.input
    output_file = args.output

    if not input_folder.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    all_text = ""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for file in os.listdir(input_folder):
        file_path = input_folder / file
        doc_type = get_doc_type(file)

        if file.lower().endswith(".pdf"):
            print(f"Processing PDF: {file}")
            document_text = process_pdf(file_path)
            if document_text.strip():
                all_text += f"\n\n===== DOCUMENT: {doc_type} ({file}) =====\n"
                all_text += document_text
        elif file.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing Image: {file}")
            document_text = process_image(file_path)
            if document_text.strip():
                all_text += f"\n\n===== DOCUMENT: {doc_type} ({file}) =====\n"
                all_text += document_text
        else:
            print(f"Skipping unsupported file: {file}")

    if not all_text.strip():
        raise RuntimeError(
            "OCR produced no text. Check the input files and the errors shown above."
        )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_text)

    print("\nOCR completed for all files.")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    main()
