from django.contrib.auth.models import User
from django.core.management import BaseCommand
from ...models import TimerLog, Task
import random
from django.utils import timezone


class Command(BaseCommand):
    help = 'Generate time logs'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='The user id to generate time logs for')
        parser.add_argument('task_id', type=int, help='The task id to generate time logs for')

    def handle(self, *args, **options):
        user = User.objects.get(id=options['user_id'])
        task = Task.objects.get(id=options['task_id'])
        if user and task:
            for i in range(25000):
                TimerLog.objects.create(
                    start_time=timezone.now(),
                    end_time=timezone.now(),
                    task=random.randint(1, 25000),
                    user=user
                )
            self.stdout.write(self.style.SUCCESS('25000 time logs created successfully!'))
        else:
            self.stdout.write(self.style.ERROR('User or task not found'))
