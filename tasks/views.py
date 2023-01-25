from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Task, Comment
from .serializers import TaskSerializer, TaskSerializerWithUser, TaskSerializerTitle, TaskSerializerDescription, \
    CommentSerializer, CommentSerializerText
from .utils import send_email


class CreateTaskItemView(GenericAPIView):
    serializer_class = TaskSerializerDescription

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        user = request.user
        task = Task.objects.create(title=title, description=description, user=user)
        task.save()
        return Response({'task_id': task.id})


class TaskItemView(GenericAPIView):
    serializer_class = TaskSerializerWithUser

    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        serialized_task = TaskSerializerWithUser(task)
        return Response(serialized_task.data)

    def delete(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response({'message': 'Task deleted'})


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


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializerTitle

    def get_queryset(self):
        return Task.objects.all()


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
        comment = Comment.objects.create(text=text, task=task)
        comment.save()

        user = task.user
        if user.email != request.user.email:
            title = "You have a new comment"
            message = "You have a new comment by " + request.user.first_name + " " + request.user.last_name + " on task: " + task.title
            message += ". Comment: " + text
            name = user.first_name + " " + user.last_name
            send_email(name, title, message, user.email)

        return Response({'comment_id': comment.id})


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
