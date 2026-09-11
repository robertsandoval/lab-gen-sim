# Trigger codegen pipeline

After pushing this demo repo, start the Tekton pipeline:

```bash
# From lab-gen-sim repo (facilitator):
make pipeline-install

# Create PipelineRun (edit image registry first):
oc create -f - <<EOF
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  generateName: demo-${{ values.domain_id }}-
  namespace: ${{ values.pipeline_namespace }}
spec:
  pipelineRef:
    name: demo-domain-codegen
  params:
    - name: brief-path
      value: domain-brief.yaml
    - name: image-registry
      value: ${{ values.image_registry }}
    - name: image-name
      value: general-sim-api
    - name: image-tag
      value: demo-${{ values.domain_id }}
    - name: deploy-namespace
      value: ${{ values.deploy_namespace }}
    - name: skip-approval-gates
      value: "false"
  workspaces:
    - name: shared-workspace
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 5Gi
EOF
```

Clone this repo into the workspace PVC or add a `git-clone` task before `validate-brief`.

See [lab-gen-sim/pipeline/PipelineRun-example.yaml](https://github.com/REPLACE/lab-gen-sim/blob/main/pipeline/PipelineRun-example.yaml).
