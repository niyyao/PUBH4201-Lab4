# AI Usage

## Tool used


Chat GPT (GPT-6.1 Sol)


## How it Helped

ChatGPT helped me write the SQL scripts for counting mutations per patient and gene and counting patients by tissue source site and tumor stage.



## How I checked the results

I verified the number of patient-gene rows to be 2,830 rows for 566 patients and 5 genes. I verified that the 12 Silent entries in 758 target-gene mutation records left 746 counted mutations. The site-stage query returned 142 rows as expected, with total patients of 566, with all 54 patients with missing stage. I also matched the individual mutation records of patient TCGA-05-4244 with the feature table; one KRAS Missense_Mutation (p.G12C) was found to match KRAS_count = 1 with count = 0 for other four genes. The validation results have been stored in validation_results.txt and patient_check.txt.

In the scripts I also added assertions for key checks. It is saved and the validation_results.txt is for where validation results can be found and patient_check.txt is where individual patient comparisons can be found.
