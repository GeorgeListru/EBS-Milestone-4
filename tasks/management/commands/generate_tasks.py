from random import randint
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from ...models import Task


class Command(BaseCommand):
    help = 'Generate tasks'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='The user id to assign tasks to')

    def handle(self, *args, **options):
        user = User.objects.get(id=options['user_id'])
        if user:
            for i in range(25000):
                Task.objects.create(
                    title=get_random_string(10),
                    description=get_random_string(100),
                    status="to do" if randint(0, 1) else "completed",
                    user=user
                )
            self.stdout.write(self.style.SUCCESS('25000 tasks created successfully!'))
        else:
            self.stdout.write(self.style.ERROR('User not found'))
