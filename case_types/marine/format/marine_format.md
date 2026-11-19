# Preliminary Marine Insurance Survey Report Format

This format is based on `Working_3/base_format.md` and the marine example report in `Working_3/case_types/marine/examples/example_output.md`.

Where a placeholder is not part of the current JSON schema, keep it blank or complete it manually after review.

## Cover Page

# Preliminary Marine Insurance Survey Report

**Private and Confidential**

**Submitted to**  
`{{name_of_insurer_company}}`

**Marine Insurance Survey Report**

## Insured

- `{{name_of_insured}}`
- `{{insured_company_address}}`
- Contact number: `{{insured_contact_number}}`
- Policy number: `{{policy_number}}`
- Endorsement number: `{{endorsement_number}}`
- Survey report number: `{{survey_report_number}}`
- Status of report: Payable

## Surveyor Identity

- Submitted by: 
- `{{surveyor_firm}}`
- Insurance surveyor
- License number: 679/071/072 

## Submission Letter

**Date:** {today's date}
**To:** `{{name_of_insurer_company}}`  
**Address:** `{{address_of_insurer_company}}`  
**Report No.:** `{{survey_report_number}}`

Dear Sir / Madam,

This report is submitted in reference to the appointment of the surveyor for preliminary verification of loss or damage to `{{subject_matter_insured}}` belonging to `{{name_of_insured}}` under policy number `{{policy_number}}` and claim number `{{claim_number}}`.

The reported loss occurred on `{{date_of_loss}}` during transit from `{{voyage_from}}` to `{{voyage_to}}` by `{{mode_of_transit}}`. The presently reported cause of loss is `{{cause_of_loss}}`, and the survey activities are connected with deputation date `{{deputation_date}}` and survey date `{{survey_date}}`.

The presently reported damaged cargo / items include:

`{{items_damaged}}`

This preliminary survey report is submitted for your kind perusal and necessary action, subject to detailed verification of documents, cargo condition, policy terms, and final assessment.

## Enclosed Documents

- `{{enclosed_document_1}}`
- `{{enclosed_document_2}}`
- `{{enclosed_document_3}}`
- `{{enclosed_document_4}}`
- `{{enclosed_document_5}}`
- `{{enclosed_document_6}}`
- `{{enclosed_document_7}}`
- `{{enclosed_document_8}}`
- `{{enclosed_document_9}}`
- `{{enclosed_document_10}}`
- `{{enclosed_document_11}}`
- `{{enclosed_document_12}}`
- `{{enclosed_document_13}}`
- `{{enclosed_document_14}}`
- `{{enclosed_document_15}}`
- `{{enclosed_document_16}}`
- `{{enclosed_document_17}}`
- `{{enclosed_document_18}}`
- `{{additional_enclosed_documents}}`

Yours faithfully,  
`{{surveyor_name}}`
Insurance surveyor  
`{{surveyor_firm}}`

## Detail Description Of The Marine Insurance Survey

**Private and Confidential**

This report is issued by Pivot Risk Pvt. Ltd, a loss assessor, without prejudice in respect of cause, nature, and extent of loss/damage and strictly subjected to the terms and conditions of the insurance policy.

## 1. Insurance Policy Details

Table 1: Policy Details

| Particulars | Details |
| --- | --- |
| Survey Report No. | `{{survey_report_number}}` |
| Insurer | `{{name_of_insurer_company}}` |
| Type of Policy | `{{type_of_policy}}` |
| Insured | `{{name_of_insured}}` |
| Bank / Account | `{{bank_name}}` |
| Policy No. | `{{policy_number}}` |
| Claim No. | `{{claim_number}}` |
| Endorsement No. | `{{endorsement_number}}` |
| Policy Issued Date | `{{policy_insured_date}}` |
| Period of Insurance | `{{period_of_insurance}}` |
| Export Invoice No. and Date | `{{invoice_number_and_date}}` |
| Declaration No. | `{{declaration_number}}` |
| Total Sum Insured | `{{total_sum_insured}}` |
| Declared Value | `{{declared_value}}` |
| Premium Amount | `{{premium_amount}}` |
| Exchange Rate | `{{exchange_rate}}` |
| Voyage From | `{{voyage_from}}` |
| Voyage To | `{{voyage_to}}` |
| Mode of Transit | `{{mode_of_transit}}` |
| Subject Matter Insured | `{{subject_matter_insured}}` |
| Basis of Valuation | `{{basis_of_valuation}}` |
| Deductible Excess | `{{deductible_excess}}` |
| Policy Clauses | `{{policy_clauses}}` |
| Clause | `{{clause}}` |
| PAN of Insured | `{{insured_pan}}` |

## 2. SPOT SURVEY OBSERVATION

### 2.1 PARTICULARS OF SURVEY

Table 2: Survey Details

| Particulars | Details |
| --- | --- |
| Date of loss | `{{date_of_loss}}` |
| Place of loss | `{{place_of_loss}}` |
| Date of Intimation | `{{intimation_date}}` |
| Date of Deputation | `{{deputation_date}}` |
| Date of survey | `{{survey_date}}` |
| Place of survey | `{{place_of_survey}}` |

## 3. Cause And Nature Of Loss

According to the intimation and available documents, `{{name_of_insured}}` reported loss/damage to `{{subject_matter_insured}}` during transit from `{{voyage_from}}` to `{{voyage_to}}`. The reported cause of loss is `{{cause_of_loss}}`, and the damaged cargo / items presently noted are `{{items_damaged}}`.

`{{cause_and_nature_narrative}}`

Note:
This section should be written as a marine-cargo narrative. It should explain the transit route, vehicle/vessel or consignment details where available, how the damage was noticed, what cargo was affected, and what initial cause is supported by the documents.

## 4. Inland Cargo Details

Table 3: Imported Goods as per Export Invoice `{{invoice_number_and_date}}`

| SN | Goods Description | Specification | HSN Code | Quantity | Rate | Amount |
| --- | --- | --- | --- | --- | --- | --- |
{{imported_goods_table_rows}}
| Total |  |  |  | `{{total_quantity}}` |  | `{{invoice_value}}` |

## 5. Base Information on Cargo

Table 4: Cargo Details

| Section | Code | Particulars | Details |
| --- | --- | --- | --- |
| 1 |  | Details of consignee |  |
|  | A | Name of consignee | `{{consignee_name}}` |
|  | B | Name of Exporter | `{{exporter_name}}` |
|  | C | Proforma Invoice No and Date | `{{proforma_invoice_number_and_date}}` |
|  | D | Commercial Invoice No and Date | `{{invoice_number_and_date}}` |
|  | E | Exim Code | `{{exim_code}}` |
|  | F | PAN of Insured | `{{insured_pan}}` |
|  | G | Country of Origin | `{{country_of_origin}}` |
|  | H | Country of Destinations | `{{country_of_destination}}` |
|  | I | Delivery Terms and Place | `{{delivery_terms_and_place}}` |
|  | J | Place of Final Destination | `{{final_destination}}` |
|  | K | Harmonic Code | `{{commodity_or_hsn_code}}` |
|  | L | Descriptions of Goods | `{{goods_description}}` |
|  | M | Total Qty | `{{total_quantity}}` |
|  | N | Rate(INR) | `{{rate_range}}` |
|  | O | Total Amount of Value (INR) | `{{invoice_value}}` |
|  | P | Terms of Payment | `{{terms_of_payment}}` |
|  | Q | Gross Weight (KG) | `{{gross_weight}}` |
|  | R | Net Weight (KG) | `{{net_weight}}` |
|  | S | Total Volume | `{{total_volume}}` |
|  | T | Packing | `{{packing_details}}` |
|  | U | Pre-Carriage By | `{{pre_carriage_by}}` |
|  | V | GSTIN | `{{gstin}}` |
|  | W | Place of Loading | `{{place_of_loading}}` |
|  | X | If goods are transshipped, Name of original vehicle | `{{original_vehicle_if_transshipped}}` |
|  | Y | Term of Payment | `{{terms_of_payment}}` |
|  | Z | Custom Entry Point | `{{customs_entry_point}}` |
| 2 |  | Bill of Lading / Consignment Details |  |
|  | AA | Consignment Number and Date | `{{consignment_number_and_date}}` |
|  | AB | Number and Type of Package | `{{number_and_type_of_packages}}` |
|  | AC | Total Value of the Consignment | `{{total_consignment_value}}` |
|  | AD | Commodity/Harmonic Code | `{{commodity_or_hsn_code}}` |
|  | AE | Total Quantity of Goods | `{{total_quantity}}` |
|  | AF | Items Name | `{{goods_description}}` |
|  | AG | Container No | `{{container_number}}` |
|  | AH | Transporter | `{{transporter_name}}` |
|  | AI | Truck No | `{{truck_number}}` |
|  | AJ | Reporting Date and Time | `{{reporting_date_and_time}}` |
|  | AK | PAN | `{{insured_pan}}` |
|  | AL | L/C No and Date | `{{lc_number_and_date}}` |
|  | AM | Place and Date of Issue | `{{place_and_date_of_issue}}` |
|  | AN | Consignment ID No | `{{consignment_id}}` |
| 3 |  | Pragyapan Patra |  |
|  | A | Custom Office | `{{customs_office}}` |
|  | B | Custom Reference No and Date | `{{customs_reference_number_and_date}}` |
|  | C | Declarant Reference No | `{{declarant_reference_number}}` |
|  | D | Invoice No and Date | `{{invoice_number_and_date}}` |
|  | E | Declarant/Agent/Representative | `{{customs_agent_or_representative}}` |
|  | F | Country of Origin and Export | `{{country_of_origin_and_export}}` |
|  | G | Vehicle No. | `{{vehicle_or_container_number}}` |
|  | H | Delivery Terms and Place | `{{delivery_terms_and_place}}` |
|  | I | Total Amount of Value | `{{invoice_value}}` |
|  | J | Name of Items | `{{name_of_items}}` |
|  | K | Terms of Payment | `{{terms_of_payment}}` |
|  | L | Place of Destination | `{{final_destination}}` |
|  | M | Location of Goods | `{{location_of_goods}}` |
|  | N | Office of Entry and Exit | `{{office_of_entry_and_exit}}` |
|  | O | Statistical Value | `{{statistical_value}}` |
|  | P | Import Duty | `{{import_duty}}` |
|  | Q | ECS | `{{ecs_details}}` |
|  | R | VAT | `{{vat_details}}` |
| 4 |  | Survey Details |  |
|  | A | Name of Applicant for survey | `{{survey_applicant_name}}` |
|  | B | Date of Applicant for Survey | `{{survey_application_date}}` |
|  | C | Date and place of a survey held | `{{survey_held_date_and_place}}` |
|  | D | Delay if any, in applying for the survey due to | `{{delay_in_applying_for_survey}}` |
|  | E | The external condition of packages at the time of the survey | `{{external_condition_of_packages}}` |
|  | F | New or second hand | `{{new_or_second_hand}}` |
|  | G | Cause, After Examination Attributed by the surveyor | `{{cause_attributed_by_surveyor}}` |
|  | H | Nature of Packages | `{{nature_of_packages}}` |
|  | I | Condition of goods at that time | `{{condition_of_goods}}` |
|  | J | Date of Delivery of goods into warehouse or other places where survey held | `{{goods_delivery_date_to_survey_place}}` |
|  | K | Delay if any, in clearance and/or forwarding of goods to destination | `{{delay_in_clearance_or_forwarding}}` |
|  | L | Rate of Exchange | `{{exchange_rate}}` |

## 6. REGISTRATION DETAILS OF THE COMPANY

Company Name: `{{name_of_insured}}`  
Company Address: `{{insured_company_address}}`

Table 5: Company Details from IRD

| PAN Detail |  |  |
| --- | --- | --- |
| PAN | `{{ird_pan}}` |  |
| Name (Eng.) | `{{ird_name_english}}` |  |
| Name (Nep) | `{{ird_name_nepali}}` |  |
| Address | `{{ird_address}}` |  |
| Ward | `{{ird_ward}}` |  |
| Phone | `{{ird_phone}}` |  |
| Office | `{{ird_office}}` |  |
| Effective Registration Date | `{{ird_effective_registration_date}}` |  |
| Business Details |  |  |
| Trade Name (Eng.) | Trade Name (Nep) | Main Business |
| `{{ird_trade_name_english}}` | `{{ird_trade_name_nepali}}` | `{{ird_main_business}}` |

## 7. Brief Description Of Damage Site And Detail Of Loss

As per the available documents and preliminary survey, the reported damage occurred to `{{subject_matter_insured}}` during transit. The damaged goods / packages were observed at `{{place_of_survey}}`.

`{{damage_site_and_loss_details}}`

Note:
This section should summarize the physical condition of the packages and goods, visible damage, segregation or opening of packages, damaged quantity where available, and any immediate action taken by the insured.

## 8. Estimated Claim From Insured

As per the documents submitted by the insured, the estimated claim of loss is `{{estimated_claim_amount}}`.

Table 6: Estimated Claim Of Loss

| SN | Item Description | Invoice Quantity | Damage Quantity | Rate | Amount |
| --- | --- | --- | --- | --- | --- |
{{estimated_claim_table_rows}}
| Total |  |  | `{{total_damaged_quantity}}` |  | `{{estimated_claim_amount}}` |

## 9. Observation

This preliminary survey report is prepared based on the documents presently available from the insured and other related records.

The reported cause of loss is presently identified as `{{cause_of_loss}}`. The damaged cargo / items currently noted are `{{items_damaged}}`. The consignment details presently available include invoice `{{invoice_number_and_date}}`, consignment `{{consignment_number_and_date}}`, and transit route from `{{voyage_from}}` to `{{voyage_to}}`.

Further verification may be required to establish the exact quantity, value, admissibility, salvage position, policy excess, and final liability under the policy.

`{{observation_narrative}}`

Note:
This section should read like a concluding preliminary observation. It should avoid final liability language and should not include assessment of loss, salvage computation, deductible computation, or net payable amount.

## 10. Remarks On Submission Of Report

This preliminary report is submitted after review of the documents and preliminary survey work completed up to `{{report_submission_date}}`. The report is issued without prejudice and remains subject to terms and conditions of the policy and further verification.

## 11. Conclusion

The above information is complete to the best of our knowledge and belief based on the documents and information presently provided by the insured. The findings remain subject to further verification and insurance policy terms.

## 12. Remarks

This preliminary survey report is prepared for `{{name_of_insurer_company}}` and should not be used in any other circumstances.

The copies of legal and supporting documents provided by the insured are assumed to be true, correct, and not manipulated. If there is any manipulation in the documents provided by the insured, the surveyor is not liable for outcomes, discrepancies, or legal problems arising from such manipulated documents.

The observations are based on facts and assumptions identified in this report. No important factors have been intentionally overlooked or withheld.

- Prepared by: `{{submitted_by}}`
- Surveyor / surveyor firm: `{{surveyor_firm}}`
- Surveyor name: `{{surveyor_name}}`
- Surveyor license number: `{{surveyor_license_number}}`

## Notes On Marine Placeholders

Core placeholders already overlap with the current property schema:

- `{{name_of_insurer_company}}`
- `{{address_of_insurer_company}}`
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
- `{{endorsement_number}}`
- `{{cause_of_loss}}`
- `{{items_damaged}}`
- `{{deputation_date}}`
- `{{survey_date}}`
- `{{premium_amount}}`
- `{{subject_matter_insured}}`
- `{{date_of_loss}}`
- `{{place_of_loss}}`
- `{{place_of_survey}}`
- `{{surveyor_name}}`

Marine-specific placeholders likely need schema support:

- `{{survey_report_number}}`
- `{{submitted_by}}`
- `{{surveyor_firm}}`
- `{{surveyor_license_number}}`
- `{{report_submission_date}}`
- `{{declared_value}}`
- `{{basis_of_valuation}}`
- `{{deductible_excess}}`
- `{{policy_clauses}}`
- `{{declaration_number}}`
- `{{invoice_number_and_date}}`
- `{{invoice_value}}`
- `{{exchange_rate}}`
- `{{voyage_from}}`
- `{{voyage_to}}`
- `{{country_of_origin}}`
- `{{country_of_destination}}`
- `{{mode_of_transit}}`
- `{{place_of_loading}}`
- `{{final_destination}}`
- `{{delivery_terms}}`
- `{{terms_of_payment}}`
- `{{lc_number_and_date}}`
- `{{intimation_date}}`
- `{{external_condition_of_packages}}`
- `{{condition_of_goods}}`
- `{{delay_in_clearance_or_forwarding}}`
- `{{consignee_name}}`
- `{{exporter_name}}`
- `{{consignment_number_and_date}}`
- `{{number_and_type_of_packages}}`
- `{{total_quantity}}`
- `{{gross_weight}}`
- `{{net_weight}}`
- `{{packing_details}}`
- `{{commodity_or_hsn_code}}`
- `{{goods_description}}`
- `{{vehicle_or_container_number}}`
- `{{transporter_name}}`
- `{{consignment_id}}`
- `{{imported_goods_table_rows}}`
- `{{customs_office}}`
- `{{customs_reference_number_and_date}}`
- `{{declarant_reference_number}}`
- `{{customs_agent_or_representative}}`
- `{{customs_entry_point}}`
- `{{office_of_entry_and_exit}}`
- `{{location_of_goods}}`
- `{{import_duty_tax_details}}`
- `{{insured_pan}}`
- `{{exim_code}}`
- `{{estimated_claim_amount}}`
- `{{total_damaged_quantity}}`

## Narrative Guidance

Sections 3, 7, and 9 require explanation, reasoning, and report-style writing. Section 4 also requires dynamic table extraction from the case OCR/output text.

- Section 3 should explain the marine transit route, reported incident, damaged cargo, and apparent cause.
- Section 4 should populate `{{imported_goods_table_rows}}` with every cargo item found in the export invoice/imported goods table for the current case. Do not limit it to three sample rows; if the invoice has 49 items, write 49 rows.
- Section 7 should explain the physical survey observations, damaged packages/goods, and available damage quantity.
- Section 9 should summarize the preliminary position and further verification required.

This marine preliminary format intentionally excludes final loss assessment, salvage computation, deductible computation, insurer liability recommendation, net payable amount, and proforma invoice / professional fee sections.
