from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='list'),
    path('add/', views.add_task, name='add'),
    path('task/<int:pk>/', views.task_detail, name='detail'),
    path('edit/<int:pk>/', views.edit_task, name='edit'),
    path('delete/<int:pk>/', views.delete_task, name='delete'),
]