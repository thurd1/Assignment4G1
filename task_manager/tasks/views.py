# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task  # Make sure you have a Task model defined
from .forms import TaskForm  # Make sure you have a TaskForm defined

def task_list(request):
    tasks = Task.objects.all()  # Get all tasks
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to task list after adding
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

def edit_task(request, pk):
    task = Task.objects.get(pk=pk)  # Get the task by primary key
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Update the existing task
            return redirect('task_list')  # Redirect to the task list
    else:
        form = TaskForm(instance=task)  # Pre-fill the form with the task's current data

    return render(request, 'tasks/edit_task.html', {'form': form})

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')  # Redirect to task list after deleting
    return render(request, 'tasks/delete_task.html', {'task': task})
