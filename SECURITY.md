# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | Yes       |
| < 0.4   | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in MoveWise, please report it responsibly.

**Do not open a public GitHub Issue for security vulnerabilities.**

Instead, please email the maintainers directly. We will acknowledge your report within 48 hours and provide a detailed response within 5 business days.

## Scope

The following areas are in scope for security reports:

- API authentication and authorization logic
- GDPR data handling in consent and profile flows
- User data exposure through API endpoints
- Docker container security configuration
- Dependency vulnerabilities in `requirements.txt` or `package.json`

## Best Practices Implemented

- CORS middleware restricts origins in production
- No user credentials stored in source code
- Docker runs as non-root user
- `.dockerignore` excludes model weights and sensitive files
- GDPR consent mechanism with explicit opt-in
