# Contributing to Virtual Environment Manager

Thank you for considering contributing to venv-manager! Here are some guidelines to help you get started.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/spohaver/venv-manager.git
cd venv-manager
```

2. Create a development virtual environment:
```bash
python -m venv dev-venv
source dev-venv/bin/activate  # On Windows: dev-venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e .
pip install -r requirements-dev.txt
```

## Testing

Run tests before submitting changes:
```bash
pytest tests/
```

Test the script manually:
```bash
./venv-manager --help
./venv-manager create --name test-env
./venv-manager list
./venv-manager remove --name test-env --force
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings for new functions and classes
- Keep functions focused and modular

## Submitting Changes

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes and test them
3. Commit with a clear message: `git commit -m "Add feature: description"`
4. Push and create a pull request

## Reporting Issues

When reporting issues, please include:
- Your operating system and Python version
- Command that caused the issue
- Full error message
- Expected vs actual behavior

## Feature Requests

We welcome feature requests! Please:
- Check existing issues first
- Provide a clear use case
- Suggest implementation approach if possible