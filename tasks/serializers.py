# tasks/serializers.py
from rest_framework import serializers
from tasks.models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 
                 'priority', 'time_remaining', 'is_overdue']
    
    def get_time_remaining(self, obj):
        return obj.get_time_remaining()
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()
    
    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La fecha de vencimiento no puede ser en el pasado")
        return value