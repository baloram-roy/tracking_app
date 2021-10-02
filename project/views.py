# import from python:
from datetime import datetime, timedelta


# import from django:

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Entry, Project, Task

# Create your views here.


# Home view:
#
def home(request):
    task = Task.objects.all()
    project = Project.objects.all()
    entry = Entry.objects.all()
    
    list = []
    for i in range(0, 7):
        time = (datetime.today() + timedelta(i))
        list.append(time)

    context = {
        'tasks': task,
        'entrys':entry,
        'date': list,
        'project': project 
    }
    return render(request, 'project/index.html',context)


def project_list_create(request):
    project = Project.objects.all()  # this is for list all the project

    # this section is for creating project in the same page
    if request.method == 'POST':
        title = request.POST.get('title')
        client_name = request.POST.get('client_name')
        if title and client_name:
            project = Project.objects.create(
                title=title,
                client_name=client_name,
                created_by=request.user
            )
            project.save()

            return redirect('project_list')

    context = {'object_list': project}
    return render(request, 'project/project_list.html', context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # this down section is for creating task in the project detail page
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)

        if title:
            task_create = Task.objects.create(
                name=title, project=project, created_by=request.user)
            return redirect('project_detail', pk=project.id)

    task_runing = project.task.filter(status=Task.RUNING)
    task_done = project.task.filter(status=Task.DONE)

    context = {
        'project': project,
        'task_runing': task_runing,
        'task_done': task_done
    }

    return render(request, 'project/project_details.html', context)

# class ProjectListView(ListView):
#     model = Project
#     template_name = "project/project_list.html"


# class ProjectDetailView(DetailView):
#     model = Project
#     template_name = "project/project_details.html"


# class ProjectCreateView(CreateView):
#     model = Project
#     template_name = "project/project_create.html"
#     fields = ['title', 'client_name']
#     success_url = reverse_lazy('project_list')

#     def form_valid(self, form: Project):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = "project/project_update.html"
    fields = ['title', 'client_name']
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     project = self.get_object()
    #     if self.request.user == project.created_by:
    #         return True
    #     return False


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()

    return redirect('project_list')

# Task section start here:
###################
##################


def task_detail(request, pk, task_id):
    project = get_object_or_404(Project, pk=pk)
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        hours = int(request.POST.get('hours'))
        minutes = int(request.POST.get('minutes'))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())

        minutes_total = (hours * 60) + minutes

        entry = Entry.objects.create(
            project=project, task=task, minutes=minutes_total, created_by=request.user, created_at=date)
    
    context = {
        'project': project,
        'task': task,
        'today': datetime.today()  # facing problem on this
    }
    return render(request, 'project/task_detail.html', context)


def task_edit(request, pk, task_id):
    project = get_object_or_404(Project, pk=pk)
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')

        if title:
            task.name = title
            task.status = status
            task.save()
            return redirect('task_detail', pk=project.id, task_id=task.id)

    context = {
        'project': project,
        'task': task
    }
    return render(request, 'project/task_edit.html', context)


def edit_entry(request, pk, task_id, entry_id):
    project = get_object_or_404(Project, pk=pk)
    task = get_object_or_404(Task, pk=task_id)
    entry = get_object_or_404(Entry, pk=entry_id)
    if request.method == 'POST':
        hours = int(request.POST.get('hours'))
        minutes = int(request.POST.get('minutes'))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())

        entry.created_at = date
        entry.minutes = (hours * 60) + minutes
        entry.save()

        return redirect('task_detail', pk=project.id, task_id=task.id)

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'project': project,
        'task': task,
        'entry': entry,
        'hours': hours,
        'minutes': minutes
    }
    return render(request, 'project/entry_edit.html', context)
