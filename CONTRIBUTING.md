# Contributing to tai42-connector-atlassian

This repo ships the **Atlassian** connector provider as **pure descriptor data**.
The one rule that shapes everything: **no behaviour, and `tai42-contract` is the
only dependency.**

## Ground rules

- **Depend on `tai42-contract` only.** No other tai-* package, no skeleton import. The
  registration goes through the runtime handle: `from tai42_contract.app import
  tai42_app`, then `tai42_app.connectors.register_connector(descriptor)`.
- **No OAuth / probe / launch code.** All of that is generic in the connector
  engine, keyed off the descriptor. This plugin declares one
  `ProviderDescriptor` and nothing more.
- **Credentials are env-var names**, not typed settings — the descriptor names
  `CONNECTORS_ATLASSIAN_CLIENT_ID` / `CONNECTORS_ATLASSIAN_CLIENT_SECRET`; the
  engine resolves them.
- **Typed package.** `py.typed` ships; keep pyright clean.

## Layout

- `src/tai42_connector/atlassian/core/connector.py` — builds the
  `ProviderDescriptor` and registers it on import. `tai42_connector` is a namespace
  package, so each provider ships in its own repo under the shared namespace.
- `src/tai42_connector/atlassian/tai-plugin.yml` — the plugin manifest.
- **`tests/test_connector.py`** — the descriptor constructs and validates against
  the contract `ProviderDescriptor`, and loading the module registers it through
  the `tai42_app` handle. **No private dependency.**
- **`tests/test_plugin_spec.py`** — the shipped plugin manifest's shape.

## Naming

PyPI is a flat namespace with no owner in the path, so distributions carry the
`tai42-` prefix. GitHub repositories keep their `tai-` names, because the
`tai42ai` organisation already namespaces them. Import packages follow the
distribution.

| Surface | Form |
| --- | --- |
| Distribution — PyPI, `pip install`, dependency pins | `tai42-<name>` |
| Import package | `tai42_<name>` |
| GitHub repository and sibling checkout directory | `tai-<name>` |

So a dependency is declared as `tai42-<name>` but resolved from `../tai-<name>`
during local development, and both spellings are correct in their own context.

Connectors are the one exception to the import-package form: they share the
`tai42_connector` namespace package, so this distribution imports as
`tai42_connector.atlassian` rather than `tai42_connector_atlassian`.

Some surfaces are deliberately neither, and must not be renamed: the `tai` CLI
command (`tai42` is an alias), the Prometheus metric namespace (`tai_tool_*`),
`TAI_*` environment variables, and the `tai-plugin.yml` descriptor filename.

## Dev

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest            # self-contained tests
```

For local cross-repo work, `make dev` editable-installs the sibling `tai-*`
checkouts this package builds on into the venv. While `[tool.uv.sources]` pins
those siblings to local paths, `uv sync` already installs them editable and
`make dev` changes nothing; once the lock resolves them from the registry,
`uv sync` / `uv run` installs the published builds instead, so re-run
`make dev` afterward to restore the editable links.

Before any commit, run a secret scan over `src/` and `tests/` (e.g.
`detect-secrets scan`).

## License

By contributing you agree your contributions are licensed under Apache-2.0.
