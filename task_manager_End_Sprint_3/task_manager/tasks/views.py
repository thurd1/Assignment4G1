from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, CreateUserForm
from django.db.models import Q 
from datetime import datetime

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')
            return redirect('login')
    context = {'form': form}
    return render(request, 'tasks/register.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'tasks/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(category__icontains=search_query))

    sort_by = request.GET.get('sort_by', '')
    if sort_by in ['category', '-category', 'due_date', '-due_date']:
        tasks = tasks.order_by(sort_by)

    uncomplete_tasks = tasks.filter(completed=False)

    # Greeting based on the current hour
    current_hour = datetime.now().hour
    greeting = "Good Morning" if current_hour < 12 else "Good Afternoon" if current_hour < 18 else "Good Evening"

    context = {
        'uncomplete_tasks': uncomplete_tasks,
        'search_query': search_query,
        'greeting': f"{greeting}, {request.user.username}!",
        'task_count': tasks.count(),  # Total tasks for display
    }
    
    return render(request, 'tasks/task_list.html', context)

@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.user != request.user:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.user != request.user:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/confirm_delete.html', {'task': task})

@login_required(login_url='login')
def completed_tasks(request):
    completed_tasks = Task.objects.filter(user=request.user, completed=True)
    return render(request, 'tasks/completed_tasks.html', {'completed_tasks': completed_tasks})

@login_required(login_url='login')
def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.user != request.user:
        messages.error(request, 'You do not have permission to uncomplete this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        task.completed = False
        task.save()
        messages.success(request, 'Task marked as incomplete!')
        return redirect('completed_tasks')

@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.user != request.user:
        messages.error(request, 'You do not have permission to complete this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        task.completed = True
        task.save()
        messages.success(request, 'Task marked as complete!')
    return redirect('task_list')
