from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo

# Basic CRUD views - September 10 development

def todo_list(request):
    """Display all todos"""
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_create(request):
    """Create a new todo"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        
        if title:
            Todo.objects.create(
                title=title, 
                description=description,
                priority=priority
            )
            return redirect('todo_list')
    
    return render(request, 'todo/todo_form.html', {'action': 'Create'})

def todo_update(request, pk):
    """Update an existing todo"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.priority = request.POST.get('priority', 'medium')
        
        if todo.title:
            todo.save()
            return redirect('todo_list')
    
    return render(request, 'todo/todo_form.html', {'todo': todo, 'action': 'Update'})

def todo_delete(request, pk):
    """Delete a todo"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

def todo_toggle(request, pk):
    """Toggle todo completion status"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
