# GitOps for demo repositories

The [ApplicationSet](applicationset.yaml) deploys **demo forks** created by the Developer Hub template — not the upstream general-simulation repository.

## Demo manifest format

Register each demo repo in a manifest repo (`demo-domains-manifest`):

```yaml
# demos/manufacturing.yaml
domain_id: manufacturing
repo_url: https://github.com/myorg/demo-manufacturing.git
revision: main
namespace: general-simulation
image_tag: demo-manufacturing-20260910
```

## Deploy without ApplicationSet

From a demo fork at the pinned upstream SHA:

```bash
helm upgrade --install general-simulation ./helm \
  --namespace general-simulation \
  --create-namespace \
  -f helm/values.yaml \
  -f helm/values-overlay.yaml
```

Or use upstream `make deploy` with secrets — see [UPSTREAM.md](../UPSTREAM.md).
