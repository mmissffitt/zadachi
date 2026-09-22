from json import loads
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Tasks, Tags
from .forms import TasksForm, TagsForm
from django.shortcuts import get_object_or_404


@method_decorator(csrf_exempt, name='dispatch')
class TasksView(View):

    # GET /tasks
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

        obj = {
            'data': task_list
        }

        return JsonResponse(obj)

    # POST /tasks
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
            {
                'status': 'error',
                'code': 400
            },
            status=400
        )

    def patch(self, request):
        pass

    def delete(self, request):
        pass


class TasksUndoneView(View):

    # GET /tasks/undone
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

        obj = {
            'data': task_list
        }

        return JsonResponse(obj)


@method_decorator(csrf_exempt, name='dispatch')
class TaskByIdView(View):

    # GET /tasks/<id>
    def get(self, request, id):
        task = get_object_or_404(Tasks, id=id)

        obj = {
            'data': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done,
            }
        }

        return JsonResponse(obj)

    # PUT /tasks/<id>
    def put(self, request, id):
        task = get_object_or_404(Tasks, id=id)
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
            {
                'status': 'error',
                'code': 400
            },
            status=400
        )

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass


class TasksByTagView(View):

    # GET /tasks_by_tag/<tag_id>
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

        obj = {
            'data': task_list
        }

        return JsonResponse(obj)


@method_decorator(csrf_exempt, name='dispatch')
class TagsView(View):

    # GET /tags
    def get(self, request):
        tags = Tags.objects.all()

        tag_list = []

        for tag in tags:
            tag_list.append({
                'id': tag.id,
                'name': tag.name,
            })

        obj = {
            'data': tag_list
        }

        return JsonResponse(obj)

    # POST /tags
    def post(self, request):
        new_data = loads(request.body)

        form = TagsForm(new_data)

        if form.is_valid():
            tag = form.save()

            obj = {
                'data': {
                    'id': tag.id,
                    'name': tag.name
                }
            }

            return JsonResponse(obj, status=201)

        return JsonResponse({'status': 'error','code': 400}, status=400)

    def patch(self, request):
        pass

    def delete(self, request):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class TagsByIdView(View):

    # GET /tags/<id>
    def get(self, request, id):
        tag = get_object_or_404(Tags, id=id)
        return JsonResponse({'data': {'id': tag.id,'name': tag.name}})

    # PUT /tags/<id>
    def put(self, request, id):
        tag = get_object_or_404(Tags, id=id)
        new_data = loads(request.body)

        form = TagsForm(new_data, instance=tag)

        if form.is_valid():
            tag = form.save()

            return JsonResponse({'data': 
                                 {'id': tag.id,
                                  'name': tag.name}})

        return JsonResponse({'status': 'error','code': 400}, status=400)

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class TasksTagsView(View):

    # GET /tasks_tags
    def get(self, request):
        tasks = Tasks.objects.prefetch_related('tags').all()

        link_list = []

        for task in tasks:
            for tag in task.tags.all():
                link_list.append({
                    'task_id': task.id,
                    'tag_id': tag.id,
                })

        obj = {
            'data': link_list
        }

        return JsonResponse(obj)

    # POST /tasks_tags
    def post(self, request):
        new_data = loads(request.body)
        task_id = new_data.get('task_id')
        tag_id = new_data.get('tag_id')
        task = get_object_or_404(Tasks, id=task_id)
        tag = get_object_or_404(Tags, id=tag_id)

        task.tags.add(tag)

        obj = {
            'data': {
                'task_id': task.id,
                'tag_id': tag.id
            }
        }

        return JsonResponse(obj, status=201)

    def patch(self, request):
        pass

    def delete(self, request):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class TasksTagsByIdView(View):

    def patch(self, request, task_id, tag_id):
        pass

    def delete(self, request, task_id, tag_id):
        pass


class TasksTagsByTaskView(View):

    # GET /tasks_tags_by_task/<task_id>
    def get(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)

        tag_list = []

        for tag in task.tags.all():
            tag_list.append({
                'id': tag.id,
                'name': tag.name,
            })

        obj = {
            'data': tag_list
        }

        return JsonResponse(obj)
