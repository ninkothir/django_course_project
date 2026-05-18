from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    hello,
    create_task,
    task_list,
    task_detail,
    task_stats,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskFilterView,
    TaskListCreateGenericView,
    TaskDetailGenericView,
    SubTaskListCreateGenericView,
    SubTaskDetailGenericView,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', hello, name='hello'),

    path('create-task/', create_task, name='create_task'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('task-stats/', task_stats, name='task_stats'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),

    path('tasks-filter/', TaskFilterView.as_view(), name='tasks-filter'),

    path('generic/tasks/', TaskListCreateGenericView.as_view(), name='generic-task-list-create'),
    path('generic/tasks/<int:pk>/', TaskDetailGenericView.as_view(), name='generic-task-detail'),

    path('generic/subtasks/', SubTaskListCreateGenericView.as_view(), name='generic-subtask-list-create'),
    path('generic/subtasks/<int:pk>/', SubTaskDetailGenericView.as_view(), name='generic-subtask-detail'),
] + router.urls