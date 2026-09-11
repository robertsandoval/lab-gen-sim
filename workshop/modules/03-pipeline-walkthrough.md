# Module 3 — Create your demo (60 min)

Use Developer Hub to scaffold a demo repo and walk the gated Tekton pipeline.

## Learning outcomes

- Fill a domain brief and validate it against the JSON Schema
- Approve LLM-generated artifacts at human gates
- Deploy a demo fork with Helm overlay and run smoke tests

## Prerequisites

- Module 1 complete (baseline platform running)
- `lab-gen-sim` pipeline installed: `oc apply -k pipeline/`
- Developer Hub catalog includes this repo's `catalog-info.yaml`

## Step 1 — Install pipeline (facilitator, once)

```bash
oc project <workshop-namespace>
oc apply -k pipeline/
```

Verify:

```bash
oc get pipeline,task -n <workshop-namespace>
```

## Step 2 — Create demo via Developer Hub

1. Open Developer Hub → **Create** → **Create Demo Domain**
2. Fill parameters (or use defaults for a synthetic manufacturing demo)
3. Submit — scaffolder creates `demo-<domain_id>` repo and opens a PR with `domain-brief.yaml`
4. Merge the PR to trigger `PipelineRun` (or create manually below)

### Manual PipelineRun (fallback)

```bash
oc create -f - <<EOF
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  generateName: demo-domain-
spec:
  pipelineRef:
    name: demo-domain-codegen
  params:
    - name: git-repo-url
      value: https://github.com/<org>/demo-manufacturing.git
    - name: git-revision
      value: main
    - name: domain-brief-path
      value: domain-brief.yaml
    - name: image-registry
      value: quay.io/<org>
    - name: image-tag
      value: workshop-$(date +%Y%m%d)
  workspaces:
    - name: shared-workspace
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 2Gi
    - name: git-credentials
      secret:
        secretName: git-credentials
EOF
```

## Step 3 — Pipeline stages and gates

| Stage | What happens | Your action |
|---|---|---|
| 0 validate-brief | JSON Schema check | Auto |
| 1 generate-spec | LLM emits `domain-spec.json` | **Review PR / approve gate** |
| 2 generate-adapter | LLM writes adapter + registry | **Review PR / approve gate** |
| 3 run-tests | `uv run pytest` offline | Auto (fails = fix brief) |
| 4 generate-graph | LLM writes bootstrap + seed | **Review PR / approve gate** |
| 5 build-push | Image to Quay | Auto |
| 6 gitops-deploy | Apply `helm/values-overlay.yaml` | Optional review |
| 7 smoke-test | Seed + `POST /query` | Auto |

Human gates use Tekton `when` + manual approval task or PR review in the demo repo between stages. See `pipeline/tasks/manual-approval.yaml`.

## Step 4 — Review generated code

Check the demo repo PR diff. Allowed paths only:

- `domain/**`
- `tests/**`
- `src/ingestion/registry.py`
- `helm/values-overlay.yaml`
- `scripts/seed_<domain>.py` (optional)

If the pipeline reports a diff violation, reject the PR and re-run with a clearer brief.

## Step 5 — Verify deployment

After stage 7:

```bash
# From demo repo clone at pinned upstream + overlay
make smoke-test

# Or query your scenario
curl -s -X POST "$API/query" \
  -H 'Content-Type: application/json' \
  -d "{
    \"scenario_id\": \"<your-scenario-id>\",
    \"question\": \"$(yq '.demo_questions[0]' domain-brief.yaml)\",
    \"allow_live_ingestion\": false
  }" | jq .
```

## Tips

- Use `data_source.mode: synthetic` for first demos (matches `shipping_demo` pattern)
- Keep one domain enabled if you need a custom solver (`StubSolver` is the default)
- Pre-fill aviation brief from [examples/briefs/aviation-uk-closure.yaml](../../examples/briefs/aviation-uk-closure.yaml) if codegen fails — baseline still demos

## Next module

[04-customer-narrative.md](modules/04-customer-narrative.md)
