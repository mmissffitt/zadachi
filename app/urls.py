from django.urls import path
from . import views


urlpatterns = [
    path('tasks', views.TasksView.as_view()),
    path('tasks/undone', views.TasksUndoneView.as_view()),
    path('tasks/<int:id>', views.TaskByIdView.as_view()),
    path('tasks_by_tag/<int:tag_id>', views.TasksByTagView.as_view()),

    path('tags', views.TagsView.as_view()),
    path('tags/<int:id>', views.TagsByIdView.as_view()),

    path('tasks_tags', views.TasksTagsView.as_view()),
    path(
        'tasks_tags/<int:task_id>/<int:tag_id>',
        views.TasksTagsByIdView.as_view()
    ),
    path(
        'tasks_tags_by_task/<int:task_id>',
        views.TasksTagsByTaskView.as_view()
    ),
]
