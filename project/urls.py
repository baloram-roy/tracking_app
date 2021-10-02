from django.urls import path

from .views import (home, edit_entry, project_list_create, project_detail,
                    ProjectUpdateView, delete_project, task_detail, task_edit)

urlpatterns = [

    # path for home view
    path('', home, name='home'),

    # path for project related view
    path('project/', project_list_create, name='project_list'),
    path('project/<int:pk>/', project_detail, name='project_detail'),
    path('project/<int:pk>/edit/',
         ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/',
         delete_project, name='project_delete'),



    # path  for task realted view:

    path('project/<int:pk>/<int:task_id>/', task_detail, name='task_detail'),
    path('project/<int:pk>/<int:task_id>/edit/', task_edit, name='task_edit'),


    # path for entry related view:
    path('project/<int:pk>/<int:task_id>/<int:entry_id>/edit/',
         edit_entry, name='edit-entry'),

]
