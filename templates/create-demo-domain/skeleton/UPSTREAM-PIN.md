# Upstream pin (read-only)

This demo repository was scaffolded from general-simulation.

| Field | Value |
|---|---|
| Branch | ${{ values.upstream_branch }} |
| SHA | ${{ values.upstream_sha }} |
| Policy | Do not push changes to rh-ai-quickstart/general-simulation |

Domain extensions in this repo only:

- `domain/${{ values.domain_id }}/`
- `src/ingestion/registry.py`
- `helm/values-overlay.yaml`
