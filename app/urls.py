from django.urls import path
from . import views

urlpatterns = [
    path('tasks', views.TasksView.as_view()),                       # GET все, POST создать
    path('tasks/undone', views.TasksUndoneView.as_view()),          # GET невыполненные
    path('tasks/<int:id>', views.TaskByIdView.as_view()),           # GET одна, PUT, PATCH, DELETE
    path('tasks_by_tag/<int:tag_id>', views.TasksByTagView.as_view()),  # GET задачи по тегу

    path('tags', views.TagsView.as_view()),                         # GET все, POST создать
    path('tags/<int:id>', views.TagsByIdView.as_view()),            # PUT, DELETE

    path('tasks_tags', views.TasksTagsView.as_view()),              # GET все, POST создать
    path('tasks_tags/<int:task_id>/<int:tag_id>', views.TasksTagsByIdView.as_view()),  # DELETE
    path('tasks_tags_by_task/<int:task_id>', views.TasksTagsByTaskView.as_view()),      # GET теги задачи
]