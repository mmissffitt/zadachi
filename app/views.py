from json import loads
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Tasks, Tags
from .forms import TasksForm, TagsForm
from django.forms.models import model_to_dict


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
        return JsonResponse({'data': task_list})

    # POST /tasks
    def post(self, request):
        new_data = loads(request.body)
        form = TasksForm(new_data)
        if form.is_valid():
            task = form.save()
            return JsonResponse({
                'data': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'done': task.done,
                }
            }, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


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
        return JsonResponse({'data': task_list})


@method_decorator(csrf_exempt, name='dispatch')
class TaskByIdView(View):

    # GET /tasks/<id>
    def get(self, request, id):
        task = get_object_or_404(Tasks, id=id)
        return JsonResponse({
            'data': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done,
            }
        })

    # PUT /tasks/<id>
    def put(self, request, id):
        task = get_object_or_404(Tasks, id=id)
        new_data = loads(request.body)
        form = TasksForm(new_data, instance=task)
        if form.is_valid():
            form.save()
            return self.get(request, id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # PATCH /tasks/<id>
    def patch(self, request, id):
        task = get_object_or_404(Tasks, id=id)
        merged = model_to_dict(task)
        merged.update(loads(request.body))

        form = TasksForm(merged, instance=task)
        if form.is_valid():
            form.save()
            return self.get(request, id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # DELETE /tasks/<id>
    def delete(self, request, id):
        task = get_object_or_404(Tasks, id=id)
        task.delete()
        return JsonResponse({'status': 'ok'}, status=204)


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
        return JsonResponse({'data': task_list})


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
        return JsonResponse({'data': tag_list})

    # POST /tags
    def post(self, request):
        new_data = loads(request.body)
        form = TagsForm(new_data)
        if form.is_valid():
            tag = form.save()
            return JsonResponse({
                'data': {
                    'id': tag.id,
                    'name': tag.name
                }
            }, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TagsByIdView(View):

    # GET /tags/<id>
    def get(self, request, id):
        tag = get_object_or_404(Tags, id=id)
        return JsonResponse({'data': {'id': tag.id, 'name': tag.name}})

    # PUT /tags/<id>
    def put(self, request, id):
        tag = get_object_or_404(Tags, id=id)
        new_data = loads(request.body)
        form = TagsForm(new_data, instance=tag)
        if form.is_valid():
            form.save()
            return self.get(request, id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # PATCH /tags/<id>
    def patch(self, request, id):
        tag = get_object_or_404(Tags, id=id)
        merged = model_to_dict(tag)
        merged.update(loads(request.body))

        form = TagsForm(merged, instance=tag)
        if form.is_valid():
            form.save()
            return self.get(request, id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # DELETE /tags/<id>
    def delete(self, request, id):
        tag = get_object_or_404(Tags, id=id)
        tag.delete()
        return JsonResponse({'status': 'ok'}, status=204)


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
        return JsonResponse({'data': link_list})

    # POST /tasks_tags
    def post(self, request):
        new_data = loads(request.body)
        task_id = new_data.get('task_id')
        tag_id = new_data.get('tag_id')
        task = get_object_or_404(Tasks, id=task_id)
        tag = get_object_or_404(Tags, id=tag_id)
        task.tags.add(tag)
        return JsonResponse({
            'data': {
                'task_id': task.id,
                'tag_id': tag.id
            }
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class TasksTagsByIdView(View):

    # DELETE /tasks_tags/<task_id>/<tag_id>
    def delete(self, request, task_id, tag_id):
        task = get_object_or_404(Tasks, id=task_id)
        tag = get_object_or_404(Tags, id=tag_id)
        task.tags.remove(tag)
        return JsonResponse({'status': 'ok'}, status=204)


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
        return JsonResponse({'data': tag_list})
