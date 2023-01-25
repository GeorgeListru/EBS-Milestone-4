from .models import Task, Comment

from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status')


class TaskSerializerWithUser(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'user')


class TaskSerializerTitle(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title')


class TaskSerializerDescription(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description')


class TaskSerializerUser(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'user')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'task')


class CommentSerializerText(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')


class CommentSerializerId(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',)