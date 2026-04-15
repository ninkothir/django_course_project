from django.urls import path
from .views import hello, create_task, task_list, task_detail, task_stats

urlpatterns = [
    path("", hello, name="home"),
    path("api/tasks/create/", create_task, name="create_task"),
    path("api/tasks/", task_list, name="task_list"),
    path("api/tasks/<int:pk>/", task_detail, name="task_detail"),
    path("api/tasks/stats/", task_stats, name="task_stats"),
]