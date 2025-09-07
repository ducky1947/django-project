from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Todo

def todo_list(request):
    """Display all todos with search and filter functionality"""
    search_query = request.GET.get('search', '')
    filter_status = request.GET.get('filter', 'all')
    
    todos = Todo.objects.all()
    
    # Search functionality
    if search_query:
        todos = todos.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter functionality
    if filter_status == 'completed':
        todos = todos.filter(completed=True)
    elif filter_status == 'pending':
        todos = todos.filter(completed=False)
    
    context = {
        'todos': todos,
        'search_query': search_query,
        'filter_status': filter_status,
    }
    return render(request, 'todo/todo_list.html', context)

def todo_create(request):
    """Create a new todo"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        
        if title:
            todo = Todo.objects.create(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date if due_date else None
            )
            messages.success(request, f'Todo "{todo.title}" created successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Title is required!')
    
    return render(request, 'todo/todo_form.html', {'action': 'Create'})

def todo_update(request, pk):
    """Update an existing todo"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        todo.due_date = due_date if due_date else None
        
        if todo.title:
            todo.save()
            messages.success(request, f'Todo "{todo.title}" updated successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Title is required!')
    
    return render(request, 'todo/todo_form.html', {'todo': todo, 'action': 'Update'})

def todo_delete(request, pk):
    """Delete a todo"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        title = todo.title
        todo.delete()
        messages.success(request, f'Todo "{title}" deleted successfully!')
        return redirect('todo_list')
    
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

def todo_toggle(request, pk):
    """Toggle todo completion status"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    
    status = "completed" if todo.completed else "marked as pending"
    messages.success(request, f'Todo "{todo.title}" {status}!')
    return redirect('todo_list')
