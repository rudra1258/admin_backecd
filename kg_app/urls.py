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
    path('gs-login/create/', views.create_gs_login, name='create_gs_login'),#http://127.0.0.1:8000/api/v1/gs-login/create/
    
    # task GET endpoints
    path('tasks/get/', views.get_tasks, name='get_tasks'),#http://127.0.0.1:8000/api/v1/tasks/get/
    path('tasks/get/<int:task_id>/', views.get_task_by_id, name='get_task_by_id'), #http://127.0.0.1:8000/api/v1/tasks/get/?admin_id=1
    
    
    # task UPDATE endpoint
    path('tasks/update/<int:task_id>/', views.update_api_task, name='update_task'),#http://127.0.0.1:8000/api/v1/tasks/update/5/
    
    
    # GET endpoints for task updates
    path('task-updates/get/', views.get_task_updates, name='get_task_updates'),
    path('task-updates/get/<int:task_update_id>/', views.get_task_update_by_id, name='get_task_update_by_id'),
    
    # POST endpoint for creating task update
    path('task-updates/create/', views.create_task_update, name='create_task_update'),
    
    #TODO: api testing
    # Example Usage: above 3 urls
    """
    1. Get all task updates:
    GET /api/task-updates/get/

    2. Get task updates filtered by admin_id:
    GET /api/task-updates/get/?admin_id=1

    3. Get task updates filtered by task_id:
    GET /api/task-updates/get/?task_id=5

    4. Get task updates filtered by agreement_id:
    GET /api/task-updates/get/?agreement_id=AGR12345

    5. Get task updates with multiple filters:
    GET /api/task-updates/get/?admin_id=1&task_id=5

    6. Get single task update by ID:
    GET /api/task-updates/get/10/

    7. Create task update (JSON - without files):
    POST /api/task-updates/create/
    Content-Type: application/json
    
    Body:
    {
        "updated_by": "John Doe",
        "admin_id": 1,
        "task_id": 5,
        "agreement_id": "AGR12345",
        "code": "CODE001",
        "new_mobile_number": "9876543210",
        "projection": "Payment Expected",
        "promise_date": "2024-12-30T10:00:00",
        "promise_amount": "25000",
        "customer_remark": "Customer agreed to pay",
        "reference_remark": "Reference confirmed",
        "need_group_visit": "Yes",
        "visit_projection": "Visit scheduled",
        "visit_status": "Pending",
        "customer_available": "Yes",
        "vehicle_available": "Yes",
        "third_party_status": "No",
        "third_party_details": "",
        "new_update_address": "123 New Street, Mumbai",
        "location_status": "Verified",
        "recipt_no": "RCPT123",
        "payment_mode": "UPI",
        "payment_amount": "15000",
        "payment_date": "2024-12-23T14:30:00"
    }

    8. Create task update (Form Data - with files):
    POST /api/task-updates/create/
    Content-Type: multipart/form-data
    
    Form Data:
    - updated_by: "John Doe"
    - admin_id: 1
    - task_id: 5
    - agreement_id: "AGR12345"
    - location_image: [file upload]
    - document_image: [file upload]
    - customer_remark: "Customer agreed to pay"
    - ... (other fields)
    """
]
