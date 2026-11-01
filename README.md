# Course:PUBH 4201 — Lab 4-database-feature-table

In lab 4 it uses SQL and Python to create patient-level feature table

Using real data from TCGA Lung Adenocarcinoma PanCancer Atlas study.

## How to reproduce this analysis from scratch

1. Clone the repo and enter the project folder:

   ```bash
   git clone https://github.com/niyyao/PUBH4201-Lab4.git
   cd PUBH4201-Lab4
   ```

2. Activate the proper python environment:

   ```bash
   conda env create -f environment.yml
   conda activate lab4
   ```

3. Download this database:

   ```bash
   mkdir -p data
   curl -fL "https://raw.githubusercontent.com/gwcbi/applied-computing-HDS/main/data/raw/lab4-cbioportal-luad/cohort.db" -o data/cohort.db
   ```

4. Run analysis:

   ```bash
   python build_features.py
   ```

5. Make sure it compeltes without errors and reports 566 patients before and after the joins. should generate `feature_table.tsv`, `site_stage_counts.tsv`, and `validation_results.txt`.

## DATA SOURCE

The database is not from here and it was downloaded from the course repo:

https://raw.githubusercontent.com/gwcbi/applied-computing-HDS/main/data/raw/lab4-cbioportal-luad/cohort.db

The provided database was built from the TCGA Lung Adenocarcinoma PanCancer Atlas study available through cBioPortal:

https://www.cbioportal.org/study/summary?id=luad_tcga_pan_can_atlas_2018

The data contains de-identified data from 566 patients across 4 tables: patients, samples, mutations, and genes. Check SCHEMA.md for more information.

## What the script does

The script:

- Loads the provided SQLite database
- Uses SQL to count non-Silent mutations per patient for TP53, KRAS, EGFR, STK11, and KEAP1
- Counts patients by tissue source site and tumor stage, including missing stages
- Uses Python to reshape gene counts into five separate columns
- Combines clinical information and gene counts into one row per patient
- Retains missing clinical values as NA
- Saves the feature table, site-stage counts, and validation results

## Validation and missing data

The gene count query was expected to have 2,830 rows (566 patients x 5 genes) and had 2,830 rows, with 746 non-Silent mutation counts observed.

The site-stage query was expected to return 142 rows based on the distinct combinations of the observed site and stage and had 142 rows. The total number of patients in these categories was 566, including all 54 patients with missing stages.

There were 566 patients prior to any joins, after the clinical LEFT JOIN, after reshaping, and finally after the merging step. Each patient had exactly one sample and there were no foreign key violations observed.

Missing data for sex (52 patients), age (71 patients), and stage (54 patients) was left in as NA. There were no missing data for tissue source site and tumor mutation burden.

The genes with 0 indicate that no records of mutation were found for that particular patient and that particular gene. The genes which have 0 are the ones where mutation is not called, but it doesn’t necessarily indicate that there are no mutations biologically or insufficient sequence coverage.

Individual mutation records for patient TCGA-05-4244 is tested. This patient has one KRAS Missense_Mutation (p.G12C) and the value of KRAS_count equals to 1. All other genes have counts = 0. Check `patient_check.txt`.

## files

- `gene_counts.sql`: patient-gene mutation-count query
- `site_stage_counts.sql`: patient counts by site and stage
- `SCHEMA.md`: database schema description
- `DATA_DICTIONARY.md`: column meanings, units, sources, and missing-value coding
- `validation_results.txt`: saved validation results
- `patient_check.txt`: individual patient comparison
- `AI_USAGE.md`: documentation of AI assistance
