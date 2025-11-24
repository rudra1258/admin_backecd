from django.urls import path
from . import views

app_name = 'kg_app'  # important for namespacing URLs

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.admin_login, name='admin_login'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('complete_task/', views.complete_task, name='complete_task'),
    path('create_task/', views.create_task, name='create_task'),
    path('create_user/', views.create_user, name='create_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groundstaff/', views.groundstaff, name='groundstaff'),
    path('gs_login/', views.gs_login, name='gs_login'),
    path('leave/', views.leave, name='leave'),
    path('pending_task/', views.pending_task, name='pending_task'),
    path('tc_login/', views.tc_login, name='tc_login'),
    path('teamlead/', views.teamlead, name='teamlead'),
    path('telecaller/', views.telecaller, name='telecaller'),
    path('tl_login/', views.tl_login, name='tl_login'),
    
    path('download-sample/', views.download_sample_excel_user_create, name='download_sample_excel'),
    path('import_users_from_excel/', views.import_users_from_excel, name='import_users_from_excel'),
    
    # Task Import URLs
    path('import-tasks/', views.import_tasks_from_excel, name='import_tasks'),
    path('download-task-sample/', views.download_task_sample_excel, name='download_task_sample_excel'),
    path('telecaller/delete/<int:id>/', views.tc_delete, name='tc_delete'),
    path('teamlead/delete/<int:id>/', views.tl_delete, name='tl_delete'),
    path('groundstaff/delete/<int:id>/', views.gs_delete, name='gs_delete'),


]
