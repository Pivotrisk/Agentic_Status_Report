You are working inside my project workspace. Continue the marine insurance preliminary survey workflow using the OCR text that already exists in the current working case folder.

Default case type: `marine`
Default OCR path: `Working_3/current_output/ocr_output.txt`

Do not try to run `Working_3/ocr.py` in this prompt. Assume OCR has already been run manually for the current case.

Your job is to do all of the following in order:

1. Read the OCR output from `Working_3/current_output/ocr_output.txt` unless the user gives another path.
2. If the OCR file does not exist or is empty, stop and clearly tell the user to place documents in `Working_3/current_input/` and run `python Working_3/ocr.py` or `py Working_3/ocr.py` first.
3. Use these reference files to understand the expected marine case structure and report style:
   - `Working_3/case_types/marine/examples/` as sample marine case documents and reference output
   - `Working_3/case_types/marine/examples/example_output.md` as the sample marine preliminary report
   - `Working_3/case_types/marine/format/marine_template.md` as the canonical marine report template
   - `Working_3/case_types/marine/fields.json` as the extraction schema
4. Extract structured data from the OCR text and create one valid JSON object using exactly the fields listed in `Working_3/case_types/marine/fields.json`.
5. Save that JSON to `Working_3/current_output/data.json`.
6. Read `Working_3/case_types/marine/format/marine_template.md` and fill its placeholders using the values from `Working_3/current_output/data.json`.
7. While filling the selected format template, treat sections 3 `Causes Of Loss`, 7 `Brief Description Of Damage Site And Detail Of Loss`, and 9 `Observation` as narrative sections. For those sections, do not only substitute placeholders. Write short professional marine survey-report prose using the OCR text, the extracted JSON facts, and reasonable document-supported inference.
8. Replace the `cargo_*` sample row with the resulting rows. For Table 3 `Imported Goods as per Export Invoice`, populate `imported_goods_table_rows` dynamically from the OCR text. Include every item found in the export invoice/imported goods table. If the case has 49 cargo rows, write 49 Markdown table rows. Do not include the table header, separator, or total row inside `imported_goods_table_rows`.
9. Replace the `claim_*` sample row with the resulting rows. For Table 6 `Estimated Claim Of Loss`, populate `estimated_claim_table_rows` dynamically from the OCR text. Include every damaged/claimed item found in the estimated claim table. Do not include the table header, separator, or total row inside `estimated_claim_table_rows`.
10. Create the final report in markdown and save it to `Working_3/current_output/<name_of_insured>_status_report.md`, using a lowercase underscore slug of `name_of_insured` for the filename. Example: `Working_3/current_output/him_electronics_pvt_ltd_status_report.md`.
11. If Python execution is available in this session, run `Working_3/archive_case.py --case-type marine` so the current case is preserved in its own folder inside `Working_3/case_types/marine/archive_cases/` without overwriting previous cases.
12. If Python execution is not available, clearly tell the user to run `python Working_3/archive_case.py --case-type marine` or `py Working_3/archive_case.py --case-type marine` manually after reviewing the report.

Rules for extraction:

- Return one JSON object only for the data extraction step.
- Use exactly the field names listed in `Working_3/case_types/marine/fields.json`.
- If a value is not found, use `""`.
- Do not hallucinate.
- Prefer exact values from the documents.
- If OCR is noisy, infer carefully only when the intended value is still clear from context.
- Preserve numbers, policy numbers, claim numbers, endorsement numbers, declaration numbers, invoice numbers, consignment numbers, dates, and addresses as accurately as possible.
- For IRD fields, use verified IRD/PAN lookup information only. If IRD data is not available in the current context, leave the `ird_*` fields blank rather than guessing.
- For `imported_goods_table_rows`, output Markdown rows in this form:
  `| SN | Goods Description | Specification | HSN Code | Quantity | Rate | Amount |`
- For `estimated_claim_table_rows`, output Markdown rows in this form:
  `| SN | Item Description | Invoice Quantity | Damage Quantity | Rate | Amount |`

Rules for report generation:

- Follow `Working_3/case_types/marine/format/marine_template.md` closely.
- Keep the report professional and clean.
- Do not invent missing facts.
- If a placeholder maps to a current JSON field, fill it from `Working_3/current_output/data.json`.
- If a placeholder is not supported by the current JSON schema, leave it blank or keep it for manual completion.
- Preserve the existing structure of the selected marine format template and do not rewrite it into a different report style.
- Do not include final loss assessment, salvage computation, deductible computation, insurer liability recommendation, net payable amount, or proforma invoice / professional fee sections in the preliminary report.
- Dynamic table row placeholders must expand as Markdown table rows, not as inline code.
- In narrative sections, rely first on OCR text and extracted facts, and only make careful, limited inferences that are strongly supported by the documents.
- Do not produce generic filler language. The narrative should stay case-specific.

Required outputs:

- `Working_3/current_output/data.json`
- `Working_3/current_output/<name_of_insured>_status_report.md`
- one archived case folder inside `Working_3/case_types/marine/archive_cases/` if Python execution is available in the session

At the end, briefly confirm what files were created or updated.
