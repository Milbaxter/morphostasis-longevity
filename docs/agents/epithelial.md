# Epithelial workstream handoff

The epithelial workstream implements the prospective specification in `docs/specs/epithelial.md`. Its focus is fixed-panel gene expression across independent human replicative-senescence and epidermal aging datasets. It does not infer membrane voltage or gap-junction function from RNA abundance.

Data sources are GSE155371 (`GSE155371_normed.txt.gz`, normalized RNA-seq expression) and GSE85358 (processed Agilent sample values / Series Matrix). Donors, not culture replicates or microarray probes, are biological units. GSE155371 has three donors, so conventional significance is not expected to resolve. GSE85358 supplies 24 donors per age group.

The public planarian tail RNA-seq is excluded from fresh processing under local resource limits: the nine relevant paired-end FASTQ files alone total 32.6 GB compressed. A limited secondary use of published source-data fold changes would require a separate specification.

Fetch, validation, analysis, and report entry points are exposed through `morphostasis.epithelial` and CLI integration if/when approved by the coordinating agent. Do not alter common CLI/IO code; coordinate any integration need with the root agent.
