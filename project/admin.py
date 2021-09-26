from django.contrib import admin

from .models import Project, Task

# Register your models here.

# admin.site.register(Project)


@admin.register(Project)
class ProjecrtAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name',
                    'deadline', 'created_at', 'created_by']


@admin.register(Task)
class ProjecrtAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'created_at', 'created_by', 'status']
