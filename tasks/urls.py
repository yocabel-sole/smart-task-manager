from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('api/task/<int:task_id>/toggle/', views.toggle_task_api, name='toggle_task_api'),
    path('register/', views.register, name='register'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]




