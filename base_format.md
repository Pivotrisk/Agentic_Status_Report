# Status Report Format

This format is based on your required structure and should be filled primarily from `output/data.json`.

Where a placeholder is not part of the current JSON schema, keep it blank or complete it manually after review.

## Cover Page

# Status Survey Report

**Private and Confidential**

**Submitted to**  
`{{name_of_insurer_company}}`  

**Property Survey Report**
**Insured**
- Type of policy: `{{type_of_policy}}`
- Insured: `{{bank_name}}`
- Account / insured entity: `{{name_of_insured}}`
- Insured address: `{{insured_company_address}}`
- Contact number: `{{insured_contact_number}}`


## Case Identity

- Policy number: `{{policy_number}}`
- Claim number: `{{claim_number}}`
- Survey report number: `{{survey_report_number}}`
- Status: Status report

## Surveyor Identity

- Submitted by: `{{submitted_by}}`
- Surveyor / surveyor firm: `{{surveyor_firm}}`
- Surveyor name: `{{surveyor_name}}`
- Surveyor license number: `{{surveyor_license_number}}`


## Submission Letter
- Date of report submission: `{{report_submission_date}}`
**To:** `{{name_of_insurer_company}}`  
**Report No.:** `{{survey_report_number}}`

Dear Sir / Madam,

This report is submitted in reference to the appointment of the surveyor for the assessment of loss or damage affecting `{{name_of_insured}}` at `{{place_of_loss}}` under policy number `{{policy_number}}` and claim number `{{claim_number}}`.

The reported cause of loss is `{{cause_of_loss}}`. The loss is reported to have occurred on `{{date_of_loss}}`, and the survey activities are connected with deputation date `{{deputation_date}}` and survey date `{{survey_date}}`.

The presently reported damaged items include:

`{{items_damaged}}`

The survey report is submitted for your kind perusal and necessary action.


## Enclosed Documents

- `{{enclosed_document_1}}`
- `{{enclosed_document_2}}`
- `{{enclosed_document_3}}`
- `{{enclosed_document_4}}`
- `{{enclosed_document_5}}`
- `{{enclosed_document_6}}`

Yours faithfully,  
`{{surveyor_name}}`  
`{{surveyor_firm}}`


**PROPERTY SURVEY REPORT**
(PRIVATE & CONFIDENTIAL)
The report is issued by Pivot Risk Pvt. Ltd, a loss assessor without prejudice in respect of cause, nature, and extent of loss/damage strictly subjected to the terms and conditions of the insurance policy.

## 1. Insurance Policy Details
Table 1: Insurance Policy Details

| Particulars | Details |
| --- | --- |
| Survey Report No. | `{{survey_report_number}}` |
| Policy Type | `{{type_of_policy}}` |
| Insurer | `{{name_of_insurer_company}}` |
| Bank | `{{bank_name}}` |
| Insured | `{{name_of_insured}}` |
| Claim No. | `{{claim_number}}` |
| Policy No. | `{{policy_number}}` |
| Policy Issued Date | `{{policy_insured_date}}` |
| Period of Insurance | `{{period_of_insurance}}` |
| Total Sum Insured | `{{total_sum_insured}}` |
| Machinery & Fixed Assets | `{{sum_insured_machinery_fixed_assets}}` |
| Raw materials & Water plant, bottle, jar and finished goods | `{{sum_insured_raw_materials_finished_goods}}` |
| Premium Amount | `{{premium_amount}}` |
| Subject Matter Insured | `{{subject_matter_insured}}` |
| Address of Insured Property | `{{insured_property_address}}` |
| Nature of Insured Property | `{{nature_of_insured_property}}` |
| Nature of Building | `{{nature_of_building}}` |


## 2. Incident Details

Table 2: Incident Details

| Particulars | Details |
| --- | --- |
| Date of Loss | `{{date_of_loss}}` |
| Place of Loss | `{{place_of_loss}}` |
| Date of Deploy/Deputation | `{{deputation_date}}` |
| Date of Survey | `{{survey_date}}` |
| Place of Survey | `{{place_of_survey}}` |
| Cause of Loss | `{{cause_of_loss}}` |


