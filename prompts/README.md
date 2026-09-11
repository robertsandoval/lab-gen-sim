# LLM prompt templates for Tekton codegen

Copied and adapted from general-simulation `docs/prompts/add-domain/README.md` on branch `chore/helm-cleanup` at SHA `4118e0e69a30aabaf27c2f905acebebb4993d53a`.

**Do not edit the upstream repo.** Update prompts here only.

## Template variables

| Variable | Source |
|---|---|
| `{{DOMAIN_BRIEF}}` | Contents of `domain-brief.yaml` |
| `{{DOMAIN_SPEC}}` | Output of stage 1 (`domain-spec.json`) |
| `{{DOMAIN_ID}}` | `domain_id` from brief |
| `{{ADAPTER_ID}}` | `adapter_id` from brief |

## Pipeline mapping

| Stage | Prompt file | Upstream equivalent |
|---|---|---|
| 1 generate-spec | `stage1-domain-spec.txt` | Prompt 0 + structured output |
| 2 generate-adapter | `stage2-adapter.txt` | Prompts 1–2 |
| 3 run-tests | `stage3-tests.txt` | Prompt 3 |
| 4 generate-graph | `stage4-graph-scenarios.txt` | Prompt 4 |
| Deploy wiring | (in stage2 helm overlay) | Prompt 6 |

Optional: `stage0-orient.txt` for human review before codegen.
