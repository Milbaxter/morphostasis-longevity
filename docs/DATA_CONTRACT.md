# Data and execution contract

Every workstream exposes `fetch(cache_dir, out_dir)`, `validate(cache_dir, out_dir)`,
and `analyze(cache_dir, out_dir)` returning a JSON-serializable status dictionary.
The CLI passes one workstream's subdirectory to each function. Raw source assets
stay in that ignored subdirectory; global budgets apply to the common parent.

Source manifests must include accession/DOI or repository revision, exact public
URL, retrieval timestamp, size, SHA-256, terms, and analytical use. A download is
not considered valid solely because the endpoint returned 200: parse and validate
expected file format, dimensions, sample IDs, and annotations. ZIP partial reads
require 206 with an exact `Content-Range` before any response body is read.

Sample tables distinguish study, subject/donor/culture, condition, technical
replicate/field, covariates, and raw identifier. Unknown values stay missing. Data
schemas can differ by assay, but these identities cannot be conflated.

`summary.json` is the workstream result entry point. It must state status, methods,
sample/feature counts, quantitative results if estimable, caveats, and evidence
class. A blocked source or unidentifiable contrast is not a measured null.

CLI stages write `run_<stage>.json` with software versions, source revision, and
each workstream's status. Unexpected execution exceptions make the command fail;
scientifically valid null/inconclusive outcomes remain completed computations.

Results must be regenerated after implementation changes affecting their values.
Nondeterministic provenance timestamps may differ across reruns; numerical
results, sorted identifiers, and source hashes must agree to stated precision.
