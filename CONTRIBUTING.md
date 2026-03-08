# Contributing to MoveWise

Thank you for your interest in contributing to MoveWise. This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch from `main`
4. Set up both the frontend and RL engine environments:

```bash
# Frontend
cd movewise-react
npm install

# RL Engine
cd ../rl_engine
pip install -r requirements.txt
```

## Development Workflow

We follow a feature-branch workflow:

| Branch Name Pattern | Purpose |
|---|---|
| `feature/<name>` | New features or enhancements |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation updates |
| `refactor/<name>` | Code refactoring without behavior change |

### Branch Conventions

- Always branch from `main`
- Keep branches focused on a single concern
- Rebase on `main` before opening a PR

## Code Style

### Python (RL Engine)

- Follow PEP 8 with a 100-character line limit
- Use type hints for all function signatures
- Include docstrings with references to the v3 formulation (section and equation numbers)
- Use `dataclass` for configuration objects

### JavaScript / React (Frontend)

- Use functional components with hooks
- Keep components under 200 lines; extract sub-components when appropriate
- Use Unicode escape sequences for emoji in JSX (e.g., `\u{1F33F}`)
- CSS classes follow BEM-like naming: `component-name`, `component-name__element`

## Pull Request Process

1. Ensure all tests pass and the training pipeline completes without errors
2. Update the README if your changes affect usage or architecture
3. Add or update docstrings for any modified functions
4. Include relevant v3 formulation references when modifying RL logic
5. Request a review from at least one maintainer

### PR Title Convention

Format: `<type>: <short description>`

Examples:
- `feat: add weather-aware nudge selection`
- `fix: correct GC transfer penalty for carpool mode`
- `docs: update API endpoint documentation`
- `refactor: simplify HUR acceptance model`

## Questions

If you have questions about the project or how to contribute, please open a GitHub Issue or reach out to the maintainers.
