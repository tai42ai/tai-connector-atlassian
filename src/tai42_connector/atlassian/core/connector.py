"""Atlassian connector provider — Jira, Confluence, and Compass.

A pure-data provider plugin: it declares one :class:`ProviderDescriptor` and
registers it through the ``tai42_app`` handle when the manifest loads this module.
All OAuth / probe / launch behaviour is generic in the connector engine, keyed
off this descriptor — the plugin carries no behaviour of its own.

The three sub-services share Atlassian's hosted Rovo MCP endpoint
(``/v1/mcp/authv2``). Scopes come from each product's canonical OAuth-scope
reference under ``developer.atlassian.com``. Atlassian 3LO requires
``audience=api.atlassian.com`` and rotates refresh tokens on every exchange;
``prompt=consent`` re-prompts so incrementally-added sub-service scopes are
granted. OAuth client credentials are read by the engine from the named env
vars (``CONNECTORS_ATLASSIAN_CLIENT_ID`` / ``CONNECTORS_ATLASSIAN_CLIENT_SECRET``).
"""

from __future__ import annotations

from tai42_contract.app import tai42_app
from tai42_contract.connectors.providers import (
    McpServerDescriptor,
    OAuthEndpoints,
    ProviderDescriptor,
    SubServiceDescriptor,
)

# Atlassian's hosted Rovo MCP endpoint. All three sub-services target the
# ``authv2`` endpoint; the legacy ``/v1/sse`` endpoint is deprecated.
ATLASSIAN_MCP_URL = "https://mcp.atlassian.com/v1/mcp/authv2"


def build_descriptor() -> ProviderDescriptor:
    """Build the Atlassian provider descriptor.

    Validated on construction by the contract model, so a misconfigured
    descriptor fails loudly at load time rather than at first user click.
    """
    return ProviderDescriptor(
        id="atlassian",
        kind="oauth",
        origin="system",
        category="dev-tools",
        display_name="Atlassian",
        description="Connect Jira, Confluence, and Compass.",
        icon_url="/static/connector-icons/atlassian.svg",
        oauth=OAuthEndpoints(
            authorize="https://auth.atlassian.com/authorize",
            token="https://auth.atlassian.com/oauth/token",
            # Atlassian has no public 3LO revocation endpoint; users revoke from
            # id.atlassian.com "Connected apps", and disconnect falls back to a
            # local delete.
            revoke=None,
        ),
        client_id_env="CONNECTORS_ATLASSIAN_CLIENT_ID",
        client_secret_env="CONNECTORS_ATLASSIAN_CLIENT_SECRET",
        sub_services={
            "jira": SubServiceDescriptor(
                id="jira",
                display_name="Jira",
                description=(
                    "Read and search issues, sprints, and projects; create, update, and delete issues; update sprints."
                ),
                scopes=[
                    "offline_access",
                    # Granular scopes equivalent to the classic read:jira-work /
                    # write:jira-work grants: issue, project, comment,
                    # attachment, worklog, and JQL-search read; issue, comment,
                    # and worklog create-update plus issue delete; and the Jira
                    # Software agile board/sprint read with sprint write. The
                    # app is all-granular because Atlassian forbids mixing
                    # classic and granular scopes in one OAuth app.
                    "read:issue:jira",
                    "read:issue-meta:jira",
                    "read:project:jira",
                    "read:comment:jira",
                    "read:attachment:jira",
                    "read:issue-worklog:jira",
                    "read:jql:jira",
                    "read:board-scope:jira-software",
                    "read:sprint:jira-software",
                    "write:issue:jira",
                    "write:comment:jira",
                    "write:issue-worklog:jira",
                    "delete:issue:jira",
                    "write:sprint:jira-software",
                ],
                mcp_server=McpServerDescriptor(type="http", url=ATLASSIAN_MCP_URL),
            ),
            "confluence": SubServiceDescriptor(
                id="confluence",
                display_name="Confluence",
                description="Read and search pages, spaces, and comments; write pages.",
                scopes=[
                    "offline_access",
                    "read:page:confluence",
                    "read:hierarchical-content:confluence",
                    "read:comment:confluence",
                    "read:space:confluence",
                    "write:page:confluence",
                    # Granular equivalent of the classic search:confluence scope
                    # (the granular scope the CQL content-search endpoint
                    # accepts); keeps the whole app on granular scopes.
                    "read:content-details:confluence",
                ],
                mcp_server=McpServerDescriptor(type="http", url=ATLASSIAN_MCP_URL),
            ),
            "compass": SubServiceDescriptor(
                id="compass",
                display_name="Compass",
                description="Read and update components in the service catalog.",
                scopes=[
                    "offline_access",
                    "read:component:compass",
                    "write:component:compass",
                ],
                mcp_server=McpServerDescriptor(type="http", url=ATLASSIAN_MCP_URL),
            ),
        },
        # 3LO requires audience=api.atlassian.com; prompt=consent re-prompts the
        # user when a new sub-service is added so incremental scopes are granted.
        extra_authorize_params={
            "audience": "api.atlassian.com",
            "prompt": "consent",
        },
    )


# Manifest-loaded registration: importing this module registers the provider
# through the runtime app handle. The manifest binds ``tai42_app`` before loading
# plugins, so the handle resolves; loading the module is the registration.
tai42_app.connectors.register_connector(build_descriptor())
