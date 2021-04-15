from . import views
from django.urls import re_path

urlpatterns = [

    # User Registration And Login
    re_path(r'^register/', views.UserRegistration.as_view(), name='user-registration'),  # POST
    re_path(r'^login/', views.UserLogin.as_view(), name='login'),  # POST

    # Project CRUD-URL
    re_path(r'^create-list-project/', views.CreateListProjectView.as_view(), name='create-content'), # POST , GET
    re_path(r'^update-retrieve-project/(?P<pk>\d+)/', views.ProjectUpdateRetrieveView.as_view(), name='create-content'),  # POST #GET #PATCH #DELETE

    # Task CRUD-URL
    re_path(r'^create-list-task/(?P<project_id>\d+)', views.TaskCreateListTaskView.as_view(), name='create-content'),  # POST , GET
    re_path(r'^update-retrieve-task/(?P<pk>\d+)/', views.TaskUpdateRetrieveView.as_view(), name='create-content'), # POST #GET #PATCH #DELETE

    # Sub Task CRUD-URL
    re_path(r'^create-list-subtask/(?P<task_id>\d+)', views.SubTaskCreateListTaskView.as_view(), name='create-content'),# POST , GET
    re_path(r'^update-retrieve-subtask/(?P<pk>\d+)/', views.SubTaskUpdateRetrieveView.as_view(), name='create-content'),# POST #GET #PATCH #DELETE

]
