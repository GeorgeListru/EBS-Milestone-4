from django.urls import path

from .views import TaskItemView, TaskListView, CreateTaskItemView, UserTaskListView, CompletedTaskListView, \
    ModifyTaskOwnerView, ModifyTaskStatusView, AddCommentView, CommentsListView, SearchTaskView

urlpatterns = [
    path("task", CreateTaskItemView.as_view(), name="task_item"),
    path('user-tasks', UserTaskListView.as_view(), name='user_tasks'),
    path('completed-tasks', CompletedTaskListView.as_view(), name='completed_tasks'),
    path("task/<int:task_id>", TaskItemView.as_view(), name="task_item"),
    path("task/<int:task_id>/owner/<int:user_id>", ModifyTaskOwnerView.as_view(), name="task_item"),
    path("task/<int:task_id>/completed", ModifyTaskStatusView.as_view(), name="task_item"),
    path("task/<int:task_id>/comment", AddCommentView.as_view(), name="task_item"),
    path('task/<int:task_id>/comments', CommentsListView.as_view(), name='task_comments'),
    path("tasks/<str:q>", SearchTaskView.as_view(), name="task_item"),
    path("tasks", TaskListView.as_view(), name="task_list"),
]