from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm
from .models import Task

def register(request):
    if request.user.is_authenticated:
        return redirect('list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-created')
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'tasks/detail.html', {'task': task})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add.html', {'form': form})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit.html', {'form': form, 'task': task})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('list')
    return render(request, 'tasks/delete.html', {'task': task})