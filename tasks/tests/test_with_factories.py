# tasks/tests/test_with_factories.py
import pytest
from tasks.tests.factories import TaskFactory, UserFactory
from tasks.models import Task

pytestmark = pytest.mark.django_db

class TestWithFactories:
    
    def test_create_tasks_with_factory(self):
        """Prueba creación de tareas con Factory"""
        tasks = TaskFactory.create_batch(5)
        assert Task.objects.count() == 5
        assert all(isinstance(task, Task) for task in tasks)
    
    def test_complete_task_factory(self):
        """Prueba completar tarea creada con Factory"""
        task = TaskFactory()
        task.mark_as_completed()
        assert task.status == 'COMPLETED'