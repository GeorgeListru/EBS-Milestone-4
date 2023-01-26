from django.urls import path

from .views import TaskItemView, TaskListView, CreateTaskItemView, UserTaskListView, CompletedTaskListView, \
    ModifyTaskOwnerView, ModifyTaskStatusView, AddCommentView, CommentsListView, SearchTaskView, TimerItemStartView, \
    TimerItemStopView, TimerLogItemView, TimerLogListView, TimerLogLastMonthView, Top20TasksView

urlpatterns = [
    path("task", CreateTaskItemView.as_view(), name="task_item"),
    path('tasks/user', UserTaskListView.as_view(), name='user_tasks'),
    path('tasks/completed', CompletedTaskListView.as_view(), name='completed_tasks'),
    path("task/<int:task_id>", TaskItemView.as_view(), name="task_item"),
    path("task/<int:task_id>/owner/<int:user_id>", ModifyTaskOwnerView.as_view(), name="task_item"),
    path("task/<int:task_id>/completed", ModifyTaskStatusView.as_view(), name="task_item"),
    path("task/<int:task_id>/comment", AddCommentView.as_view(), name="task_item"),
    path('task/<int:task_id>/comments', CommentsListView.as_view(), name='task_comments'),
    path('task/<int:task_id>/timer-start', TimerItemStartView.as_view(), name='task_timer_start'),
    path('task/<int:task_id>/timer-stop', TimerItemStopView.as_view(), name='task_timer_stop'),
    path('task/<int:task_id>/timer-log', TimerLogItemView.as_view(), name='task_timer_log'),
    path('task/<int:task_id>/timers', TimerLogListView.as_view(), name='task_timers'),
    path('time/last-month', TimerLogLastMonthView.as_view(), name='task_timers'),
    path('tasks/top-20', Top20TasksView.as_view(), name='task_list'),
    path("tasks/<str:q>", SearchTaskView.as_view(), name="task_item"),
    path("tasks", TaskListView.as_view(), name="task_list"),
]