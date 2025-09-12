from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Dashboard view
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    # Filtering by status
    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    # Search query
    q = request.GET.get('q')
    if q:
        tasks = tasks.filter(models.Q(title__icontains=q) | models.Q(description__icontains=q))

    # Sorting
    sort = request.GET.get('sort', 'due')
    if sort == 'priority':
        tasks = tasks.order_by('priority', 'due_date')
    elif sort == 'title':
        tasks = tasks.order_by('title')
    elif sort == 'status':
        tasks = tasks.order_by('completed', 'due_date')
    else:
        tasks = tasks.order_by('due_date')

    return render(request, 'tasks/dashboard.html', {'tasks': tasks})

# Create a new task
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})

# Edit an existing task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task})

# Toggle task completion status
@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'ok': True,
            'taskId': task.id,
            'completed': task.completed,
        })
    messages.success(
        request,
        f'Task "{task.title}" marked as {"complete" if task.completed else "incomplete"}!'
    )
    return redirect('dashboard')


@login_required
@require_POST
def toggle_task_api(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'ok': True, 'taskId': task.id, 'completed': task.completed})


# Delete a task with confirmation
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted successfully!')
        return redirect('dashboard')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# User registration view (simple)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'tasks/register.html')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'tasks/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'tasks/register.html')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')

        messages.error(request, 'There was a problem logging you in. Please log in manually.')
        return redirect('login')

    return render(request, 'tasks/register.html')




    





