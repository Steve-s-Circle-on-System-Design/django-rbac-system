# Contributing to the Django RBAC System

Thanks for considering a contribution! We welcome bug fixes, features, and doc improvements.

## Code of Conduct

Be respectful, inclusive, collaborative, and take ownership of your work.

## Getting Started

```bash
git clone https://github.com/Steve-s-Circle-on-System-Design/django-rbac-system.git
cd your-repo

python -m venv venv
venv\Scripts\activate         # windows
source venv/bin/activate      # ios 

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

git checkout -b feature/your-feature-name
```

Configure a `.env` file with your `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, and JWT token lifetimes.

## Development Guidelines

- Follow PEP 8 and DRF conventions
- Use `black`, `isort`, `flake8`
- Keep business logic in services/selectors, not views/serializers

```bash
flake8 . && black . && isort .
```

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(auth): implement JWT refresh token rotation
fix(orders): resolve race condition in stock validation
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

## Testing

```bash
pytest --cov=. --cov-report=term-missing
```

- New features need tests; bug fixes need regression tests
- Target 80%+ coverage

## Documentation

- Update `README.md` / `CONTRIBUTING.md` as needed
- Add docstrings; include OpenAPI/Swagger annotations for endpoints

## Security

- Never commit secrets or `.env` files
- Validate input via serializers; use the ORM, never raw SQL
- Run `pip-audit` and `python manage.py check --deploy` before submitting a PR
- Report vulnerabilities privately to **security@your-project.com** (48hr response)

## Pull Requests

Before submitting:
- Rebase on latest `main`
- Ensure tests pass and coverage doesn't drop
- Update docs; include migrations if models changed

PR title: `<type>(<scope>): <description>`

## Issues

**Bugs**: title, environment, repro steps, expected vs. actual behavior, logs
**Features**: problem, proposed solution, alternatives, priority

## Code Review

Maintainers review within 48 hours; one approval required to merge. Be constructive, explain your reasoning, respond promptly.

## Recognition

Contributors are added to `CONTRIBUTORS.md` and recognized in release notes.

---

Thank you for contributing!
