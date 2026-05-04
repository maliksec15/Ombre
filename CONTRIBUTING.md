# Contributing to Ombre

Thank you for your interest in contributing to Ombre. This document explains how to contribute effectively.

---

## Ways to Contribute

- **Bug reports** — Open a GitHub Issue with full reproduction steps
- **Provider connectors** — Add support for new GPU providers
- **Performance improvements** — Optimize routing or scanning logic
- **Documentation** — Improve clarity and completeness
- **Tests** — Expand test coverage

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/ombreaiq/ombre.git
cd ombre

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v
```

---

## Adding a New Provider

Provider connectors live in `ombre/providers/`. Each provider must implement the `BaseProvider` interface:

```python
from ombre.providers.base import BaseProvider

class MyProvider(BaseProvider):
    def scan_workloads(self) -> list:
        """Return list of active GPU workloads."""
        ...

    def get_pricing(self, gpu_type: str) -> dict:
        """Return current pricing for GPU type."""
        ...

    def route_job(self, job: dict) -> dict:
        """Route a job to this provider."""
        ...

    def get_idle_capacity(self) -> list:
        """Return list of idle GPU windows."""
        ...
```

Add your provider to `ombre/providers/__init__.py` and write tests in `tests/test_providers.py`.

---

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-provider`
3. Write your code and tests
4. Ensure all tests pass: `python -m pytest tests/ -v`
5. Submit a pull request with a clear description

---

## Code Standards

- Python 3.9+ compatible
- Type hints on all public functions
- Docstrings on all classes and public methods
- Tests for all new functionality
- No secrets or API keys in code

---

## Questions

Email: [ombreaiq@gmail.com](mailto:ombreaiq@gmail.com
