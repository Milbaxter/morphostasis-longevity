# Prospective spatial bioelectric aging analysis

## Question and scope

Does spatial autocorrelation of keratinocyte membrane-potential signal change with culture age after accounting descriptively for mean signal and cell coverage? The primary analysis is a reproducible, culture-level reanalysis of the published spatial-imaging data. It is not a test of organismal rejuvenation, lifespan extension, or a treatment recommendation.

The analysis will use the released image archive only after a read-only inventory identifies eligible samples and the complete image payload can be retrieved within the project's cache limits. The 19.95 GB ZIP will not be downloaded wholesale. A subset may be fetched only if its archive structure permits bounded range requests, all requested byte ranges are verified, and both the 10 GB cache ceiling and 10 GB free-space floor remain satisfied. If those conditions fail, record the access/manifest blocker and stop the raw-data analysis.

## Provenance and sample eligibility

Before computing outcomes, record the Dataverse DOI, dataset version, file ID, filename, advertised size, license, HTTP status and `Content-Range` for each requested range, archive-member name, member size, checksum when available, and source URL. Do not store signed URLs or credentials. Do not fetch image members until a sample manifest can identify an eligible cohort.

The sample manifest must preserve published labels verbatim and include, where discoverable: figure-folder/member path, reported age in culture, passage, replicate label, treatment, imaging modality/dye, image role/channel, and any explicit culture/well/field identifier. Keep unknown values null. Never infer that equal numeric replicate labels from different figure folders are paired. Flag conflicts between the prerevision Dataverse folder numbering and the final article figure numbering; map figures by assay/content and source-file provenance, not by number alone.

Eligible primary samples are untreated baseline cultures with spatial Vmem-sensitive imaging and enough image metadata to identify the biological culture and field. A matched Hoechst channel may support a cell-coverage/density covariate. If a pairing between channels or replicate metadata cannot be established from source labels, exclude that covariate and report why. Include day-10 cultures as the early reference and day-40/day-50 cultures as the prespecified late group; retain day-40 and day-50 separately in plots and secondary contrasts. Passage is reported alongside culture day because they are near-collinear in this study; do not claim independent age and passage effects.

## Experimental unit and image processing

The independent unit is the biological culture/replicate identified by the source, not an individual cell, pixel, overlapping window, image tile, or random subsample. Fields nested in one culture are summarized within culture before group inference. The study uses neonatal keratinocytes from one donor, so the analysis cannot estimate donor-to-donor variation.

Reproduce the authors' image preparation and spatial statistic where the distributed scripts and necessary inputs are available. The paper describes a 15 × 15 pixel ROI scan over non-background pixels, x/y/lifetime extraction, a k-nearest-neighbor graph selected at k=3, and repeated 1,000-cell subsampling. Record exact code/input correspondence. Do not count the 10 subsampling iterations or the cells as independent replicates. If the original pipeline cannot be reproduced from available files, label any reconstructed segmentation or graph analysis as an alternative analysis, not a reproduction.

For each field, retain the valid-pixel/cell mask and raw lifetime values. Calculate mean lifetime (relative Vmem proxy), valid area/cell count or coverage when supported, and Global Moran's I with k=3. Aggregate field estimates to one culture estimate using a declared weighting rule; default to equal field weights to avoid letting larger fields dominate. Report field-level distributions descriptively. Treat lifetime as a relative dye signal, not an absolute voltage measurement.

## Outcomes and comparisons

**Primary outcome:** culture-level Global Moran's I from voltage-sensitive spatial images.

**Primary contrast:** day 10 versus the pooled late group (day 40 and day 50, equally weighted by culture, not by cell or field). Show all culture points and estimate the culture-level difference with an uncertainty interval. Also report day 10 vs day 40 and day 10 vs day 50 separately as descriptive secondary contrasts.

