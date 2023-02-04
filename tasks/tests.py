from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Task, Comment, Timer, TimerLog


class TestSetup(APITestCase):
    fixtures = ["users"]

    def setUp(self) -> None:
        self.register = reverse("token_register")
        self.login_url = reverse("token_obtain_pair")

        self.test_user1 = User.objects.create(
            first_name="George",
            last_name="Listru",
            email="george@example.com",
            username="george@example.com",
            password="parola123"
        )

        self.test_user2 = User.objects.create(
            first_name="Alexandru",
            last_name="exemplu",
            email="alexandru.exemplu@gmail.com",
            username="alexandru.exemplu@gmail.com",
            password="parola321"
        )
        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.test_user1)
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.test_user2)

        taskA = Task.objects.create(
            title="Task a",
            description="Description a",
            status="completed",
            user=self.test_user1
        )

        taskB = Task.objects.create(
            title="Task b",
            description="Description b",
            status="to do",
            user=self.test_user2
        )

        taskC = Task.objects.create(
            title="Task c",
            description="Description c",
            status="to do",
            user=self.test_user1
        )

        Comment.objects.create(
            text="Text 1",
            task=taskA,
            user=self.test_user1
        )
        Comment.objects.create(
            text="Text 2",
            task=taskB,
            user=self.test_user1
        )
        Comment.objects.create(
            text="Text 3",
            task=taskC,
            user=self.test_user2
        )
        Comment.objects.create(
            text="Text 4",
            task=taskA,
            user=self.test_user2
        )
        Comment.objects.create(
            text="Text 5",
            task=taskB,
            user=self.test_user2
        )
        Timer.objects.create(
            start_time=timezone.now(),
            task=taskA,
            user=self.test_user1
        )

        super().setUp()


class TestViews(TestSetup):
    def test_create_task(self):
        response = self.client1.post(
            reverse("task_item"),
            {
                "title": "Task 1",
                "description": "Description 1",
                "status": "todo",
            },
        )
        self.assertEqual(response.status_code, 201, "Task not created")

    def test_get_task(self):
        response = self.client1.get(reverse("task_item", args=[1]))
        self.assertEqual(response.status_code, 200, "Task not retrieved")

    def test_delete_task(self):
        response = self.client1.delete(reverse("task_item", args=[1]))
        self.assertEqual(response.status_code, 204, "Task not deleted")

    def test_create_comment(self, comment="Comment 1"):
        response = self.client1.post(reverse("task_item_comment", args=[1]), {"text": "Comment 1", })
        self.assertEqual(response.status_code, 201, "Comment not created")

    def test_get_comments(self):
        response = self.client1.get(reverse("task_comments", args=[2]))
        self.assertEqual(response.status_code, 200, "Comments not retrieved")

    def test_modify_task_completed(self):
        response=self.client1.put(reverse("task_item_status",args=[2]))
        self.assertEqual(response.status_code, 200, "Comment status not modified")

    def test_modify_task_owner(self):
        response=self.client1.put(reverse("task_item_owner", args=[2,2]))
        self.assertEqual(response.status_code, 200, "Comment owner not modified")

    def test_timer_start(self):
        response = self.client1.post(reverse("task_timer_start",args=[1]))
        self.assertEqual(response.status_code, 200, "Timer did not start")

    def test_timer_stop(self):
        response = self.client1.post(reverse("task_timer_stop", args=[1]))
        self.assertEqual(response.status_code, 200, "Timer did not stop")

    def test_create_timer_log(self):
        response = self.client1.post(reverse("task_timer_log", args=[1]),{
            "date":timezone.now(),
            "duration_minutes":50
        })
        self.assertEqual(response.status_code, 200, "Timer Log has not been created")

    def test_get_timers_logs(self):
        response = self.client1.get(reverse("task_timers", args=[1]))
        self.assertEqual(response.status_code, 200, "Timers Logs not retrieved")

    def test_get_tasks(self):
        response = self.client1.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200, "Tasks not retrieved")

    def test_get_completed_tasks(self):
        response = self.client1.get(reverse("completed_tasks"))
        self.assertEqual(response.status_code, 200, "Completed Tasks not retrieved")

    def test_get_top_tasks(self):
        response = self.client1.get(reverse("top_task_list"))
        self.assertEqual(response.status_code, 200, "Top Tasks not retrieved")

    def test_get_user_tasks(self):
        response = self.client1.get(reverse("user_tasks"))
        self.assertEqual(response.status_code, 200, "User Tasks not retrieved")

    def test_search_tasks(self):
        response = self.client1.get(reverse("search_tasks", args=["Task"]))
        self.assertEqual(response.status_code, 200, "Tasks not retrieved")

    def test_get_timers_logs_last_month(self):
        response = self.client1.get(reverse("task_timers_last_month"))
        self.assertEqual(response.status_code, 200, "Timers Logs not retrieved")