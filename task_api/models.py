from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Projects(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    duration = models.IntegerField()  # days
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True)


class AbstractTask(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True


class ProjectTask(AbstractTask):
    project_name = models.ForeignKey(Projects, on_delete=models.CASCADE)


class SubTask(AbstractTask):
    task_name = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
