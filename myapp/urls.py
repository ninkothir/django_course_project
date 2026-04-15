from django.urls import path
from .views import (
    hello,
    create_task,
    task_list,
    task_detail,
    task_stats,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('', hello, name='hello'),
    path('create-task/', create_task, name='create_task'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('task-stats/', task_stats, name='task_stats'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]