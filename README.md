# CUSTOM-GPT

A lightweight workspace for experimenting with custom GPT behaviors and prompts. This repository now includes a **tool security + telemetry layer** that can wrap every connector/tool execution.

## What was added

Implementation lives in `src/safe_tools/` and covers:

1. **AuthN/AuthZ**
   - Service tokens (`token_id + secret` with hashed secret storage).
   - Role bindings per subject.
   - RBAC checks per tool/connector via `ToolConfig.allowed_roles`.

2. **Policy Engine**
   - Ordered allow/deny policies with wildcard matching.
   - Action-level checks such as `repo.write` or `prod.db.read`.
   - Role-conditional policies.

3. **Audit Logging**
   - JSONL audit events with:
     - who (`subject`)
     - when (`timestamp`)
     - which tool/connector/action
     - input arguments
     - outcome/error
     - latency/retry/cost
     - trace id

4. **Tracing + Metrics**
   - Trace span per tool call (`trace_id`).
   - In-memory metrics for:
     - latency
     - success/failure rates
     - retry count
     - tool cost

5. **Kill-switch + Rate Limits**
   - Connector-level kill-switch for immediate shutdown of high-risk integrations.
   - Token-bucket rate limiting at connector level.

## Quick start

Run the example:

```bash
PYTHONPATH=src python3 src/safe_tools/example.py
```

The example:
- registers a service token
- binds RBAC roles
- loads policy rules (`allow repo.write`, `deny prod.db.read`)
- registers a high-risk tool with connector rate limits
- executes a tool call
- writes audit events to `logs/tool_audit.jsonl`

## Project structure

- `src/safe_tools/models.py` – shared domain models.
- `src/safe_tools/auth.py` – service token auth + RBAC.
- `src/safe_tools/policy.py` – policy engine (allow/deny rules).
- `src/safe_tools/audit.py` – JSONL audit logger.
- `src/safe_tools/telemetry.py` – tracing + metrics primitives.
- `src/safe_tools/rate_limit.py` – connector kill-switch + token-bucket limits.
- `src/safe_tools/gateway.py` – orchestration layer wrapping tool execution.
- `src/safe_tools/example.py` – runnable end-to-end example.

## Development

- Commit changes in small, reviewable increments.
- Keep configuration files under version control and avoid committing secrets.
- Use `.gitignore` to keep transient artifacts out of the repository.

## Contributing

Issues and pull requests are welcome as the project grows. Please include clear descriptions of any changes or ideas for new functionality.