## 3. CAUSE & NATURE OF INCIDENT

According to the intimation, `{{name_of_insured}}`, suffered loss and damage to various items such as `{{items_damaged}}` due to `{{cause_of_loss}}`. The loss occurred on `{{date_of_loss}}` at the location `{{insured_property_address}}` / `{{place_of_loss}}`.

As a result, `{{incident_effect_summary}}`

Note:
This section should not be treated as a simple placeholder replacement only. It should be written as a short explanatory narrative using the OCR facts, with professional insurance-report wording. The final text should explain what happened, where it happened, what was damaged, and the practical effect of the incident.


## 4. Spot and Preliminary Survey Details

The field survey has been carried out by our insurance surveyor `{{surveyor_name}}` on `{{survey_date}}` at `{{place_of_survey}}`. During the survey, the site showed damage caused by `{{cause_of_loss}}`.

Site observations:

`{{spot_survey_observation}}`

Note:
This section should describe the field visit in clear report language. Even if some inputs are missing, the narrative should summarize the visible condition of the site, the type of damage observed, and any practical survey findings that are reasonably supported by the OCR text.


## 5. Estimated Claim From insured

As per our site visit observation, the total estimated claim of loss on the insured property is `{{estimated_claim_amount}}`.



## 6. Observation

This status report is prepared based on the documents presently available from the insured and other related records.

The cause of loss is presently identified as `{{cause_of_loss}}`. The damaged items currently noted are `{{items_damaged}}`.

The insured property is situated at `{{insured_property_address}}`, and the incident location is recorded as `{{place_of_loss}}`.

Further verification may be required to establish the exact quantity, value, and condition of the damaged property and to support final assessment.

Note:
This section should read like a concluding observation, not just a list of fields. It should briefly explain the present status of the case, what is currently supported by the available documents, and what may still require verification or follow-up.


- Prepared by: `{{submitted_by}}`
- Surveyor / surveyor firm: `{{surveyor_firm}}`
- Surveyor name: `{{surveyor_name}}`
- Surveyor license number: `{{surveyor_license_number}}`

## Notes On Placeholders

These placeholders are already part of the current JSON schema:

- `{{name_of_insurer_company}}`
- `{{type_of_policy}}`
- `{{name_of_insured}}`
- `{{bank_name}}`
- `{{insured_company_address}}`
- `{{insured_contact_number}}`
- `{{policy_number}}`
- `{{claim_number}}`
- `{{policy_insured_date}}`
- `{{period_of_insurance}}`
- `{{total_sum_insured}}`
- `{{premium_amount}}`
- `{{subject_matter_insured}}`
- `{{insured_property_address}}`
- `{{nature_of_insured_property}}`
- `{{nature_of_building}}`
- `{{date_of_loss}}`
- `{{place_of_loss}}`
- `{{deputation_date}}`
- `{{survey_date}}`
- `{{place_of_survey}}`
- `{{cause_of_loss}}`
- `{{items_damaged}}`
- `{{surveyor_name}}`

These placeholders are not in the current JSON schema yet and may need manual completion or future schema expansion:

- `{{survey_report_number}}`
- `{{submitted_by}}`
- `{{surveyor_firm}}`
- `{{surveyor_license_number}}`
- `{{report_submission_date}}`
- `{{enclosed_document_1}}` to `{{enclosed_document_6}}`
- `{{sum_insured_machinery_fixed_assets}}`
- `{{sum_insured_raw_materials_finished_goods}}`
- `{{incident_effect_summary}}`
- `{{spot_survey_observation}}`
- `{{estimated_claim_amount}}`

## Narrative Guidance

Sections 3, 4, and 6 require explanation, reasoning, and report-style writing.

- Section 3 should explain the cause and nature of the incident in a compact factual paragraph.
- Section 4 should explain the survey visit and the main visible observations from the site.
- Section 6 should summarize the current assessment status and any need for further verification.

These sections should be generated from the OCR content and extracted facts, even when the exact sentences do not already exist in the JSON file.
