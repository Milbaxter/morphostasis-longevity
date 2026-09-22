# AGED reproduction and confounder-aware extension

**Status:** prospective specification; no new hypothesis test has been run.  
**Workstream:** evolutionary gene-age associations during human fibroblast aging.  
**Known prior evidence:** Pio-Lopez and Levin (2025) reported shifts toward ancient phylostrata across a set of aging and senescence signatures. Those published results are known at specification time; this document is not an external preregistration.

## Questions and decision rules

1. Can the published `LPioL/atavisticDissociation` GenAge enrichment outputs be reproduced from the repository's pinned inputs and code? This is a computational reproduction, not new evidence for AGED.
2. In healthy adult dermal fibroblasts, do genes in the oldest phylostratum show stronger age-associated expression than comparable measurable genes after accounting for expression level, detection, transcript length, sex, and sequencing platform? This is the primary new test.
3. Does the estimate retain direction and useful precision in the single-platform subset and under reasonable expression/mapping sensitivities?

Evidence for an ancient-gene association requires a positive oldest-stratum excess in age-association strength, an empirical one-sided permutation (p<0.05), and a positive lower 95% confidence bound for the matched effect estimate. Results that fail any of these conditions are reported as unresolved or inconsistent with this operational prediction; no alternative endpoint will be promoted to primary after inspection.

## Data and provenance

