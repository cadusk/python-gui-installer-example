# Running Tests

## Quick Commands

```bash
# Run all tests with coverage
uv run pytest

# Or use Makefile shortcuts
make test         # Run all tests
make test-fast    # Stop at first failure
make test-verbose # Extra verbosity
```

## Test Configuration

- All pytest config is in `pyproject.toml` under `[tool.pytest.ini_options]`
- Tests are in `tests/` directory
- Coverage tracking enabled for `models/`, `services/`, `ui/`
- HTML coverage report generated in `htmlcov/index.html`

## CI/CD

- Tests run automatically in GitHub Actions before builds
- Uses same command: `uv run pytest`
- Build fails if any tests fail
- Runs on Linux, Windows, and macOS

## Requirements

- pytest-cov is in dev dependencies
- Run `uv sync` to install dev dependencies first
