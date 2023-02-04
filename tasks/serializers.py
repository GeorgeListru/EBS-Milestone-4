from .models import Task, Comment, Timer, TimerLog

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


class TaskSerializerDuration(serializers.ModelSerializer):
    duration = serializers.IntegerField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'duration')


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
        fields = ('id', 'text', 'task', "user")


class CommentSerializerText(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')


class CommentSerializerId(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',)


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = "__all__"


class TimerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerLog
        fields = "__all__"


class AddTimerLogSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    duration_minutes = serializers.IntegerField()

    class Meta:
        model = TimerLog
        fields = ('id', 'date', 'duration_minutes')
