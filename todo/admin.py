from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'completed', 'created_at', 'due_date')
    list_filter = ('priority', 'completed', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('completed',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
