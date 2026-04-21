from django.urls import path, include
from . import views
from rest_framework import routers
from .views import *

app_name = 'kg_app'  # important for namespacing URLs


router = routers.DefaultRouter()
router.register(r'createUserList', views.CreateUserViewSet)
router.register(r'createTaskList', views.Create_task_Viewset)

urlpatterns = [
    
    # admin urls 
    
    
    path('login/', views.admin_login, name='index'),
    path('', views.landing_page, name='landing_page'),
    path('testing/dev/home-page', views.landing_page, name='landing_page'),
    path('test_screen/', views.test_page, name='test_screen'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    
    path('assign_task/api/', views.assign_task_api, name='assign_task_api'),
    path('assign_task/filter-values/', views.assign_task_filter_values, name='assign_task_filter_values'),
    path('assign_task/category-counts/', views.assign_task_category_counts, name='assign_task_category_counts'),
    path('assign_task/', views.assign_task, name='assign_task'),
    
    path('update_task/', views.update_task, name='update_task'),
    # path('view_history/', views.view_history, name='view_history'),
    path('complete_task/', views.complete_task, name='complete_task'),
    path('create_task/', views.create_task, name='create_task'),
    path('create_user/', views.create_user, name='create_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groundstaff/', views.groundstaff, name='groundstaff'),
    path('repo_boy/', views.repo_boy, name='repo_boy'),
    path('gs_login/', views.gs_login, name='gs_login'),
    path('repo_login/', views.repo_login, name='repo_login'),
    path('leave/', views.leave, name='leave'),
    path('get-leave-details/', views.get_leave_details, name='get_leave_details'),
    path('approve_leave/', views.approve_leave, name='approve_leave'),
    path('reject_leave/', views.reject_leave, name='reject_leave'),
    path('pending_task/', views.pending_task, name='pending_task'),
    path('tc_login/', views.tc_login, name='tc_login'),
    path('teamlead/', views.teamlead, name='teamlead'),
    path('telecaller/', views.telecaller, name='telecaller'),
    path('tl_login/', views.tl_login, name='tl_login'),
    path('feddback_history/', views.feddback_history, name='feddback_history'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('team_management/', views.team_management, name='team_management'),
    path('telecaller/<int:telecaller_id>/team/', views.telecaller_team_detail, name='telecaller_team_detail'),
    path('tlAssignToTc/', views.tlAssignToTc, name='tlAssignToTc'),
    path("change-staff-password/", views.change_staff_password, name="change_staff_password"),
    path("change_tc_password/", views.change_tc_password, name="change_tc_password"),
    path("change_tl_password/", views.change_tl_password, name="change_tl_password"),
    path("change_repoboy_password/", views.change_repo_password, name="change_repoboy_password"),
    path('bulk-delete-tasks/', views.bulk_delete_tasks, name='bulk_delete_tasks'),
    path('pending-bulk-delete-tasks/', views.pending_bulk_delete_tasks, name='pending_bulk_delete_tasks'),
    path('attendance/', views.attendance, name='attendance'),
    path('support/', views.support, name='support'),
    path('feedback/', views.feedback, name='feedback'),
    path("send-support-email/", views.send_support_email, name="send_support_email"),
    path('submit/', views.submit_feedback, name='submit'),
    path('list/', views.feedback_list, name='list'),
    path('contact_message_submit/', views.contact_message_submit, name='contact_message_submit'),
    path('email_list_submit/', views.email_list_submit, name='email_list_submit'),

    path('download-sample/', views.download_sample_excel_user_create, name='download_sample_excel'),
    path('import_users_from_excel/', views.import_users_from_excel, name='import_users_from_excel'),
    path('download-failed-rows/', views.download_failed_import_rows, name='download_failed_rows'),
    
    
    path('repo-search-history/', views.repo_search_history, name='repo_search_history'),

    path(
        "admin/marquee_app/marqueemessage/<int:pk>/toggle/",
        views.toggle_marquee,
        name="toggle_marquee",
    ),
    
    path("marquee/", views.marquee_demo, name="marquee_demo"),
 
    # AJAX / API endpoints
    path("api/marquee/active/", views.get_active_marquee_api, name="active_marquee_api"),
    path("api/marquee/<int:pk>/toggle/", views.toggle_marquee_api, name="toggle_marquee_api"),


    
    # Task Import URLs
    path('import-tasks/', views.import_tasks_from_excel, name='import_tasks'),
    path('download-task-sample/', views.download_task_sample_excel, name='download_task_sample_excel'),
    path('telecaller/delete/<int:id>/', views.tc_delete, name='tc_delete'),
    path('teamlead/delete/<int:id>/', views.tl_delete, name='tl_delete'),
    path('groundstaff/delete/<int:id>/', views.gs_delete, name='gs_delete'),
    path('repo_boy/delete/<int:id>/', views.repo_delete, name='repo_delete'),
    path('task/delete/<int:id>/', views.task_delete, name='task_delete'),
    path('complete_task/delete/<int:id>/', views.task_delete_complete, name='task_delete_complete'),
    path('pending_task/delete/<int:id>/', views.pending_task_delete_complete, name='pending_task_delete'),

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
    path('tc_leave_apply/', views.tc_leave_apply, name='tc_leave_apply'),
    path('tc_leave_list/', views.tc_leave_list, name='tc_leave_list'),
    path('tc_profile/', views.tc_profile, name='tc_profile'),
    path('tc_leave_requests/', views.tc_leave_requests, name='tc_leave_requests'),
    path('tc_approve_leave/', views.tc_approve_leave, name='tc_approve_leave'),
    path('tc_reject_leave/', views.tc_reject_leave, name='tc_reject_leave'),
    
    
    # api urls
    path('', include(router.urls)),
    path('user/login/', views.user_login, name='user-login'),
    path('update-image-status-drf/', views.update_api_image_status_drf, name='update_image_status_drf'),
    path('gs-login/create/', views.create_gs_login, name='create_gs_login'),#http://127.0.0.1:8000/api/v1/gs-login/create/
    path('tl-login/create/', views.create_tl_login, name='create_tl_login'),#http://127.0.0.1:8000/api/v1/tl-login/create/
    path('repo-login/create/', views.create_repo_login, name='create_repo_login'),#http://127.0.0.1:8000/api/v1/repo-login/create/
    
    # task GET endpoints
    path('tasks/get/', views.get_tasks, name='get_tasks'),#http://127.0.0.1:8000/api/v1/tasks/get/
    path('tasks/get/<int:task_id>/', views.get_task_by_id, name='get_task_by_id'), #http://127.0.0.1:8000/api/v1/tasks/get/?admin_id=1
    
    
    # task UPDATE endpoint
    path('tasks/update/<int:task_id>/', views.update_api_task, name='update_task'),#http://127.0.0.1:8000/api/v1/tasks/update/5/
    
    
    # GET endpoints for task updates
    path('task-updates/get/', views.get_task_updates, name='get_task_updates'),
    path('task-updates/get/<int:task_update_id>/', views.get_task_update_by_id, name='get_task_update_by_id'),
    
    # filter by task id 
    # https://admin-backecd-2.onrender.com/api/v1/task-updates/get/?task_id=4
    # filter by admin id 
    # https://admin-backecd-2.onrender.com/api/v1/task-updates/get/?admin_id=1
    
    
    # POST endpoint for creating task update
    # NOT WORKING DON'T USE THIS url
    # this url is not using in api testing also because of some issue in serializer validation for task_id and admin_id
    path('task-updates/create/', views.create_task_update, name='create_task_update'),#https://admin-backecd-2.onrender.com/api/v1/task-updates/create/

    # this url is working fine and using in api testing for creating task update
    path('task-update/create/', TaskUpdateCreateAPI.as_view(), name='task-update-create'),
    
    #TODO: api testing -> done
    # Example Usage: above 3 urls
    
    # 1. Get all task updates:
    # GET /api/task-updates/get/

    # 2. Get task updates filtered by admin_id:
    # GET /api/task-updates/get/?admin_id=1

    # 3. Get task updates filtered by task_id:
    # GET /api/task-updates/get/?task_id=5

    # 4. Get task updates filtered by agreement_id:
    # GET /api/task-updates/get/?agreement_id=AGR12345

    # 5. Get task updates with multiple filters:
    # GET /api/task-updates/get/?admin_id=1&task_id=5

    # 6. Get single task update by ID:
    # GET /api/task-updates/get/10/

    # 7. Create task update (JSON - without files):
    # POST /api/task-updates/create/
    # Content-Type: application/json
    
    # Body:
    # {
    #     "updated_by": "John Doe",
    #     "admin_id": 1,
    #     "task_id": 5,
    #     "agreement_id": "AGR12345",
    #     "code": "CODE001",
    #     "new_mobile_number": "9876543210",
    #     "projection": "Payment Expected",
    #     "promise_date": "2024-12-30T10:00:00",
    #     "promise_amount": "25000",
    #     "customer_remark": "Customer agreed to pay",
    #     "reference_remark": "Reference confirmed",
    #     "need_group_visit": "Yes",
    #     "visit_projection": "Visit scheduled",
    #     "visit_status": "Pending",
    #     "customer_available": "Yes",
    #     "vehicle_available": "Yes",
    #     "third_party_status": "No",
    #     "third_party_details": "",
    #     "new_update_address": "123 New Street, Mumbai",
    #     "location_status": "Verified",
    #     "recipt_no": "RCPT123",
    #     "payment_mode": "UPI",
    #     "payment_amount": "15000",
    #     "payment_date": "2024-12-23T14:30:00"
    # }

    # 8. Create task update (Form Data - with files):
    # POST /api/task-updates/create/
    # Content-Type: multipart/form-data
    
    # Form Data:
    # - updated_by: "John Doe"
    # - admin_id: 1
    # - task_id: 5
    # - agreement_id: "AGR12345"
    # - location_image: [file upload]
    # - document_image: [file upload]
    # - customer_remark: "Customer agreed to pay"
    # - ... (other fields)
    
    
    
    # to update mobile login status to prevent multiple login
    path( 'update-mobile-login/<int:user_id>/', UpdateMobileLoginAPI.as_view(), name='update-mobile-login' ),
    # demo link : http://127.0.0.1:8000/api/v1/update-mobile-login/17/
    # api body : 
    # {
    #     "isMobile_login": "Yes"
    # }
    
    # api response 
    # {
    #     "status": true,
    #     "message": "Mobile login status updated successfully",
    #     "data": {
    #         "isMobile_login": "Yes"
    #     }
    # }
    
    # to get gs punch in details by gs User Id user id
    # method get - -
    path( 'gs-login/<int:user_id>/', get_gs_login_by_user_id, name='get_gs_login_by_user_id' ),
    path( 'tl-login/<int:user_id>/', get_tl_login_by_user_id, name='get_tl_login_by_user_id' ),
    path( 'repo-login/<int:user_id>/', get_repo_login_by_user_id, name='get_repo_login_by_user_id' ),
    # http://127.0.0.1:8000/api/v1/gs-login/23/
    
    # to update gs login details by gs_login_id
    # path('gs-punch-in/update/<int:gs_login_id>/', update_gs_login, name='update_gs_login' ),
    # http://127.0.0.1:8000/api/v1/gs-punch-in/update/4/
    
    path('update-gs-login/<int:gs_login_id>/', views.update_gs_login, name='update_gs_login'),
    path('update-tl-login/<int:tl_login_id>/', views.update_tl_login, name='update_tl_login'),
    path('update-repo-login/<int:repo_login_id>/', views.update_repo_login, name='update_repo_login'),


    path('leave-request/create/', LeaveRequestCreateAPIView.as_view(), name='leave-request-create'),
    # http://127.0.0.1:8000/api/v1/leave-request/create/
    
    
    path('leave-request/user/<int:user_id>/', LeaveRequestByUserAPIView.as_view(), name='leave-request-by-user'),
    # http://127.0.0.1:8000/api/v1/leave-request/user/10/


    path('attendance/user/<int:user_id>/', get_user_attendance),
    path('attendance/all/', get_all_attendance),
    
    path('tasks/with-registration/', TasksWithRegistrationNumberView.as_view(), name='tasks-with-registration'),
    
    path('search-history/', SearchHistoryListCreateAPI.as_view(), name='search_history_api'),
    # POST /api/v1/search-history/
    # request body:
    # {
    #     "admin_id": 1,
    #     "user_id": 5,
    #     "search_query": "Honda City",
    #     "vehicle_registration_number": "OD02AB1234",
    #     "customer_name": "Rudra",
    #     "customer_mobile_number": "9876543210"
    # }
    # GET /api/v1/search-history/
    # GET /api/v1/search-history/?admin_id=1
    
    
    # notifications/ - for FCM token management
    path('fcm/upsert/', FCMTokenUpsertView.as_view(), name='fcm-upsert'),
    # { "user_id": 1, "fcm_token": "abc123" } body/parameter
    path('fcm/fetch/', FCMTokenFetchView.as_view(), name='fcm-fetch'), # get /api/v1/fcm/fetch/?user_id=1
    

]
