# Contributing

**English** | [Português (Brasil)](CONTRIBUTING.pt-BR.md)

Contributions, compatibility reports, documentation improvements and validation results are welcome.

## Development workflow

1. Create a focused branch from `main`.
2. Keep monitoring read-only and least-privilege.
3. Update English and Brazilian Portuguese documentation together.
4. Preserve existing item keys and UUIDs for backward-compatible changes.
5. Run the local validation suite.
6. Open a pull request.

Recommended branch prefixes are `feature/`, `fix/`, `docs/`, `refactor/`, `test/`, `ci/` and `chore/`.

Conventional Commits are recommended.

## Monitoring design rules

Changes must not add privileged operating-system commands, BIND control/write operations or unnecessary network exposure. Prefer native BIND statistics, standard Zabbix agent keys, dependent items and preprocessing.

## Compatibility reports

Include:

- exact ISC BIND version;
- operating system and version;
- Zabbix Server version;
- Zabbix Agent or Agent 2 version;
- BIND JSON statistics version;
- affected endpoint and item key;
- sanitized sample data when necessary.

Do not publish credentials, TSIG material, public management addresses or customer-identifying hostnames.
