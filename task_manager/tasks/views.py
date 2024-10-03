from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import Q

def task_list(request):
    sort_by = request.GET.get('sort', 'due_date')  # Default sort by due date
    search_query = request.GET.get('search', '')  # Get search query


    tasks = Task.objects.filter(
        Q(title__icontains=search_query) |  # Search in title
        Q(category__icontains=search_query)  # Search in category
    ).order_by(sort_by)  # Sort tasks based on user selection

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'sort_by': sort_by, 'search_query': search_query})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect
from .models import Task

def mark_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True  # Mark the task as completed
    task.save()
    return redirect('task_list')  # Redirect back to the task list

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})
