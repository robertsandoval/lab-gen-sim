# Upstream dependency (read-only)

This workshop depends on [general-simulation](https://github.com/rh-ai-quickstart/general-simulation) as a **read-only** upstream. Do not commit, push, or open pull requests against that repository from this lab.

## Pinned reference

| Field | Value |
|---|---|
| Repository | `https://github.com/rh-ai-quickstart/general-simulation` |
| Branch | `chore/helm-cleanup` |
| Commit SHA | `4118e0e69a30aabaf27c2f905acebebb4993d53a` |
| Clone (read-only) | `git clone --branch chore/helm-cleanup https://github.com/rh-ai-quickstart/general-simulation.git` |
| Checkout pin | `git checkout 4118e0e69a30aabaf27c2f905acebebb4993d53a` |

## Where changes go

| Artifact | Repository |
|---|---|
| Workshop docs, Tekton, prompts, Backstage template | `lab-gen-sim` (this repo) |
| Generated domain code, registry edit, Helm overlay | Scaffolder-created `demo-<domain_id>` repo |
| Core platform (`src/core`, `src/reasoning`, etc.) | **Never** — use upstream pin as-is |

## Deploy baseline (from pinned upstream)

Run these commands inside a clone of general-simulation at the pinned SHA (not in `lab-gen-sim`):

```bash
podman login quay.io
make build
make deploy \
  PG_PASSWORD='<postgres-password>' \
  NEO4J_PASSWORD='<neo4j-password>' \
  MAAS_API_TOKEN='<maas-token>'
```

Secrets can also be supplied via `helm/values-secrets.yaml` in the upstream clone (never commit that file).

## Smoke test (from pinned upstream)

```bash
# Seed UK airspace closure demo + POST /query (auto-detects cluster vs local)
make smoke-test

# Or step by step:
uv run seed-demo
./scripts/smoke-uk-closure.sh

# In-cluster seeding after deploy:
SEED_MODE=cluster NAMESPACE=general-simulation make smoke-test
```

Default scenario: `opensky-uk-closure-001`.

## Key upstream paths on `chore/helm-cleanup`

| Path | Purpose |
|---|---|
| `helm/` | Umbrella Helm chart (authoritative deploy) |
| `helm/values.yaml` | Default values (MaaS chat model, `ingestion.enabled: false`) |
| `helm/values-full.yaml` | Full reference including `enabledDomains`, `adapterId` |
| `ADD_DOMAIN.md` | Human checklist for new domains |
| `docs/prompts/add-domain/README.md` | Staged LLM prompts (copied into `lab-gen-sim/prompts/`) |
| `domain/aviation/`, `domain/shipping/` | Reference domain packages |
| `src/ingestion/registry.py` | `DOMAIN_CATALOG` — one line added per new domain in demo forks |

## Updating the pin

When upstream `chore/helm-cleanup` moves, update the SHA in this file and in `templates/create-demo-domain/template.yaml`. Re-run `make smoke-test` against the new pin before teaching the workshop.
