# tasks/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_PROGRESS', 'En Progreso'),
        ('COMPLETED', 'Completada'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=1, choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')])
    
    def mark_as_completed(self):
        """Marca la tarea como completada"""
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save()
    
    def is_overdue(self):
        """Verifica si la tarea está vencida"""
        if self.status == 'COMPLETED':
            return False
        return timezone.now() > self.due_date
    
    def get_time_remaining(self):
        """Calcula el tiempo restante para la tarea"""
        if self.is_overdue() or self.status == 'COMPLETED':
            return None
        remaining = self.due_date - timezone.now()
        return remaining.total_seconds() / 3600  # Horas restantes