**Incremental-information question:** assess whether the age-associated spatial signal is distinguishable from mean lifetime and cell coverage. First report unadjusted culture-level association of Moran's I with culture day. Then fit only a parsimonious, prespecified culture-level model with Moran's I as outcome and culture day/group, mean lifetime, and coverage as predictors if the number of independent cultures and rank of the design matrix permit it. Report coefficients, uncertainty, collinearity, and leverage; do not use cell-level rows, machine learning, or a fixed incremental-R² threshold. If sample size/rank is inadequate, report the adjusted question as not estimable and retain descriptive stratified plots. If cross-figure replicate matching to senescence markers is not explicit, do not fit marker-prediction models or claim that spatial metrics add predictive information for senescence markers.

## Spatial and measurement sensitivity analyses

1. Recompute Moran's I with k=2 through k=8 and compare conclusions with the paper's k=3 result.
2. Compare the original overlapping 15 × 15 pixel scan with a non-overlapping spatial sampling/segmentation analysis if source pixel images permit both. The methods are alternatives; do not select the result with the strongest age effect.
3. For each image, permute lifetime values over its fixed valid mask to obtain a within-image null that preserves the observed lifetime histogram and mask. This checks whether measured spatial arrangement exceeds a random arrangement for that field; it does not increase biological sample size or replace culture-level inference.
4. Evaluate signal robustness to measurement noise only using a documented noise estimate from source technical controls or replicate imaging. If no such estimate is available, omit numeric noise perturbation and state that measurement-noise sensitivity could not be calibrated.
5. Where VF2.0 voltage-insensitive controls are present and comparable, analyze them separately as an assay-artifact check; do not pool them with Vmem-sensitive images.

## Perturbation and time-series analyses

Analyze bioelectric pretreatment spatial images separately from baseline aging cohorts. If sample labels establish biological replicate and treatment groups, calculate one Moran's I value per culture and compare the reported control, pinacidil, and depolarizing-treatment conditions as treatment contrasts. Keep the published treatment conditions and source figure identity explicit. Do not call the experiment randomized unless the paper documents random allocation.

Analyze BeRST pre/post-pinacidil time series separately. Pair frames only when their within-culture pre/post identity is explicit; summarize the within-culture lifetime response and recovery/resilience with a prespecified time window only if timestamps and frame order support it. These BeRST series do not measure spatial Moran's I unless the acquisition/labels establish spatial frames. Never infer a treatment effect from unmatched conditions or from age-group comparisons.

## Inference, limitations, and stopping rules

Use biological cultures as n and show their values. Given the small reported n and one donor, prioritize effect estimates and uncertainty over binary significance. Use an exact culture-label permutation only when the exchangeability assumptions and group sizes make it valid; otherwise report descriptive contrasts. Do not make population-wide or clinical claims.

Stop and mark the primary raw-data analysis `blocked` or `not_estimable` if: source file ranges cannot be fetched/verified within bounds; cohort membership or biological replicate labels cannot be reconstructed; there are fewer than three independent cultures in an age-condition; or images lack sufficient signal/mask information to calculate the prespecified statistic. Fewer than three cultures is a reporting floor, not a guarantee of adequate power. Report any available data-quality issue rather than silently dropping samples.

## Required outputs

The analysis implementation will expose `fetch(cache_dir: Path, out_dir: Path) -> dict`, `validate(cache_dir: Path, out_dir: Path) -> dict`, and `analyze(cache_dir: Path, out_dir: Path) -> dict`. `fetch` is restricted to bounded metadata/range retrieval and eligible members; `validate` checks source hashes, labels, completeness, image dimensions/channels, and independent-unit counts; `analyze` produces culture-level estimates and figures. Save a machine-readable `results/spatial/summary.json` with status, source/version/checksums, eligible and excluded members, replicate counts, methods, results, caveats, and reason for any blocked/not-estimable analysis. Keep downloaded raw data under gitignored `data/cache/spatial`; commit only manifests and derived summaries/figures.
