# Epithelial aging and bioelectric-machinery expression: prospective specification

**Version:** 1.0  
**Frozen before inspecting cohort expression associations:** 2026-09-22  
**Scope:** secondary, exploratory expression analysis; no voltage, electrical coupling, rejuvenation, or causal claims.

## Question and hypotheses

Do fixed, biologically motivated plasma-membrane ion-homeostasis and gap-junction gene sets show donor-consistent expression changes during independent primary keratinocyte senescence and in vivo human epidermal aging? Are those changes more coherent than predeclared proliferation and stress control sets?

H1: one or more bioelectric-machinery submodules have a directionally coherent age/passage association in the oral-keratinocyte study, with donor-level sign consistency beyond the control modules. H2: the same prespecified submodule(s) show a concordant age-group direction in the independent epidermis cohort. H1/H2 are exploratory and do not predict whether Vmem becomes more positive or negative. A transcript's abundance does not determine channel current, membrane voltage, or tissue coupling.

## Fixed datasets and units

1. **GSE155371**: normalized bulk RNA-seq expression, 18 libraries from three primary oral-keratinocyte donors; two culture replicates nested within each donor at passages 5, 10, and terminal passage (13–16). Biological unit is donor; replicate cultures are repeated/nested observations. This tests passage-associated replicative senescence, not chronological donor aging. Processed file `GSE155371_normed.txt.gz` (GEO reports 1.9 MB) is normalized expression, not raw integer counts. Do not apply DESeq2 count models. Primary contrast: terminal passage versus passage 5, paired within donor after averaging the two culture replicates within each donor/passage. Secondary descriptive contrast: passage 10 versus passage 5.
2. **GSE85358**: processed Agilent expression for inner-forearm epidermis, 24 donors aged 20–25 and 24 aged 55–66. Biological unit is donor, one array per donor. This tests cross-sectional chronological age, not induced senescence or rejuvenation. Use GEO processed sample values / Series Matrix; do not download the 590.4 MB raw tar unless a later QC finding requires it. Fit a linear age-group contrast. Include sex only if GEO metadata provide complete sex labels and both age groups have adequate overlap; otherwise report age as an unadjusted association and flag sex imbalance.

The two datasets are analyzed independently. Never batch-correct or pool their expression values. The human epidermis cohort is an independent age-context triangulation; oral keratinocytes are the direct independent senescence-model triangulation.

## Fixed panels

Panel membership is in `data/bioelectric_panel.csv`, defined by public canonical annotations and the directly relevant human keratinocyte study before association analysis. Submodules are kept separate because the genes do not have a common functional direction: increased expression could reflect compensation, altered composition, or changed activity, and cannot be translated to depolarization/hyperpolarization.

