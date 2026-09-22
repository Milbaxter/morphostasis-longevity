# Morphostasis Longevity

An open, evidence-led research program testing connections between cellular
coordination, bioelectric organization, and aging. The long-term aim is to help
develop effective rejuvenation approaches through falsifiable research.

**Initial analyses are being implemented.** This repository does not yet contain
validated new biological findings. See the prospective specifications for the
questions and limits fixed before analysis.

| Investigation | Primary question | Specification |
|---|---|---|
| Spatial bioelectric organization | Does spatial signal change beyond imaging/density effects in a single-donor keratinocyte model? | [Spatial](docs/specs/spatial.md) |
| Epithelial expression | Do predefined ion-homeostasis/coupling genes change coherently across passage and donor-age contexts? | [Epithelial](docs/specs/epithelial.md) |
| Evolutionary gene age | Does oldest-stratum association survive expression, detection, length and sample covariates? | [AGED](docs/specs/aged.md) |

## Reproduce

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/), at least 10 GiB free
disk plus cache space. Dependencies and transitive versions are locked.

```sh
git clone https://github.com/Milbaxter/morphostasis-longevity.git
cd morphostasis-longevity
make reproduce
```

Individual stages: `morphostasis fetch`, `morphostasis validate`,
`morphostasis analyze`, `morphostasis report` (prefix with `uv run --frozen`).
Select a workstream with `--workstream spatial|epithelial|aged`, and use
`--cache-dir` / `--output-dir` for a separate reproduction. Run `make test` for
offline unit and scientific-control tests.

The resource gate limits source cache to 10 GiB and preserves 10 GiB free disk.
Full image ZIP and planarian raw sequencing downloads are excluded. A blocked
data branch is reported explicitly; it is not replaced with synthetic biology.
Synthetic data are used only for software and statistical validation.

## Research record

- [Charter and evidence classes](docs/CHARTER.md)
- [Primary-source evidence register](docs/EVIDENCE.md)
- [Research decisions and agent disagreements](docs/RESEARCH_DECISIONS.md)
- [Source terms](THIRD_PARTY.md)

This is an AI-assisted project coordinated for Milbaxter, using GPT-6 Luna agents
at high reasoning effort and independent computational review. Findings must be
judged by their data, assumptions, and reproducibility. Transcriptomics does not
measure voltage or coupling; culture senescence is distinct from organismal
aging; none of these analyses measures lifespan extension.

Original code is [MIT](LICENSE); original documentation is [CC BY 4.0](LICENSE-DOCS.md).
Please cite the repository revision and the original papers/datasets.
