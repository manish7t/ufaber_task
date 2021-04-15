from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer, ValidationError, CharField)
from .models import *

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        email = data.get("email")

        if not email:
            raise ValidationError("Please Enter Your E-Mail !!!!")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProjectsDetailSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['name', 'description', 'image', 'duration']


class ProjectListSerializer(ModelSerializer):
    app_user = UserDetailSerializer(read_only=True, many=False)

    class Meta:
        model = Projects
        fields = ['id', 'name', 'description', 'image', 'duration', 'app_user', 'update_time', 'upload_time']


class TaskDetailSerializer(ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = ['name', 'description', 'start_time', 'end_time']


class TaskListSerializer(ModelSerializer):
    project_name = ProjectListSerializer(read_only=True, many=False)

    class Meta:
        model = ProjectTask
        fields = ['id', 'name', 'description', 'start_time', 'end_time', 'update_time', 'upload_time', 'project_name']


class SubTaskDetailSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['name', 'description', 'start_time', 'end_time']


class SubTaskListSerializer(ModelSerializer):
    task_name = TaskListSerializer(read_only=True, many=False)

    class Meta:
        model = SubTask
        fields = ['id', 'name', 'description', 'start_time', 'end_time', 'update_time', 'upload_time', 'task_name']
