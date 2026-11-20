# Marine Case Type

This folder contains the marine insurance preliminary survey workflow assets.

Included now:

- `format/marine_template.md` synchronized with the updated `format/marine_template.docx` status survey report.
- `fields.json` with marine extraction fields, including dynamic Markdown table rows for imported goods.
- `examples/example_output.md` converted from the Him Electronics marine report and trimmed to preliminary-report scope.
- `examples/FInal of Him Electronic.docx` as the original Word reference.

The marine format adds voyage, cargo, invoice, declaration, customs, consignment, package, and transit details. It intentionally excludes final loss assessment, salvage computation, deductible computation, insurer liability recommendation, net payable amount, and proforma invoice / professional fee sections.

For Table 3, `imported_goods_table_rows` should be extracted from each case's OCR/output text and saved as Markdown table rows in `data.json`.
