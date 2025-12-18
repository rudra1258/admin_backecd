from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'kg_app'  # important for namespacing URLs


router = routers.DefaultRouter()
router.register(r'createUserList', views.CreateUserViewSet)
router.register(r'createTaskList', views.Create_task_Viewset)

urlpatterns = [
    
    # admin urls 
    
    
    # path('', views.index, name='index'),
    path('', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('update_task/', views.update_task, name='update_task'),
    # path('view_history/', views.view_history, name='view_history'),
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
    path('feddback_history/', views.feddback_history, name='feddback_history'),
    
    path('download-sample/', views.download_sample_excel_user_create, name='download_sample_excel'),
    path('import_users_from_excel/', views.import_users_from_excel, name='import_users_from_excel'),
    
    # Task Import URLs
    path('import-tasks/', views.import_tasks_from_excel, name='import_tasks'),
    path('download-task-sample/', views.download_task_sample_excel, name='download_task_sample_excel'),
    path('telecaller/delete/<int:id>/', views.tc_delete, name='tc_delete'),
    path('teamlead/delete/<int:id>/', views.tl_delete, name='tl_delete'),
    path('groundstaff/delete/<int:id>/', views.gs_delete, name='gs_delete'),

    # telecaller urls 
    
    path('tc_dashboard/', views.tc_dashboard, name='tc_dashboard'),
    path('tc_teamlead/', views.tc_teamlead, name='tc_teamlead'),
    path('tc_groundstaff/', views.tc_groundstaff, name='tc_groundstaff'),
    path('tc_tl_login/', views.tc_tl_login, name='tc_tl_login'),
    path('tc_gs_login/', views.tc_gs_login, name='tc_gs_login'),
    path('tc_assign_task/', views.tc_assign_task, name='tc_assign_task'),
    path('tc_update_task/', views.tc_update_task, name='tc_update_task'),
    path('tc_pending_task/', views.tc_pending_task, name='tc_pending_task'),
    path('tc_complete_task/', views.tc_complete_task, name='tc_complete_task'),
    path('tc_leave/', views.tc_leave, name='tc_leave'),
    path('tc_feddback_history/', views.tc_feddback_history, name='tc_feddback_history'),
    
    
    # api urls
    path('', include(router.urls)),
    path('user/login/', views.user_login, name='user-login'),
    path('update-image-status-drf/', views.update_api_image_status_drf, name='update_image_status_drf'),
    path('gs-login/create/', views.create_gs_login, name='create_gs_login'),


]
