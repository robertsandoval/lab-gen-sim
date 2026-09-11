# Module 1 — Platform tour (30 min)

Deploy the pinned general-simulation platform and run the aviation UK airspace closure demo.

## Learning outcomes

- Deploy general-simulation from `chore/helm-cleanup` using `helm/` + `make deploy`
- Seed demo data with `uv run seed-demo`
- Validate end-to-end reasoning with `make smoke-test`
- Explore the JSON Admin API (no built-in Admin SPA on this branch)

## Steps

### 1. Clone upstream (read-only)

```bash
git clone --branch chore/helm-cleanup \
  https://github.com/rh-ai-quickstart/general-simulation.git
cd general-simulation
git checkout 4118e0e69a30aabaf27c2f905acebebb4993d53a
```

Do **not** fork this for domain work — demo repos are created in Module 3.

### 2. Build and deploy

```bash
podman login quay.io
make build

make deploy \
  PG_PASSWORD='<postgres-password>' \
  NEO4J_PASSWORD='<neo4j-password>' \
  MAAS_API_TOKEN='<maas-token>'
```

Default LLM on this branch uses LiteMaaS (`global.models.external-model`). For OpenAI instead, enable `global.models.openai` in `helm/values.yaml` and pass `OPENAI_API_KEY`.

Verify pods:

```bash
make status
# or: oc get pods -n general-simulation
```

### 3. Smoke test

From the upstream clone:

```bash
# Auto-detects cluster vs local seeding
make smoke-test
```

Or explicitly for in-cluster:

```bash
SEED_MODE=cluster NAMESPACE=general-simulation make smoke-test
```

This runs `scripts/smoke-uk-closure.sh`, which:

1. Seeds aircraft + UK airspace closure scenario (`opensky-uk-closure-001`)
2. Posts a question to `POST /query`
3. Prints the answer and `tool_call_trace`

### 4. Manual seed (optional)

```bash
uv run seed-demo
```

Requires local Postgres/Neo4j (e.g. `docker compose up -d`) or port-forwards to the cluster.

### 5. Admin JSON API

There is no browser Admin SPA on `chore/helm-cleanup`. Use REST endpoints:

```bash
API=https://$(oc get route general-sim-api -n general-simulation -o jsonpath='{.spec.host}')

curl -s "$API/admin/stats" | jq .
curl -s "$API/admin/graph/scenarios" | jq .
curl -s "$API/admin/graph/events?scenario_id=opensky-uk-closure-001" | jq .
curl -s "$API/admin/entities/geojson" | jq '.features | length'
```

Inject a scenario overlay:

```bash
curl -s -X POST "$API/admin/graph/events" \
  -H 'Content-Type: application/json' \
  -d '{
    "scenario_id": "workshop-test-001",
    "event_type": "disruption",
    "narrative": "Workshop test disruption",
    "affected_entity_ids": ["opensky-407290"]
  }' | jq .
```

### 6. Direct query

```bash
curl -s -X POST "$API/query" \
  -H 'Content-Type: application/json' \
  -d '{
    "scenario_id": "opensky-uk-closure-001",
    "question": "Which aircraft are affected by the UK airspace closure?",
    "allow_live_ingestion": false
  }' | jq '{answer, tool_call_trace}'
```

## Discussion points

- Live data (PostGIS) is never mutated by simulations — overlays are reversible
- The ReAct agent calls graph traversal, solver, vector search, and ingestion tools
- `tool_call_trace` is the audit trail for customer demos

## Next module

[02-domain-seams.md](02-domain-seams.md) — where customer-specific code plugs in.
