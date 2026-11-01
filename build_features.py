from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
GENES = ["TP53", "KRAS", "EGFR", "STK11", "KEAP1"]

con = sqlite3.connect(
    (ROOT / "data/cohort.db").as_uri() + "?mode=ro",
    uri=True,
)

n_patients = con.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
assert n_patients == 566

clinical = pd.read_sql_query("""
    SELECT
        p.patient_id,
        p.sex,
        p.age_at_diagnosis,
        p.stage,
        s.tissue_source_site,
        s.tmb_nonsynonymous
    FROM patients p
    LEFT JOIN samples s ON s.patient_id = p.patient_id
    ORDER BY p.patient_id
""", con)

assert len(clinical) == n_patients
assert clinical["patient_id"].is_unique

counts = pd.read_sql_query(
    (ROOT / "gene_counts.sql").read_text(), con
)
assert len(counts) == n_patients * len(GENES)
assert not counts.duplicated(["patient_id", "gene_symbol"]).any()
assert counts["mutation_count"].sum() == 746

# SQL already aggregated mutations to one row per patient and gene.
wide = counts.pivot(
    index="patient_id",
    columns="gene_symbol",
    values="mutation_count",
).reindex(columns=GENES)

assert not wide.isna().any().any()
wide = wide.astype("int64")
wide.columns = [f"{gene}_count" for gene in GENES]
wide.columns.name = None

features = clinical.merge(
    wide.reset_index(),
    on="patient_id",
    how="left",
    validate="one_to_one",
).sort_values("patient_id")

assert len(features) == 566
assert features["patient_id"].is_unique
assert set(features["patient_id"]) == set(clinical["patient_id"])
assert not features[[f"{g}_count" for g in GENES]].isna().any().any()

features.to_csv(ROOT / "feature_table.tsv", sep="\t", index=False, na_rep="NA")

site_stage = pd.read_sql_query(
    (ROOT / "site_stage_counts.sql").read_text(), con
)
assert len(site_stage) == 142
assert site_stage["n_patients"].sum() == 566
site_stage.to_csv(
    ROOT / "site_stage_counts.tsv", sep="\t", index=False, na_rep="NA"
)

report = [
    "Validation results",
    f"Patients before joins: {n_patients}",
    f"Rows after clinical LEFT JOIN: {len(clinical)}",
    f"Gene query: expected 2830 rows; actual {len(counts)}",
    f"Non-Silent target-gene mutations: {counts['mutation_count'].sum()}",
    f"Patients after Python pivot: {len(wide)}",
    f"Patients after final merge: {len(features)}",
    f"Site-stage query: expected 142 rows; actual {len(site_stage)}",
    f"Patients across site-stage groups: {site_stage['n_patients'].sum()}",
    "",
    "Missing clinical values retained as NA:",
]
for column in clinical.columns:
    if column != "patient_id":
        report.append(f"{column}: {features[column].isna().sum()}")

report.extend([
    "",
    "Gene counts of 0 mean no qualifying mutation record was found.",
    "They do not prove that a tumor is biologically mutation-free.",
    "Missing clinical values remain NA; no patients were dropped.",
])

text = "\n".join(report) + "\n"
(ROOT / "validation_results.txt").write_text(text)
print(text)
print("Saved feature_table.tsv, site_stage_counts.tsv, and validation_results.txt")

con.close()
