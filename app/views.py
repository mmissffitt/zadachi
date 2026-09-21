from json import loads
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Tasks, Tags
from .forms import TasksForm, TagsForm


@method_decorator(csrf_exempt, name='dispatch')
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
        new_data = loads(request.body)
        form = TasksForm(new_data)
        if form.is_valid():
            task = form.save()
            obj = {
                'data': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'done': task.done,
                }
            }
            return JsonResponse(obj, status=201)
        return JsonResponse(
            {'status': 'error', 'code': 400},
            status=400
        )

    def patch(self, request):
        pass

    def delete(self, request):
        pass

@method_decorator(csrf_exempt, name='dispatch')
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

@method_decorator(csrf_exempt, name='dispatch')
class TaskByIdView(View):
    def get(self, request, id):
        task = Tasks.objects.filter(id=id).first()
        if not task:
            return JsonResponse({'error': 'Not Found'}, status=404)
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
        task = Tasks.objects.filter(id=id).first()
        if not task:
            return JsonResponse({'error': 'Not Found'}, status=404)
        new_data = loads(request.body)
        form = TasksForm(new_data, instance=task)
        if form.is_valid():
            task = form.save()
            obj = {
                'data': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'done': task.done,
                }
            }
            return JsonResponse(obj)
        return JsonResponse(
            {'status': 'error', 'code': 400},
            status=400
        )

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass

@method_decorator(csrf_exempt, name='dispatch')
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

@method_decorator(csrf_exempt, name='dispatch')
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
        new_data = loads(request.body)
        form = TagsForm(new_data)
        if form.is_valid():
            tag = form.save()
            obj = {'data': {'id': tag.id, 'name': tag.name}}
            return JsonResponse(obj, status=201)
        return JsonResponse(
            {'status': 'error', 'code': 400},
            status=400
        )

    def patch(self, request):
        pass

    def delete(self, request):
        pass

@method_decorator(csrf_exempt, name='dispatch')
class TagsByIdView(View):
    def post(self, request, id):
        tag = Tags.objects.filter(id=id).first()
        if not tag:
            return JsonResponse({'error': 'Not Found'}, status=404)
        new_data = loads(request.body)
        form = TagsForm(new_data, instance=tag)
        if form.is_valid():
            tag = form.save()
            obj = {'data': {'id': tag.id, 'name': tag.name}}
            return JsonResponse(obj)
        return JsonResponse(
            {'status': 'error', 'code': 400},
            status=400
        )

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass

@method_decorator(csrf_exempt, name='dispatch')
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
        new_data = loads(request.body)
        task_id = new_data.get('task_id')
        tag_id = new_data.get('tag_id')

        task = Tasks.objects.filter(id=task_id).first()
        tag = Tags.objects.filter(id=tag_id).first()

        if not task or not tag:
            return JsonResponse(
                {'status': 'error', 'code': 404},
                status=404
            )

        task.tags.add(tag)
        obj = {'data': {'task_id': task.id, 'tag_id': tag.id}}
        return JsonResponse(obj, status=201)

    def patch(self, request):
        pass

    def delete(self, request):
        pass

@method_decorator(csrf_exempt, name='dispatch')
class TasksTagsByIdView(View):

    def delete(self, request, task_id, tag_id):
        pass

@method_decorator(csrf_exempt, name='dispatch')
class TasksTagsByTaskView(View):
    def get(self, request, task_id):
        task = Tasks.objects.filter(id=task_id).first()
        if not task:
            return JsonResponse({'error': 'Not Found'}, status=404)
        tag_list = []
        for tag in task.tags.all():
            tag_list.append({
                'id': tag.id,
                'name': tag.name,
            })
        obj = {'data': tag_list}
        return JsonResponse(obj)