- **KATP channel complex:** KCNJ8, KCNJ11, ABCC8, ABCC9; selected because the focal study uses pinacidil, described there as a KATP-channel opener. Subunit membership comes from canonical human gene/protein annotations. This is a target-linked candidate panel, not an assertion that every transcript is expressed or functional in these samples.
- **Na/K pump:** ATP1A1, ATP1A2, ATP1B1, ATP1B3.
- **Plasma-membrane Ca pump:** ATP2B1, ATP2B4.
- **Epithelial ion transport:** SLC9A1, SLC12A2.
- **Gap-junction connexins:** GJA1, GJB2, GJB6. This is a connexin-expression panel, not a coupling assay.
- **Proliferation controls:** MKI67, PCNA, MCM2, the fixed markers discussed as proliferation/growth-fraction markers in [Krebs et al.](https://pubmed.ncbi.nlm.nih.gov/27246286/). These are state controls, not senescence-specific markers.
- **Senescence/stress controls:** CDKN1A, CDKN2A, IL1A, IL6, CXCL8, HSPA1A. These are separate from bioelectric panels and are not used to select the primary gene set after observing data.
- **Epithelial-state controls:** KRT14, KRT10, DSG1, FLG, to expose differentiation/cell-state changes that can confound bulk tissue comparisons.

All genes are predeclared with equal gene weight within each submodule. No post hoc substitutions or dropping genes based on observed effect direction. Report which genes are actually measured by each platform; each gene's panel denominator is the detected/represented subset, and minimum reporting threshold is 50% of fixed members and at least two members per submodule. Missing genes are not imputed.

## Outcomes and statistics

Primary outcomes are per-gene log2 fold changes (or equivalent normalized-expression contrast) and submodule equal-weight mean standardized gene effects. For GSE155371, compute each gene's within-donor terminal-minus-passage-5 difference after culture-replicate averaging, then report all three donor effects and the mean/median; use exact sign/permutation summaries and do not rely on asymptotic p-values with three donors. With three donors, the smallest two-sided sign-test p-value is 0.25; thus no donor-level conventional significance claim is possible. For GSE85358, use a donor-level linear model on GEO processed log-scale values; report group effect, 95% CI, and p-value for each gene. Apply Benjamini–Hochberg separately across (a) measured fixed bioelectric genes and (b) all measured panel genes; keep both raw and adjusted values. No inference is made from a small panel's mean alone if individual effects oppose each other.

Panel coherence endpoint: direction agreement fraction among measured genes, median signed standardized effect, and mean signed standardized effect; retain the full vector. Standardized effects divide each gene's contrast by its SD across biological-unit-level normalized expression values within the same cohort; for GSE155371 first average replicate cultures within donor/passage and calculate SD from the resulting nine donor-by-passage values. A gene with SD <= 1e-8 is unstandardizable and is excluded from magnitude summaries but remains listed with its raw contrast. Compare each of the five bioelectric submodules to 10,000 seeded random panels matched on gene count and pooled-expression/detection bins within each platform. Compute empirical null p-values separately for direction coherence and absolute mean standardized effect, then apply Benjamini–Hochberg adjustment across the five submodules within each cohort and endpoint. Also compare bioelectric panels against the fixed proliferation, stress, and epithelial-state controls. Random panels are computational controls, not biological replicates. Resampling/permutation occurs at donor level; no cell, probe, culture replicate, or gene is treated as an independent human.

Cross-cohort triangulation endpoint: same-sign mean submodule effect across the two cohorts, with all donor-level oral effects and epidermis confidence interval shown. This is descriptive cross-cohort concordance; do not combine p-values across studies or claim independent mechanistic validation of Vmem. The GSE155371 exact paired sign-flip space has only 2^3 assignments, so its minimum two-sided permutation p-value is 0.25. No donor-level p<0.05 result is attainable there. Failure to reject or donor-direction inconsistency in n=3 is unresolved/underpowered evidence, not a biological falsification. Report all three paired donor effects and avoid binary “pass/fail” biological conclusions from that cohort.

## Falsification and interpretation rules

- A submodule is not estimable if fewer than 2 measured genes or fewer than 50% of its fixed members are represented. If its observed direction agreement/absolute mean effect is not beyond the 95th percentile of matched random-panel nulls, report no detectable expression coherence at the tested resolution. This does not establish a biological null.
- Cross-cohort concordance is unsupported if the age-cohort effect is opposite in sign, its confidence interval spans zero, or the effect is no more coherent than matched null panels. This is unresolved for cross-cohort expression concordance, not a refutation of bioelectric involvement in aging.
- If control panels show similarly strong changes or epithelial-state controls change strongly, interpret the bioelectric expression result as possibly reflecting broad senescence, proliferation, differentiation, or tissue-composition shifts.
- A missing or unmappable key panel in either assay is a data-coverage failure, not a null biological result.
- Never state that transcriptomics measures Vmem, channel gating, gap-junction conductance, bioelectric pattern, or rejuvenation.

## Reproducibility and resource limits

Use the repository's pinned Python environment. Fetch only the processed 1.9 MB GSE155371 matrix and GSE85358 Series Matrix/sample processed values; never fetch the raw GEO tar or SRA FASTQs for this analysis. Preserve original files only under gitignored `data/cache/epithelial/`. Record exact source URL, retrieval time, byte count, SHA-256, accession/sample table, normalization description, and any metadata exclusions in manifests. Outputs are machine-readable tables plus `summary.json`, report, and figures under `results/epithelial/`.

## Sources

- Sediqi & Levin, “Bioelectric characterization of senescing human keratinocytes,” iScience 28 (2025), [doi:10.1016/j.isci.2025.113275](https://doi.org/10.1016/j.isci.2025.113275); primary paper and experimental details: [PMC12496192](https://pmc.ncbi.nlm.nih.gov/articles/PMC12496192/). The work measures Vmem directly in neonatal epidermal keratinocytes from one donor and uses pinacidil; it does not supply transcriptomics for the panels specified here.
- Schwartz et al., “Insights into epithelial cell senescence from transcriptome and secretome analysis of human oral keratinocytes,” [PMC7950289](https://pmc.ncbi.nlm.nih.gov/articles/PMC7950289/); [GSE155371](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155371). Reports three donors, passage-resolved RNA-seq, and donor heterogeneity.
- Kuehne et al., “Metabolic alterations in aged human skin in vivo,” [PubMed 28201987](https://pubmed.ncbi.nlm.nih.gov/28201987/); [GSE85358](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE85358). Reports 24 young and 24 older adult epidermis samples and processed array values.
- NCBI GEO RNA-seq count-data scope/limitations: [NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/info/rnaseqcounts.html). GEO-normalized RNA-seq expression is not raw counts and is not used here for count-based inference.
- KATP target rationale: the primary keratinocyte paper uses pinacidil as a KATP opener ([PMC12496192](https://pmc.ncbi.nlm.nih.gov/articles/PMC12496192/)). The specific subunit list uses approved HGNC symbols and canonical KATP complex nomenclature; gene/protein function annotations are available through [HGNC](https://www.genenames.org/) and [UniProt](https://www.uniprot.org/). This supports panel selection only, not an expected age direction.
- Connexin family / gap junction role: reviewed by Laird, “Life cycle of connexins in health and disease,” [Biochemical Journal (2006)](https://doi.org/10.1042/BJ20051822). GJA1/GJB2/GJB6 are fixed representative human connexin genes; results do not represent all gap-junction genes.
- Na/K ATPase, PMCA, and epithelial transport genes are canonical transport machinery, included as test candidates rather than assumed aging directions; symbols/function annotations cross-checked against [HGNC](https://www.genenames.org/) and [UniProt](https://www.uniprot.org/). Proliferation controls are anchored by Krebs et al.'s marker review ([PubMed 27246286](https://pubmed.ncbi.nlm.nih.gov/27246286/)); senescence controls follow measured markers in the two primary epithelial studies. No gene is selected or removed based on observed cohort effects.
