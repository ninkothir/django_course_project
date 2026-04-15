from django.contrib import admin
from .models import Category, Task, SubTask


# INLINE (Задание 1)
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


# CATEGORY
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


# TASK
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "short_title", "status", "created_at")
    inlines = [SubTaskInline]

    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title

    short_title.short_description = "Title"


# SUBTASK
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status")
    actions = ["mark_as_done"]

    def mark_as_done(self, request, queryset):
        queryset.update(status="done")

    mark_as_done.short_description = "Mark selected subtasks as Done"