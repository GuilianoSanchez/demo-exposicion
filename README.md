# TaskManager

API REST para gestión de tareas construida con Django y Django REST Framework.

## Requisitos

- Python 3.x
- pip

## Instalación de dependencias

```bash
pip install django djangorestframework pytest pytest-django pytest-cov factory_boy
```

## Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## Ejecutar el servidor

```bash
python manage.py runserver
```

## Ejecutar pruebas unitarias

Todas las pruebas:

```bash
pytest
```

Archivo específico:

```bash
pytest tasks/tests/test_api.py
```

Prueba individual:

```bash
pytest tasks/tests/test_api.py::TestTaskAPI::test_create_task
```

Sin cobertura:

```bash
pytest --no-cov
```
