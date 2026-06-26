# tasks/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from tasks.models import Task

pytestmark = pytest.mark.django_db

class TestTaskAPI:
    
    @pytest.fixture
    def api_client(self):
        client = APIClient()
        return client
    
    @pytest.fixture
    def authenticated_client(self, api_client):
        user = User.objects.create_user(username='testuser', password='testpass123')
        api_client.force_authenticate(user=user)
        return api_client, user
    
    def test_create_task(self, authenticated_client):
        """Prueba creación de tarea vía API"""
        client, user = authenticated_client
        url = reverse('task-list')
        data = {
            'title': 'Nueva tarea',
            'description': 'Descripción de la tarea',
            'due_date': (timezone.now() + timedelta(days=3)).isoformat(),
            'priority': 2
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Nueva tarea'
        assert Task.objects.filter(created_by=user).count() == 1
    
    def test_complete_task(self, authenticated_client):
        """Prueba completar una tarea"""
        client, user = authenticated_client
        task = Task.objects.create(
            title='Tarea a completar',
            created_by=user,
            due_date=timezone.now() + timedelta(days=1)
        )
        
        url = reverse('task-complete', kwargs={'pk': task.pk})
        response = client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.status == 'COMPLETED'
        assert task.completed_at is not None
    
    def test_list_tasks(self, authenticated_client):
        """Prueba listar tareas del usuario"""
        client, user = authenticated_client
        
        # Crear tareas
        for i in range(3):
            Task.objects.create(
                title=f'Tarea {i}',
                created_by=user,
                due_date=timezone.now() + timedelta(days=i+1)
            )
        
        url = reverse('task-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
    
    def test_invalid_due_date(self, authenticated_client):
        """Prueba validación de fecha de vencimiento"""
        client, user = authenticated_client
        url = reverse('task-list')
        data = {
            'title': 'Tarea inválida',
            'description': 'Descripción',
            'due_date': (timezone.now() - timedelta(days=1)).isoformat()
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'due_date' in response.data