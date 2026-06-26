# tasks/tests/test_models.py
import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from tasks.models import Task

pytestmark = pytest.mark.django_db

class TestTaskModel:
    
    def test_create_task(self):
        """Prueba la creación básica de una tarea"""
        user = User.objects.create_user(username='testuser', password='12345')
        task = Task.objects.create(
            title='Tarea de prueba',
            description='Descripción de prueba',
            created_by=user,
            due_date=timezone.now() + timedelta(days=2)
        )
        
        assert task.title == 'Tarea de prueba'
        assert task.status == 'PENDING'
        assert task.pk is not None
    
    def test_mark_as_completed(self):
        """Prueba marcar una tarea como completada"""
        user = User.objects.create_user(username='testuser', password='12345')
        task = Task.objects.create(
            title='Tarea a completar',
            created_by=user,
            due_date=timezone.now() + timedelta(days=1)
        )
        
        task.mark_as_completed()
        
        assert task.status == 'COMPLETED'
        assert task.completed_at is not None
        assert task.is_overdue() == False
    
    def test_is_overdue(self):
        """Prueba la verificación de tareas vencidas"""
        user = User.objects.create_user(username='testuser', password='12345')
        
        # Tarea vencida
        overdue_task = Task.objects.create(
            title='Tarea vencida',
            created_by=user,
            due_date=timezone.now() - timedelta(days=1)
        )
        
        # Tarea no vencida
        future_task = Task.objects.create(
            title='Tarea futura',
            created_by=user,
            due_date=timezone.now() + timedelta(days=1)
        )
        
        assert overdue_task.is_overdue() == True
        assert future_task.is_overdue() == False
    
    def test_get_time_remaining(self):
        """Prueba cálculo de tiempo restante"""
        user = User.objects.create_user(username='testuser', password='12345')
        
        # Tarea con 2 días de plazo
        task = Task.objects.create(
            title='Tarea con plazo',
            created_by=user,
            due_date=timezone.now() + timedelta(days=2)
        )
        
        remaining = task.get_time_remaining()
        assert remaining is not None
        assert 47 <= remaining <= 49  # Aproximadamente 48 horas
        
        # Tarea completada
        completed_task = Task.objects.create(
            title='Tarea completada',
            created_by=user,
            due_date=timezone.now() + timedelta(days=1),
            status='COMPLETED'
        )
        assert completed_task.get_time_remaining() is None