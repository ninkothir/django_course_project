from myapp.models import Task, SubTask
from datetime import datetime, timedelta

# CREATE
task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="new",
    deadline=datetime.now() + timedelta(days=3)
)

SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="new",
    deadline=datetime.now() + timedelta(days=2),
    task=task
)

SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="new",
    deadline=datetime.now() + timedelta(days=1),
    task=task
)

# READ
Task.objects.filter(status="new")
SubTask.objects.filter(status="done", deadline__lt=datetime.now())

# UPDATE
task = Task.objects.get(title="Prepare presentation")
task.status = "in_progress"
task.save()

sub = SubTask.objects.get(title="Gather information")
sub.deadline = datetime.now() - timedelta(days=2)
sub.save()

sub = SubTask.objects.get(title="Create slides")
sub.description = "Create and format presentation slides"
sub.save()

# DELETE
task = Task.objects.get(title="Prepare presentation")
task.delete()