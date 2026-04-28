# Contributing

Thank you for considering contributing to WereWolf Engine!

## How to Help

- **Report bugs:** Open an issue on GitHub.
- **Suggest features:** Start a discussion in the Issues section.
- **Add a new role:** Create a role class and share it as a plugin (see [Roles](roles.md)).
- **Improve tests:** Add test cases for edge scenarios.

## Development Setup

1. Fork the repository.
2. Clone your fork:

```bash
git clone https://github.com/your-username/WereWolf-Engine.git
cd WereWolf-Engine
```

3. Create a virtual environment and install dev dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

4. Run tests to make sure everything works:

```bash
pytest
```

## Pull Request Guidelines

- Create a branch for your change.
- Add tests if you introduce new functionality.
- Make sure all tests pass (`pytest`).
- Update documentation if needed.
- Submit a PR with a clear description.

## Code Style

This project uses `black` and `ruff` for consistent formatting. Run them before committing:

```bash
black werewolf_engine tests
ruff check werewolf_engine tests
```

Your contributions will be licensed under the same MIT License as the project.
```