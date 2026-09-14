from django.http import JsonResponse
from django.views import View
from .models import Tasks, Tags

# задачи
class TasksView(View):
    def get(self, request):
        tasks = Tasks.objects.all()
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done,
            })
        obj = {'data': task_list}
        return JsonResponse(obj)

    def post(self, request):
        pass


class TasksUndoneView(View):
    def get(self, request):
        tasks = Tasks.objects.filter(done=False)
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done,
            })
        obj = {'data': task_list}
        return JsonResponse(obj)


class TaskByIdView(View):
    def get(self, request, id):
        task = Tasks.objects.filter(id=id).first()
        if not task:
            return JsonResponse({'error': 'Not found'}, status=404)
        obj = {
            'data': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done,
            }
        }
        return JsonResponse(obj)

    def put(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass


class TasksByTagView(View):
    def get(self, request, tag_id):
        tasks = Tasks.objects.filter(tags__id=tag_id)
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done,
            })
        obj = {'data': task_list}
        return JsonResponse(obj)


# теги

class TagsView(View):
    def get(self, request):
        tags = Tags.objects.all()
        tag_list = []
        for tag in tags:
            tag_list.append({
                'id': tag.id,
                'name': tag.name,
            })
        obj = {'data': tag_list}
        return JsonResponse(obj)

    def post(self, request):
        pass


class TagsByIdView(View):
    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass

# теги в задачах

class TasksTagsView(View):
    def get(self, request):
        tasks = Tasks.objects.prefetch_related('tags').all()
        link_list = []
        for task in tasks:
            for tag in task.tags.all():
                link_list.append({
                    'task_id': task.id,
                    'tag_id': tag.id,
                })
        obj = {'data': link_list}
        return JsonResponse(obj)

    def post(self, request):
        pass


class TasksTagsByIdView(View):
    def delete(self, request, id):
        pass


class TasksTagsByTaskView(View):
    def get(self, request, task_id):
        task = Tasks.objects.filter(id=task_id).first()
        if not task:
            return JsonResponse({'error': 'Not found'}, status=404)
        tag_list = []
        for tag in task.tags.all():
            tag_list.append({
                'id': tag.id,
                'name': tag.name,
            })
        obj = {'data': tag_list}
        return JsonResponse(obj)