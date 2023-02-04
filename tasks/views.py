from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Task, Comment, Timer, TimerLog
from .serializers import TaskSerializer, TaskSerializerWithUser, TaskSerializerTitle, TaskSerializerDescription, \
    CommentSerializer, CommentSerializerText, TimerSerializer, AddTimerLogSerializer, TimerLogSerializer, \
    TaskSerializerDuration
from .utils import send_email


class CreateTaskItemView(GenericAPIView):
    serializer_class = TaskSerializerDescription

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        user = request.user
        task = Task.objects.create(title=title, description=description, user=user)
        task.save()
        return Response({'task_id': task.id}, status=201)


class TaskItemView(GenericAPIView):
    serializer_class = TaskSerializerWithUser

    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        serialized_task = TaskSerializerWithUser(task)
        return Response(serialized_task.data)

    def delete(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response({'message': 'Task deleted'}, status=204)


class UserTaskListView(GenericAPIView):
    serializer_class = TaskSerializerTitle

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(user=user)
        if tasks:
            serialized_task = TaskSerializerTitle(tasks, many=True)
            return Response(serialized_task.data)
        return Response({'message': 'No tasks found'})


class CompletedTaskListView(GenericAPIView):
    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(user=user, status="completed")
        if tasks:
            serialized_task = TaskSerializerTitle(tasks, many=True)
            return Response(serialized_task.data)
        return Response({'message': 'No tasks found'})


class TaskListView(GenericAPIView):
    serializer_class = TaskSerializerTitle

    def get(self, request):
        tasks = Task.objects.all()
        serialized_task = TaskSerializerTitle(tasks, many=True)
        for i in range(len(tasks)):
            timers = TimerLog.objects.filter(task=tasks[i])
            total_duration = 0
            for timer in timers:
                start_time = timer.start_time
                end_time = timer.end_time
                duration = end_time - start_time
                duration_in_minutes = duration.total_seconds() // 60
                total_duration += duration_in_minutes
            serialized_task.data[i]['duration'] = total_duration
        return Response(serialized_task.data)


class ModifyTaskOwnerView(GenericAPIView):
    def put(self, request, task_id, user_id):
        task = Task.objects.get(id=task_id)
        user = User.objects.get(id=user_id)
        task.user = user
        task.save()

        title = "You have been assigned a new task"
        message = "You have been assigned a new task: " + task.title
        name = user.first_name + " " + user.last_name
        send_email(name, title, message, user.email)

        return Response({'message': 'Task owner changed'})


class ModifyTaskStatusView(GenericAPIView):
    def put(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.status = "completed"

        comments = Comment.objects.filter(task=task)
        users = [comment.task.user for comment in comments]
        emails = [user.email for user in users]
        title = "Task completed"
        message = 'Task "' + task.title + '" by ' + task.user.first_name + " " + task.user.last_name + " has been completed!"
        for email in emails:
            send_email(task.user.first_name + " " + task.user.last_name, title, message, email)

        return Response({'message': 'Task status changed'})


class AddCommentView(GenericAPIView):
    serializer_class = CommentSerializerText

    def post(self, request, task_id):
        text = request.data.get('text')
        task = Task.objects.get(id=task_id)
        user = request.user
        comment = Comment.objects.create(text=text, task=task, user=user)
        comment.save()

        if user.email:
            title = "You have a new comment"
            message = "You have a new comment by " + request.user.first_name + " " + request.user.last_name + " on task: " + task.title
            message += ". Comment: " + text
            name = user.first_name + " " + user.last_name
            send_email(name, title, message, user.email)

        return Response({'comment_id': comment.id}, status=201)


class CommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task=task_id)


class SearchTaskView(GenericAPIView):
    def get(self, request, q):
        if len(q) > 3:
            tasks = Task.objects.filter(title__icontains=q)
            if tasks:
                serialized_task = TaskSerializer(tasks, many=True)
                return Response(serialized_task.data)
            return Response({'message': 'No tasks found'})
        return Response({'message': 'Invalid query'})


class TimerItemStartView(GenericAPIView):
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        timer = Timer.objects.get(task=task, user=request.user)
        if not timer:
            timer = Timer.objects.create(task=task, start_time=timezone.now(), end_time=None, user=request.user)
        else:
            timer.start_time = timezone.now()
            timer.end_time = None
        timer.save()
        return Response({"message": "Timer started"})


class TimerItemStopView(GenericAPIView):
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        timer = Timer.objects.get(task=task, user=request.user)
        timer.stop_time = timezone.now()
        timer.save()
        timer_log = TimerLog.objects.create(task=task, start_time=timer.start_time, end_time=timer.stop_time,
                                            user=request.user)
        timer_log.save()
        return Response({'timer_log_id': timer_log.id})


class TimerLogItemView(GenericAPIView):
    serializer_class = AddTimerLogSerializer

    def post(self, request, task_id):
        date = request.data.get('date')
        try:
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f%z')
        duration_minutes = int(request.data.get('duration_minutes'))
        task = Task.objects.get(id=task_id)
        timer_log = TimerLog.objects.create(task=task, start_time=date,
                                            end_time=date + timedelta(minutes=duration_minutes),
                                            user=request.user)
        timer_log.save()
        return Response({'timer_log_id': timer_log.id})


class TimerLogListView(generics.ListAPIView):
    serializer_class = TimerLogSerializer

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return TimerLog.objects.filter(task=task_id)


class TimerLogLastMonthView(GenericAPIView):

    def get(self, request):
        utc = pytz.UTC
        timer_logs = TimerLog.objects.filter(user=request.user)
        last_month = datetime.now() - timedelta(days=30)

        timer_logs_last_month = [timer_log for timer_log in timer_logs
                                 if timer_log.start_time.replace(tzinfo=utc) > last_month.replace(tzinfo=utc)]

        total_duration = 0
        for timer_log in timer_logs_last_month:
            duration = timer_log.end_time - timer_log.start_time
            duration_in_minutes = duration.total_seconds() // 60
            total_duration += duration_in_minutes
        return Response({'total_time_minutes': total_duration})


class Top20TasksView(GenericAPIView):
    serializer_class = TaskSerializerDuration

    def get(self, request):
        utc = pytz.UTC
        timer_logs = TimerLog.objects.all()
        last_month = datetime.now() - timedelta(days=30)
        timer_logs_last_month = [timer_log for timer_log in timer_logs
                                 if timer_log.start_time.replace(tzinfo=utc) > last_month.replace(tzinfo=utc)]
        tasks = Task.objects.all()

        tasks_duration = []
        for task in tasks:
            duration = 0
            for timer_log in timer_logs_last_month:
                if timer_log.task == task:
                    duration += (timer_log.end_time - timer_log.start_time).total_seconds() // 60
            tasks_duration.append({'task': task, 'duration': duration})
        tasks_duration.sort(key=lambda x: x['duration'])
        tasks_duration = tasks_duration[:20]

        tasks = [task_duration['task'] for task_duration in tasks_duration]
        serialized_tasks = TaskSerializerTitle(tasks, many=True)

        for task in serialized_tasks.data:
            for task_duration in tasks_duration:
                if task_duration['task'].id == task['id']:
                    task['duration'] = task_duration['duration']

        return Response(serialized_tasks.data)
