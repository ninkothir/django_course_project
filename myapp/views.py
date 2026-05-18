from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer
from django.db.models.functions import ExtractWeekDay
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters


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
            data={"error": "Task not found"},
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
        'total_tasks': total_tasks,
        'overdue_tasks': overdue_tasks,
        'tasks_by_status': list(status_counts)
    }

    return Response(data)


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(
                {'error': 'SubTask not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(
                {'error': 'SubTask not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(
                {'error': 'SubTask not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskPagination(PageNumberPagination):
        page_size = 5

class TaskFilterView(APIView, TaskPagination):
        def get(self, request):
            tasks = Task.objects.all().order_by('-deadline')

            weekday = request.query_params.get('weekday')
            if weekday:
                tasks = tasks.annotate(
                    week_day=ExtractWeekDay('deadline')
                ).filter(week_day=weekday)

            results = self.paginate_queryset(tasks, request, view=self)
            serializer = TaskSerializer(results, many=True)

            return self.get_paginated_response(serializer.data)

class TaskListCreateGenericView(ListCreateAPIView):
            queryset = Task.objects.all()
            serializer_class = TaskSerializer
            filter_backends = [filters.SearchFilter, filters.OrderingFilter]
            search_fields = ['title', 'description']
            ordering_fields = ['created_at', 'deadline', 'status']

class TaskDetailGenericView(RetrieveUpdateDestroyAPIView):
            queryset = Task.objects.all()
            serializer_class = TaskSerializer

class SubTaskListCreateGenericView(ListCreateAPIView):
            queryset = SubTask.objects.all()
            serializer_class = SubTaskSerializer
            filter_backends = [filters.SearchFilter, filters.OrderingFilter]
            search_fields = ['title', 'description']
            ordering_fields = ['created_at', 'deadline', 'status']

class SubTaskDetailGenericView(RetrieveUpdateDestroyAPIView):
            queryset = SubTask.objects.all()
            serializer_class = SubTaskSerializer