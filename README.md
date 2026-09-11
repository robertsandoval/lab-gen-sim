# lab-gen-sim — General-Simulation LLM-Guided Demo Lab (RHADS)

Workshop assets for building customer demos on top of [general-simulation](https://github.com/rh-ai-quickstart/general-simulation) (`chore/helm-cleanup` branch) using Red Hat Advanced Developer Suite:

- **Developer Hub** software template to scaffold demo repos
- **OpenShift Pipelines** gated codegen pipeline (LLM touchpoints + human approval gates)
- **GitOps** ApplicationSet for demo deployments
- **Workshop modules** for facilitators and participants

## Policy

- **No changes to general-simulation.** See [UPSTREAM.md](UPSTREAM.md).
- Generated domain code lives in scaffolder-created `demo-<domain_id>` repositories only.

## Repository layout

```
catalog-info.yaml          # Register this repo in Developer Hub
UPSTREAM.md                # Pinned upstream SHA + read-only policy
schemas/                   # domain-brief JSON Schema
examples/briefs/           # Example briefs (aviation, manufacturing)
prompts/                   # Tekton LLM prompt templates (from upstream add-domain)
pipeline/                  # Tekton Pipeline + tasks
templates/                 # Backstage create-demo-domain template
gitops/                    # ApplicationSet for demo repos
workshop/                  # Facilitator guide + modules
scripts/                   # Pipeline helper scripts
```

## Quick start

1. Read [UPSTREAM.md](UPSTREAM.md) and deploy general-simulation at the pinned SHA.
2. Run baseline smoke: `make smoke-test` in the upstream clone (see [workshop/modules/01-baseline-demo.md](workshop/modules/01-baseline-demo.md)).
3. Register `catalog-info.yaml` in Developer Hub.
4. Install pipeline: `oc apply -f pipeline/` in your workshop namespace.
5. Use the **Create Demo Domain** template to scaffold a demo repo and trigger the pipeline.

## Workshop

Start at [workshop/README.md](workshop/README.md).
