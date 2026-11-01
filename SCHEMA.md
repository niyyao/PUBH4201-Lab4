# Database Schema

The database contains four tables. I inspected their columns, primary
keys, and foreign keys using SQLite PRAGMA commands.

## TABLE: patients

- Grain: one row per patient.
Rows: 566
Columns (name, type, primary key):
patient_id TEXT PRIMARY KEY
sex TEXT
age_at_diagnosis REAL
stage TEXT
vital_status TEXT
followup_months REAL
Foreign keys (column -> referenced table.column):
None


## TABLE:samples

- Grain: one row per tumor sample.
Rows: 566
Columns (name, type, primary key):
sample_id TEXT PRIMARY KEY
patient_id TEXT
tissue_source_site TEXT
tmb_nonsynonymous REAL
aneuploidy_score REAL
msi_mantis_score REAL
Foreign keys (column -> referenced table.column):
patient_id -> patients.patient_id


## TABLE: mutations

- Grain: one row per recorded mutation in a sample.
Rows: 200789
Columns (name, type, primary key):
mutation_id INTEGER PRIMARY KEY
sample_id TEXT
gene_symbol TEXT
variant_classification TEXT
variant_type TEXT
protein_change TEXT
chromosome TEXT
start_pos INTEGER
end_pos INTEGER
t_ref_count INTEGER
t_alt_count INTEGER
Foreign keys (column -> referenced table.column):
gene_symbol -> genes.gene_symbol
sample_id -> samples.sample_id


## TABLE: genes

- Grain: one row per gene.
Rows: 17756
Columns (name, type, primary key):
gene_symbol TEXT PRIMARY KEY
entrez_gene_id INTEGER
chromosome TEXT
Foreign keys (column -> referenced table.column):
None


## Relationships and checks

One patient having many samples is possible through the use of a foreign key in samples.patient_id rather than using the sample primary key. By doing a LEFT JOIN and then counting the number of samples per patient, I confirmed that all 566 patients in this database have exactly one sample, which means that the relationships is one to one.
Many mutations can be associated with a sample, but each mutation refers to one sample. Many genes may be associated with mutation, but each mutation refers to one gene. These are one to many relationships between samples and mutations, and between genes and mutations.
PRAGMA foreign_key_check did not return any violations.
