import factory
from django.contrib.auth.models import User
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text', max_nb_chars=200)
    status = 'PENDING'
    created_by = factory.SubFactory(UserFactory)
    due_date = factory.LazyFunction(lambda: timezone.now() + timedelta(days=5))
    priority = 2