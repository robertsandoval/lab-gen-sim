# Workshop: General-Simulation LLM-Guided Demo Lab

Facilitator guide for the RHADS workshop. Participants extend general-simulation with a new domain using a gated Tekton pipeline — without modifying the upstream platform repo.

## Audience

- Platform engineers setting up Developer Hub + Pipelines
- Solution architects building customer-specific simulation demos
- Developers learning domain extension seams on `chore/helm-cleanup`

## Duration

~2.5 hours (four modules, 30–60 min each).

## Prerequisites

| Requirement | Notes |
|---|---|
| OpenShift 4.13+ | Cluster-admin or equivalent for pipeline install |
| RHADS SSC | Developer Hub, OpenShift Pipelines, GitOps, Quay |
| general-simulation deployed | Pinned `chore/helm-cleanup` — see [UPSTREAM.md](../UPSTREAM.md) |
| `MAAS_API_TOKEN` | Default chat model on workshop clusters |
| Git org for demo repos | **Not** the general-simulation upstream repo |

## Modules

| # | Module | File |
|---|---|---|
| 1 | Platform tour — deploy + aviation smoke test | [01-baseline-demo.md](modules/01-baseline-demo.md) |
| 2 | Domain seams — where extensions plug in | [modules/02-domain-seams.md](modules/02-domain-seams.md) |
| 3 | Create your demo — Developer Hub + pipeline | [modules/03-pipeline-walkthrough.md](modules/03-pipeline-walkthrough.md) |
| 4 | Customer story — present impact reasoning | [modules/04-customer-narrative.md](modules/04-customer-narrative.md) |

## Facilitator checklist

- [ ] Upstream pinned SHA deployed and `make smoke-test` passes
- [ ] `lab-gen-sim` pipeline installed in workshop namespace
- [ ] Developer Hub catalog includes `catalog-info.yaml` from this repo
- [ ] Quay org/repo for demo images accessible from pipeline SA
- [ ] MaaS token available for build-time LLM tasks (or OpenAI fallback configured)
- [ ] Pre-bake aviation baseline before Module 3 if codegen may run slowly

## Troubleshooting

| Symptom | Check |
|---|---|
| `ENABLED_DOMAINS` mismatch | `api.enabledDomains` and `ingestion.enabledDomains` in `helm/values-overlay.yaml` |
| Empty adapter list | Domain registered in `registry.py` and domain id in `ENABLED_DOMAINS` |
| `/query` timeout | Use in-cluster query (`SEED_MODE=cluster`); increase `QUERY_TIMEOUT` |
| Neo4j SCC errors | `openshift.neo4j.scc.enabled: true` in upstream `helm/values.yaml` |
| Pipeline diff rejected | Only `domain/`, `tests/`, `registry.py`, `helm/values-overlay.yaml` allowed |
| No Admin SPA | Use JSON API at `/admin/*` — see Module 1 |

## Related docs

- [UPSTREAM.md](../UPSTREAM.md) — pin and no-push policy
- [examples/briefs/](../examples/briefs/) — sample domain briefs
- [schemas/domain-brief.schema.json](../schemas/domain-brief.schema.json) — brief validation
