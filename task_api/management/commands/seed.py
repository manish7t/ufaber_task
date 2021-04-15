import datetime

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from task_api.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


# clear or delete previous data
def clear_data():
    User.objects.filter(email='admin@admin.com').delete()
    print("Deleted previous data !!!")


# create admin user
def create_admin():
    try:
        admin_user = User()
        admin_user.email = 'admin@admin.com'
        admin_user.username = 'admin@admin.com'
        admin_user.set_password('admin123')
        admin_user.is_superuser = 1
        admin_user.save()
        # message
        print("super user created!!")
    except IntegrityError:
        print("unable to create superuser !! please try again")


# create Project
def create_project():
    try:
        admin_user = User.objects.get(username='admin@admin.com')

        # create projects
        for i in range(0, 5):
            project = Projects()
            project.name = 'Test' + str(i)
            project.description = 'Test Description' + str(i)
            project.duration = 25
            project.app_user = admin_user
            project.save()
            # message
            print(" project Test ", + i, "created!!")
    except IntegrityError:
        print("unable to project test !! please try again")


# create tasks
def create_task():
    project_instances = Projects.objects.all()

    for object in project_instances:
        project_task = ProjectTask()
        project_task.project_name = object
        project_task.name = 'Project Task' + str(object.id)
        project_task.description = 'Project Description' + str(object.id)
        project_task.start_time = datetime.datetime.now()
        project_task.end_time = datetime.datetime.now()
        project_task.save()

        # message
        print(" Project Task ", + object.id, "created!!")


def create_sub_task():
    task_instance = ProjectTask.objects.all()

    for obj in task_instance:
        sub_task = SubTask()
        sub_task.task_name = obj
        sub_task.name = 'Sub Task' + str(obj.id)
        sub_task.description = 'Sub Description' + str(obj.id)
        sub_task.start_time = datetime.datetime.now()
        sub_task.end_time = datetime.datetime.now()
        sub_task.save()

        # message
        print(" Sub Task ", + obj.id, "created!!")


def run_seed(self, mode):
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # create admin user
    create_admin()

    # create project
    create_project()

    # create task
    create_task()

    # create sub task
    create_sub_task()
