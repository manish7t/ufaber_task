from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, \
    CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework_jwt.settings import api_settings as token_settings
from rest_framework.settings import api_settings
from .serializers import *
from .models import *
from rest_framework import mixins
from django.contrib.auth import (authenticate, login as auth_login)
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

User = get_user_model()

# pagination setting for api view
pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
paginator = pagination_class()


@permission_classes([AllowAny])
class UserRegistration(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        data = request.data
        password = request.data['password']
        serailizer = UserRegistrationSerializer(data=data)

        if serailizer.is_valid():
            instance = serailizer.save()
            instance.set_password(password)
            instance.save()
        else:
            return Response({'status': 400, 'errors': serailizer.errors})

        # Token Generated after registration
        payload = token_settings.JWT_PAYLOAD_HANDLER(instance)
        token = token_settings.JWT_ENCODE_HANDLER(payload)
        return Response({'status': '200', 'token': token})


@permission_classes([AllowAny])
class UserLogin(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        username = request.data['username']
        password = request.data['password']

        print(username, password)
        serializer = UserLoginSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            payload = token_settings.JWT_PAYLOAD_HANDLER(user)
            token = token_settings.JWT_ENCODE_HANDLER(payload)
            return Response({'status': '200', 'token': token})

        return Response({'status': '400', 'errors': serializer.errors})


@permission_classes([IsAuthenticated])
class CreateListProjectView(CreateModelMixin, ListModelMixin, GenericAPIView):
    serializer_class = ProjectListSerializer
    queryset = Projects.objects.all()

    # get all
    def get(self, request, *args, **kwargs):
        return Response({'status': 200, 'data': self.list(request, *args, *kwargs).data})

    # create
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            app_user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            raise ValidationError({'error': 'Invalid User!!'})
        return serializer.save(app_user=app_user)


# Update,delete & Retrieve Project API
@permission_classes([IsAuthenticated])
class ProjectUpdateRetrieveView(UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericAPIView):
    serializer_class = ProjectsDetailSerializer
    queryset = Projects.objects.all()

    # get Ind
    def get(self, request, *args, **kwargs):
        return Response({'status': 200, 'data': self.retrieve(request, *args, **kwargs).data})

    def retrieve(self, *args, **kwargs):
        try:
            project_instance = Projects.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            return Response({'status': '400', 'error': 'Invalid Project !!'})
        serializer = ProjectListSerializer(project_instance)
        return Response(serializer.data)

    # update
    def perform_update(self, serializer):
        return serializer.save()

    def patch(self, request, *args, **kwargs):
        instance = get_object_or_404(Projects, id=kwargs.get('pk'))
        user = get_object_or_404(User, id=self.request.user.id)
        if user.is_superuser != 1:
            raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})
        return self.update(request, *args, **kwargs)

    # delete
    def perform_destroy(self, instance):

        user = User.objects.get(id=self.request.user.id)

        if user.is_superuser == 1:
            instance.delete()
        else:
            raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})

    def delete(self, request, *args, **kwargs):
        return Response(
            {'status': '200', 'msg': 'project deleted', 'data': self.destroy(request, *args, **kwargs).data})


# Task GET & POST
@permission_classes([IsAuthenticated])
class TaskCreateListTaskView(CreateModelMixin, ListModelMixin, GenericAPIView):
    serializer_class = TaskListSerializer
    queryset = ProjectTask.objects.all()

    # get
    def get(self, request, *args, **kwargs):
        self.queryset = ProjectTask.objects.filter(project_name_id=self.kwargs['project_id'])
        return self.list(request, *args, **kwargs)

    # create
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        try:
            project = Projects.objects.get(id=self.kwargs['project_id'])
        except ObjectDoesNotExist:
            raise ValidationError({'error': 'Project Not Found !!'})
        return serializer.save(project_name=project)


# Update,delete & Retrieve Project API
@permission_classes([IsAuthenticated])
class TaskUpdateRetrieveView(UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericAPIView):
    serializer_class = TaskDetailSerializer
    queryset = ProjectTask.objects.all()

    # get Ind
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        try:
            project_instance = ProjectTask.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            return Response({'status': '400', 'error': 'Invalid Task !!'})
        serializer = TaskListSerializer(project_instance)
        return Response(serializer.data)

    # update
    def perform_update(self, serializer):
        return serializer.save()

    def patch(self, request, *args, **kwargs):
        instance = get_object_or_404(Projects, id=kwargs.get('pk'))
        user = get_object_or_404(User, id=self.request.user.id)
        if user.is_superuser != 1:
            raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})
        return self.update(request, *args, **kwargs)

    # delete
    def perform_destroy(self, instance):

        user = User.objects.get(id=self.request.user.id)

        if user.is_superuser == 1:
            instance.delete()
        else:
            raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})

    def delete(self, request, *args, **kwargs):
        return Response(
            {'status': '200', 'msg': 'project deleted', 'data': self.destroy(request, *args, **kwargs).data})


# Task GET & POST
@permission_classes([IsAuthenticated])
class SubTaskCreateListTaskView(CreateModelMixin, ListModelMixin, GenericAPIView):
    serializer_class = SubTaskDetailSerializer
    queryset = SubTask.objects.all()

    # get
    def get(self, request, *args, **kwargs):
        self.queryset = SubTask.objects.filter(task_name_id=self.kwargs['task_id'])
        return self.list(request, *args, **kwargs)

    # create
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        try:
            task = ProjectTask.objects.get(id=self.kwargs.get('task_id'))
        except ObjectDoesNotExist:
            raise ValidationError({'error': 'Task Not Found !!'})
        return serializer.save(task_name=task)


# Update,delete & Retrieve Project API
@permission_classes([IsAuthenticated])
class SubTaskUpdateRetrieveView(UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericAPIView):
    serializer_class = SubTaskDetailSerializer
    queryset = SubTask.objects.all()

    # get Ind
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        try:
            task_instance = SubTask.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            return Response({'status': '400', 'error': 'Invalid Task !!'})
        serializer = SubTaskListSerializer(task_instance)
        return Response(serializer.data)

    # update
    def perform_update(self, serializer):
        return serializer.save()

    def patch(self, request, *args, **kwargs):
        instance = get_object_or_404(Projects, id=kwargs.get('pk'))
        user = get_object_or_404(User, id=self.request.user.id)
        if user.is_superuser != 1:
            raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})
        return self.update(request, *args, **kwargs)

    # delete
    def perform_destroy(self, instance):

        user = User.objects.get(id=self.request.user.id)

        if user.is_superuser == 1:
            instance.delete()
        else:
            raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})

    def delete(self, request, *args, **kwargs):
        return Response(
            {'status': '200', 'msg': 'Sub-Task deleted', 'data': self.destroy(request, *args, **kwargs).data})
