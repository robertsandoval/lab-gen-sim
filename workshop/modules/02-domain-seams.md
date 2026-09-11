# Module 2 — Domain seams (30 min)

Understand where customer-specific code plugs into general-simulation without changing core platform logic.

## Learning outcomes

- Identify the four extension points: adapter, registry, graph bootstrap, Helm overlay
- Explain why domain code lives only under `domain/<name>/` in **demo forks**
- Map a domain brief to concrete files

## Core rule

On `chore/helm-cleanup`, these packages contain **zero domain-specific names**:

- `src/core`, `src/reasoning`, `src/graph`, `src/ingestion/runner.py`, `src/solver/stub.py`

All customer logic goes in a **demo repo** fork at the pinned SHA.

## Extension points

| Concern | Location (demo fork) | Changes? |
|---|---|---|
| Live entity ingestion | `domain/<id>/adapters/<adapter_id>.py` | New adapter |
| Catalog registration | `src/ingestion/registry.py` | One `DomainSpec` |
| Dependency graph | `domain/<id>/bootstrap_graph.py` | Neo4j edges + scenario |
| Runtime enablement | `helm/values-overlay.yaml` | `enabledDomains`, `adapterId` |
| Offline tests | `tests/fixtures/`, `tests/test_<adapter>.py` | Fixture + pytest |

## Canonical entity schema

Every adapter normalizes to `CanonicalEntity`:

| Field | Purpose |
|---|---|
| `id` | Globally unique (e.g. `manufacturing-cell-3`) |
| `type` | Generic label (`moving_entity`, `fixed_node`, …) |
| `timestamp` | UTC observation time |
| `status` | Domain-defined state string |
| `geometry` | GeoJSON Point/Polygon or `null` |
| `attributes` | **All** domain-specific fields (JSONB) |

Never add columns to Postgres entity tables for domain fields.

## Reference implementations (upstream, read-only)

| Domain | Adapter | Notes |
|---|---|---|
| `aviation` | `opensky_flights` | Live OpenSky ADS-B |
| `shipping` | `shipping_demo` | Synthetic fixture — best codegen pattern |

Read upstream `ADD_DOMAIN.md` and `domain/shipping/adapters/shipping_demo.py`.

## ENABLED_DOMAINS and adapter_id

- `ENABLED_DOMAINS` — which domain packages load at runtime
- `adapter_id` — which adapter a CronJob or `ingest-run --adapter` executes
- Helm keys on `chore/helm-cleanup`:
  - `api.enabledDomains`
  - `ingestion.enabledDomains`
  - `ingestion.adapterId`
  - `ingestion.enabled: true` (default is `false`)

## Exercise (10 min)

Open [examples/briefs/manufacturing-synthetic.yaml](../../examples/briefs/manufacturing-synthetic.yaml) and list which files the pipeline would generate in a demo fork.

Expected answer:

```
domain/manufacturing/__init__.py
domain/manufacturing/adapters/__init__.py
domain/manufacturing/adapters/opcua_cells.py
domain/manufacturing/bootstrap_graph.py
src/ingestion/registry.py          # DomainSpec added
tests/fixtures/opcua_cells.json
tests/test_opcua_cells.py
helm/values-overlay.yaml
```

## Next module

[03-pipeline-walkthrough.md](03-pipeline-walkthrough.md) — scaffold a demo repo and run the gated pipeline.
