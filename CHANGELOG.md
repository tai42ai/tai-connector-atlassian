# Changelog

All notable changes to `tai42-connector-atlassian` are documented here; the format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Until 1.0.0 the connector surface is not stable: **minor (0.x) releases may
contain breaking changes.**

## [Unreleased]

First release (0.1.0) in preparation — nothing published yet.

### Added

- Atlassian OAuth 2.0 (3LO) connector descriptor for Jira, Confluence, and
  Compass, registered through the `tai42_app` handle. All three sub-services use
  **granular** OAuth scopes (Atlassian forbids mixing classic and granular
  scopes in one app):
  - Jira: `read:issue:jira`, `read:issue-meta:jira`, `read:project:jira`,
    `read:comment:jira`, `read:attachment:jira`, `read:issue-worklog:jira`,
    `read:jql:jira`, `read:board-scope:jira-software`, `read:sprint:jira-software`,
    `write:issue:jira`, `write:comment:jira`, `write:issue-worklog:jira`,
    `delete:issue:jira`, `write:sprint:jira-software`.
  - Confluence: `read:page:confluence`, `read:hierarchical-content:confluence`,
    `read:comment:confluence`, `read:space:confluence`, `write:page:confluence`,
    `read:content-details:confluence`.
  - Compass: `read:component:compass`, `write:component:compass`.
- **Operators must register their Atlassian OAuth 2.0 (3LO) app with exactly
  these granular scopes for the connector to work.** The Jira grant includes
  `delete:issue:jira`, so consenting users allow issue deletion.
