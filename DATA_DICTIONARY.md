# Feature Table Data Dictionary

The feature table contains one row per patient (566 rows).
NA indicates a value was not recorded. Missing clinical values were
retained without imputation.

| Column | Meaning | Units | Source | Missing-value coding |
|---|---|---|---|---|
| patient_id | Unique patient identifier | Not applicable | patients.patient_id | None; required unique identifier |
| sex | Recorded patient sex | Categorical | patients.sex | NA; 52 missing |
| age_at_diagnosis | Age when diagnosed | Years | patients.age_at_diagnosis | NA; 71 missing |
| stage | Recorded tumor stage | Categorical | patients.stage | NA; 54 missing |
| tissue_source_site | Site that supplied the tissue sample | Categorical | samples.tissue_source_site, linked through patient_id | NA if unrecorded; none missing here |
| tmb_nonsynonymous | Nonsynonymous tumor mutation burden | Mutations per megabase | samples.tmb_nonsynonymous, linked through patient_id | NA if unrecorded; none missing here |
| TP53_count | Number of qualifying TP53 mutation records for the patient | Mutation records | mutations, linked through samples | 0 if no qualifying record; no NA |
| KRAS_count | Number of qualifying KRAS mutation records for the patient | Mutation records | mutations, linked through samples | 0 if no qualifying record; no NA |
| EGFR_count | Number of qualifying EGFR mutation records for the patient | Mutation records | mutations, linked through samples | 0 if no qualifying record; no NA |
| STK11_count | Number of qualifying STK11 mutation records for the patient | Mutation records | mutations, linked through samples | 0 if no qualifying record; no NA |
| KEAP1_count | Number of qualifying KEAP1 mutation records for the patient | Mutation records | mutations, linked through samples | 0 if no qualifying record; no NA |

## Mutation-count definition

Atfer excluding silent mutations, the five gene columns only include records where variant_classification != 'Silent'.

The included classifications are: Missense_Mutation, Nonsense_Mutation, Frame_Shift_Del, Splice_Site, In_Frame_Del, Frame_Shift_Ins, and In_Frame_Ins.

Silent records are not counted. There were no missing classifications found for any records from these five genes. SQL comparisons also exclude any NULL classifications.

A count of 0 means there was not one mutation record found for the database provided. This includes samples that did not have any mutation calls at all; it does not mean the gene is mutation free in biology or that coverage was sufficient. NA in the clinical column means that the clinical value was not provided.
