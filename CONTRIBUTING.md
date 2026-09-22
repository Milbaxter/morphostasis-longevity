# Contributing

Contributions should change a scientific decision, improve reproducibility, or
resolve a documented measurement limitation. Include the source accession and
version, biological unit, estimand, controls, uncertainty, and a runnable command.

Commit a specification before inspecting a new analysis outcome. Amendments
after inspection must be labeled exploratory and state what changed and why.
Report negative results and limitations with the same detail as positive results.

Run `make test` and the affected workstream. Never commit downloaded source data,
tokens, signed URLs, or identifiable donor information beyond the public study
metadata needed for reproducibility. External data keep their source terms.

For a new result, request an independent rerun and inspect sensitivity to the
experimental unit, cohort overlap, missingness, and multiple comparisons. A
plausible mechanism is a hypothesis until a discriminating experiment measures it.
