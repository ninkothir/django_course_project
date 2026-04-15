from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer


def hello(request):
    return HttpResponse("Hello Nina!")


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['GET'])
def task_stats(request):
    total_tasks = Task.objects.count()
    overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()
    status_counts = Task.objects.values('status').annotate(count=Count('status'))

    data = {
        "total_tasks": total_tasks,
        "overdue_tasks": overdue_tasks,
        "tasks_by_status": list(status_counts)
    }

    return Response(data)