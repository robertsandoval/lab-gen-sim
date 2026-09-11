# Module 4 — Customer story (30 min)

Present the simulation demo as a customer-facing impact reasoning story.

## Learning outcomes

- Explain live data + graph + scenario overlay in customer terms
- Use `tool_call_trace` to show grounded, auditable answers
- Map brief entities to customer operational vocabulary

## Narrative structure (15 min)

### 1. The operational picture

"This platform holds a live snapshot of your entities — aircraft, ports, machines, or any defined entity type — with their current state and relationships."

Show: `GET /admin/entities` or `GET /admin/entities/geojson`

### 2. The disruption

"We layer a what-if scenario on top without changing ground truth. Remove the scenario and everything reverts."

Show: `GET /admin/graph/events?scenario_id=<id>` then `POST /query` with the same `scenario_id`

### 3. Impact propagation

"The system traverses your dependency graph to find everything affected, runs quantitative analysis, and retrieves relevant playbooks."

Show: `tool_call_trace` from the query response — typically:

- `get_affected_subgraph`
- `solve_impact`
- `search_scenario_context`

### 4. Recommended response

"The answer is grounded in tool outputs — the LLM explains, it does not invent impact numbers."

Highlight numeric fields from the solver result in the response.

## Customer mapping exercise (10 min)

Given your domain brief, fill in:

| Platform term | Customer term |
|---|---|
| `domain_id` | e.g. "Supply chain visibility" |
| Entity `type` | e.g. "Shipment", "SKU", "Work cell" |
| `SimulationEvent` | e.g. "Port strike", "Line stoppage" |
| `scenario_id` | e.g. "Q4 disruption drill" |
| `attributes` fields | Customer KPIs (revenue, SLA tier, …) |

## Demo script template

```
1. "Here is our live operational view" → admin entities / geojson
2. "A disruption occurs" → describe scenario narrative
3. "What is the impact?" → POST /query with prepared question
4. "How do we know?" → walk tool_call_trace
5. "What should we do?" → highlight ranked response options from solver
6. "Another scenario?" → inject second event or switch scenario_id
```

## What this is not

- Not a discrete-event physics simulator (no tick-by-tick dynamics)
- Not a replacement for ERP/MES — it reasons over a graph + snapshot model
- Not fully automatic for complex live APIs — synthetic fixtures are reliable for first customer meetings

## Wrap-up

- Extensions live in demo forks only — upstream platform unchanged
- Pipeline can regenerate domains from new briefs for the next customer vertical
- Pin SHA documented in [UPSTREAM.md](../../UPSTREAM.md)

## Resources

- [UPSTREAM.md](../../UPSTREAM.md)
- [examples/briefs/](../../examples/briefs/)
- Upstream `ADD_DOMAIN.md` on `chore/helm-cleanup`
