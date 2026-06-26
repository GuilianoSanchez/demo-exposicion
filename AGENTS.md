# AGENTS.md - taskmanager

## Stack

- **Django 6.0.6** + **Django REST Framework 3.17.1** (`rest_framework`)
- **SQLite** (default, no other DB config)
- **pytest** (not Django's unittest runner) + **pytest-cov** + **pytest-django** + **factory_boy**
- No `requirements.txt` / `pyproject.toml` — packages installed manually

## Commands

```sh
# Run all tests with coverage (configured in pytest.ini)
pytest

# Run a specific test file
pytest tasks/tests/test_api.py

# Run a single test class or method
pytest tasks/tests/test_api.py::TestTaskAPI::test_create_task

# Run without coverage
pytest --no-cov

# Run Django dev server
python manage.py runserver

# Run migrations (no migration tooling set up — use `makemigrations` then `migrate`)
python manage.py makemigrations
python manage.py migrate
```

`pytest.ini` forces `--create-db`, `-v`, and `--cov=tasks` by default.

## Tests

- All test files live in `tasks/tests/` (not the legacy `tasks/tests.py`)
- Every test module/class **must** set `pytestmark = pytest.mark.django_db` for DB access
- API tests use `rest_framework.test.APIClient` with `force_authenticate(user=user)` — **always** authenticate
- URL resolution uses `reverse('task-list')`, `reverse('task-complete', kwargs={'pk': pk})`
- Factories: `TaskFactory`, `UserFactory` in `tasks/tests/factories.py`

## API

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/tasks/` | List user's tasks |
| POST | `/api/tasks/` | Create task |
| GET | `/api/tasks/{id}/` | Retrieve task |
| PUT/PATCH | `/api/tasks/{id}/` | Update task |
| DELETE | `/api/tasks/{id}/` | Delete task |
| POST | `/api/tasks/{id}/complete/` | Mark task completed |

Tasks are **always** filtered to `request.user` in `get_queryset`. Creating sets `created_by=self.request.user`.

## Known issues

- `tasks/tests/test_api.py` uses bare `status` (e.g. `status.HTTP_201_CREATED`) without importing it — will raise `NameError`. Import from `rest_framework import status` to fix.