- AGED article: Pio-Lopez and Levin, *Aging Cell* (first published 2025-12-08), DOI [10.1111/acel.70305](https://doi.org/10.1111/acel.70305).
- Original code/data: [LPioL/atavisticDissociation](https://github.com/LPioL/atavisticDissociation), pinned to commit `7438e3259a56f9ab4b541d5ec5bab9d5a367dc7e` (HEAD observed 2026-09-22). Relevant tracked items include `genage_percentages_only.py`, `data/over.all.csv`, `data/under.all.csv`, `data/1-s2.0-S0093775418302264-mmc2.csv`, and checked-in `results/genage_*` files. Their hashes, license, and the source file's exact parsing/filtering behavior will be recorded in the data manifest before execution.
- Human expression cohort: GEO [GSE113957](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE113957), original study [Fleischer et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6300908/). Processed matrix: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE113nnn/GSE113957/suppl/GSE113957_fpkm.txt.gz` (advertised size 7.2 MB). GEO family SOFT: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE113nnn/GSE113957/soft/GSE113957_family.soft.gz` (advertised size 12,768 bytes). SHA-256 values will be recorded on retrieval; data are fetched into ignored cache and not committed.
- GEO SOFT metadata inspection (2026-09-22; before testing): 143 samples total; 133 normal and 10 HGPS; normal adult subset age ≥20 has 107 donors, age 20–96; platform coverage is GPL18573 n=94 (age 20–96) and GPL16791 n=13 (age 30–50). Sex is available with inconsistent capitalization and will be normalized. Cell source, disease, age, sex, and platform will be parsed from structured SOFT characteristics, not inferred from column-name strings.
- The processed expression matrix header contains `Transcript ID`, genomic coordinates, strand, `Length`, `Copies`, `Annotation/Divergence`, followed by sample columns. GEO documents FPKM values, hg19, and the highest-expressed isoform as the original gene-expression proxy. The supplied matrix's actual row multiplicity, duplicate gene annotations, numeric validity, and join coverage to phylostratigraphy will be summarized before testing. Mapping/collapse rules will be deterministic and recorded; no gene may be duplicated in an endpoint.

## Cohort and exclusions

Primary cohort: normal/healthy donors aged at least 20 years. Exclude all HGPS samples and samples under age 20 from the primary age slope; childhood-to-adult expression includes developmental change and cannot identify adult aging cleanly. The biological unit is the donor. Repeated measurements, if any are discovered, will be consolidated to one donor-level observation before the model or treated as clustered observations; never count technical replicates as independent donors.

HGPS is held out of the primary test. Any later HGPS contrast is secondary and will be labeled premature-progeria disease-associated expression, not a replication of normal aging. Culture passage/replicative age is not equated with donor chronological age; if passage metadata are absent, this limitation is explicit.

## Fixed processing and mapping

1. Parse sample metadata from GEO SOFT and join exactly to matrix column IDs. Fail validation on missing/duplicate sample IDs, invalid ages, conflicting health/platform fields, or an unexplained matrix/metadata mismatch.
2. Apply a documented transcript-to-gene procedure based on the matrix annotation and the versioned human gene-age source. Prefer the repository's stated highest-expressed isoform proxy when the input is one transcript per gene; if multiple transcript rows per gene remain, select the transcript with the largest mean FPKM across all eligible healthy adult donors, without using age labels. Use only unambiguous human protein-coding gene identifiers present in the phylostratigraphy table. Report all exclusions and mapping rates.
3. Define detection as FPKM > 0 across eligible donors. The measurable-gene universe is the set of successfully mapped protein-coding genes with at least 10% detected adult donors. This is the background for all primary phylostratum comparisons; the whole coding genome is not used as the expression-study background.
4. Transform expression as `log2(FPKM + 0.1)`; the pseudocount is fixed. Report robustness at pseudocount 0.01 and 1 as sensitivity analyses. No count-based method is applied to FPKM.
5. For each measurable gene, fit ordinary least squares `log2(FPKM+0.1) ~ age_centered + sex + platform`, using donor as row. The primary age statistic is the absolute two-sided t statistic for the linear age coefficient; signed slope and FDR-adjusted p-value are retained. Age is continuous and modeled per decade for readable effect sizes. Use HC3 standard errors if numerical diagnostics permit; otherwise report conventional OLS and flag the change. Exclude covariates only if the design matrix is rank-deficient, with the reason documented before viewing phylostratum results.

## Primary endpoint and null

The primary estimand is the difference in mean absolute age t statistic between measurable genes in phylostratum 1 (“All living organisms”) and genes in phylostrata 2–19, after matching on baseline abundance, detection, and transcript length. This tests whether ancient genes have stronger age-associated expression without requiring effects to be exclusively up- or down-regulation. It tests association strength only; it does **not** test whether the transcriptional profile has shifted in a signed direction toward an ancestral state.

For matching, transform abundance and transcript length as `log1p`, retain detection fraction, and form deterministic quantile strata using cut points computed without age labels. Process oldest-stratum genes in ascending stable gene ID and match each to up to five non-oldest genes, without replacement globally, ordered by standardized Euclidean distance in abundance, detection, and transcript length. Require the same abundance and detection quintiles first. If no unused control remains, back off in a fixed order: nearest detection quintile (ties lower first), then nearest abundance quintile (ties lower first), then nearest transcript-length quintile (ties lower first). If no unused control is available after these backoffs, drop that ancient gene and report its count. Matched sets are therefore disjoint. The matched estimate is the mean within-set difference in absolute t statistics. Its empirical one-sided conditional null permutes ancient-stratum labels within each disjoint set while preserving the set's single ancient label (10,000 permutations; fixed seed 20260922); this explicitly assumes gene-age labels are exchangeable within matched sets under the conditional null. Report the Monte Carlo p-value with plus-one correction.

For uncertainty, use 500 donor bootstrap replicates sampled within sex-by-platform strata. In each replicate, refit gene-wise models and recalculate the fixed matched-set statistic, holding the original match membership fixed. Report the percentile 95% interval; if more than 5% of bootstrap fits fail because of rank deficiency, the interval is unresolved. Also run a second, donor-level Freedman–Lane null with 999 row permutations: fit the reduced expression model with sex and platform, permute the donor residual rows as intact vectors shared across all genes, add them to reduced-model fitted values, and refit the age term. This retains the cross-gene covariance structure and tests the global no-age-association null. Report both nulls separately: the matched gene-label null is primary and conditional on matched exchangeability; the donor residual null verifies whether the observed ancient-stratum statistic exceeds age-free sample-level structure. Use a fixed seed 20260922 and plus-one p-value correction for both.

Also report (secondary, not substitutionary) oldest-stratum odds ratio for genes with BH FDR <0.05, weighted/ordinal phylostratum trend in absolute t statistic, and ancient-stratum signed slope distribution. The signed slopes are descriptive and do not turn the primary test into a directional ancestral-regression test. The 19-bin analysis corrects across all strata with Benjamini–Hochberg. If primary matching retains fewer than 50% of eligible oldest-stratum genes or fewer than 100 oldest-stratum genes in total, declare the primary estimate underpowered/unresolved and emphasize matched coverage; do not loosen matching after seeing outcomes.

## Confounder controls and sensitivity analyses

- **Detection/expression/length:** primary matched controls above; additionally show unadjusted whole-testable-universe results to make the effect of these controls visible. The promoter is the matched result, not the unadjusted enrichment.
- **Platform:** include platform in the primary sample-level expression model; repeat the entire gene analysis on GPL18573-only donors (n=94 eligible by metadata inspection). GPL16791 has only ages 30–50, so no platform-only subset is used for the full-range age slope.
- **Sex:** include normalized sex as a fixed effect; report missingness and a sex-adjusted versus unadjusted effect comparison. Do not claim sex-specific aging effects from this imbalanced cohort.
- **Age form:** compare the prespecified linear adult age model to a quadratic term as a sensitivity only; do not select the model by smallest p-value.
- **Expression transform:** fixed pseudocount robustness at 0.01 and 1.
- **Resampling:** bootstrap donors within sex/platform strata for uncertainty; do not resample genes as if they were independent biological replicates.
- **Mapping:** summarize a sensitivity using alternate unambiguous gene ID/symbol mapping if provided by the cited phylostratigraphy source. No alias-based many-to-many joins.

## Cohort overlap and claim limits

GSE113957 is not listed as an individual study in AGED's table of the eight named study families; however, AGED includes the Palmer et al. 2021 multi-tissue signature, which aggregates 127 datasets. Independence cannot be claimed until its source-study inventory is checked against GSE113957. The result will be described as a held-out cohort test only if that audit establishes no cohort overlap; otherwise it is a cohort-level reanalysis/sensitivity. Other published work has also reanalyzed GSE113957, so dataset novelty is not claimed.

Transcript abundance is not a direct measure of ancestral cell state, spatial coordination, membrane voltage, bioelectric coupling, tissue coherence, rejuvenation, or lifespan. A positive result is a phylogenetic association in an adult fibroblast expression dataset. It is neither causal evidence nor evidence about keratinocyte spatial voltage patterns.

## Failure and stop conditions

Stop the analysis with a machine-readable validation error if: source checksums or required fields are unavailable; GEO metadata cannot be joined unambiguously; age/disease/platform annotations conflict; the design matrix is rank-deficient for the age term; gene mapping is many-to-many and cannot be resolved prospectively; or fewer than 1,000 measurable genes remain. Report the limitation rather than reconstructing missing values. Treat a lost or reversed matched effect, insufficient ancient-gene coverage, or platform sensitivity as a null/fragile result. Do not modify the cohort, primary endpoint, matching thresholds, or null after viewing test statistics.

## Outputs and execution contract

Implementation will expose `fetch(cache_dir: Path, out_dir: Path) -> dict`, `validate(cache_dir: Path, out_dir: Path) -> dict`, and `analyze(cache_dir: Path, out_dir: Path) -> dict`. Reproducible outputs go under `results/aged/`: `summary.json`, machine-readable tables, plots, and a concise report. Data manifests record source URL, retrieval date, bytes, SHA-256, terms/license, and source commit. A cohort overlap audit records searched source inventories, exact matches, and unresolved status. Tests cover input validation, mapping/collapse, gene-background construction, matching, permutation reproducibility, null/synthetic behavior, and summary/output schemas. No analysis is run until this specification is reviewed and explicitly released by the coordinating agent.
