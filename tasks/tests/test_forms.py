# tasks/tests/test_forms.py
import pytest
from django.utils import timezone
from datetime import timedelta
from tasks.forms import TaskForm
from tasks.models import Task
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

class TestTaskForm:
    
    def test_valid_form(self):
        """Prueba formulario válido"""
        user = User.objects.create_user(username='testuser')
        data = {
            'title': 'Tarea de prueba',
            'description': 'Descripción de prueba',
            'due_date': timezone.now() + timedelta(days=2),
            'priority': 2
        }
        form = TaskForm(data=data)
        assert form.is_valid()
    
    def test_invalid_due_date(self):
        """Prueba fecha de vencimiento inválida"""
        data = {
            'title': 'Tarea de prueba',
            'due_date': timezone.now() - timedelta(days=1),
            'priority': 1
        }
        form = TaskForm(data=data)
        assert not form.is_valid()
        assert 'due_date' in form.errors
    
    def test_required_fields(self):
        """Prueba campos requeridos"""
        form = TaskForm(data={})
        assert not form.is_valid()
        assert 'title' in form.errors
        assert 'due_date' in form.errors