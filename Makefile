# lab-gen-sim workshop utilities

.PHONY: validate-brief pipeline-configmaps pipeline-install lint-briefs

validate-brief:
	python3 scripts/validate-brief.py examples/briefs/manufacturing-synthetic.yaml
	python3 scripts/validate-brief.py examples/briefs/aviation-uk-closure.yaml

lint-briefs: validate-brief

# Build ConfigMaps from local scripts/ and prompts/ for Tekton tasks
pipeline-configmaps:
	oc create configmap lab-gen-sim-scripts \
		--from-file=validate-brief.py=scripts/validate-brief.py \
		--from-file=check-diff-allowlist.sh=scripts/check-diff-allowlist.sh \
		--from-file=llm-generate.py=scripts/llm-generate.py \
		--from-file=apply-llm-files.py=scripts/apply-llm-files.py \
		--dry-run=client -o yaml | oc apply -f -
	oc create configmap lab-gen-sim-prompts \
		--from-file=prompts/ \
		--dry-run=client -o yaml | oc apply -f -

pipeline-install: pipeline-configmaps
	oc apply -k pipeline/
