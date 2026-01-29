from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from . models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import pandas as pd
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json
import io
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from rest_framework.views import APIView
from django.db.models import Q


# Create your views here.


# def index(request):
#     return render(request, "index.html")

# def admin_login(request):
#     print("Admin login view called")
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         remember_me = request.POST.get('remember_me')
#         print("Login attempt with email:", email)
#         print("Password entered:", password)
        
#         try:
#             # Check if user exists
#             admin_user = admin_user_model.objects.get(email=email)
            
#             print("Retrieved user:", admin_user)
#             print("Provided password:", password)
#             print("Stored hashed password:", admin_user.password)
            
#             # Verify password
#             if (password == admin_user.password):
#             # if (True):
#                 # Set session
#                 request.session['admin_id'] = admin_user.admin_id
#                 request.session['admin_username'] = admin_user.username
#                 request.session['admin_email'] = admin_user.email
                
#                 # Set session expiry
#                 # request.session.set_expiry(60 * 1) # 1 minute for testing
                
#                 messages.success(request, 'Login successful!')
#                 return render(request, 'dashboard.html', {'email': email})  # Change to your dashboard URL name
#             else:
#                 messages.error(request, 'Invalid email or password!')
#                 # return render(request, 'index.html', {'email': email})
#                 return JsonResponse({"status": "error", "message": "Invalid email or password!"})
                
#         except admin_user_model.DoesNotExist:
#             messages.error(request, 'Invalid email or password!')
#             # return render(request, 'index.html', {'email': email})
#             return JsonResponse({"status": "error", "message": "Invalid email or password!"})
    
#     return render(request, 'index.html')

# def admin_login(request):
#     print("Admin login view called")
    
#     # If GET request, show the login page
#     if request.method == 'GET':
#         return render(request, 'index.html')
    
#     # If POST request, handle login
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         remember_me = request.POST.get('remember_me')
        
#         print("Login attempt with email:", email)
        
#         # Try admin login first
#         try:
#             admin_user = admin_user_model.objects.get(email=email)
            
#             print("Admin user found:", admin_user.username)
#             print("Provided password:", password)
            
#             # Verify password
#             if password == admin_user.password:
#                 # Set session
#                 request.session['admin_id'] = admin_user.admin_id
#                 request.session['admin_username'] = admin_user.username
#                 request.session['admin_email'] = admin_user.email
                
#                 # Set session expiry based on remember_me
#                 if not remember_me:
#                     request.session.set_expiry(0)
                
#                 # Return JSON response for success
#                 return JsonResponse({
#                     'success': True,
#                     'message': 'Login successful!',
#                     'redirect_url': '/dashboard/' 
#                 })
#             else:
#                 # Return JSON response for invalid password
#                 return JsonResponse({
#                     'success': False,
#                     'message': 'Invalid email or password!'
#                 })  
                
#         except admin_user_model.DoesNotExist:
#             pass
#         # Try telecaller login if admin login didn't succeed
#         try:
#             user = CreateUser.objects.get(email=email)
            
#             # Check if user role is allowed to login
#             allowed_roles = ['telecaller']
            
#             if user.role not in allowed_roles:
#                 return JsonResponse({
#                     'success': False,
#                     'message': 'Access denied. Only telecallers can login through this portal.'
#                 })
            
#             # Verify user password
#             if password == user.password:  # Use check_password() if hashed
#                 # Set user session
#                 request.session['tc_admin_id'] = user.admin_id.admin_id
#                 request.session['user_type'] = user.role
#                 request.session['user_id'] = user.id
#                 request.session['username'] = user.username
#                 request.session['tc_first_name'] = user.first_name
#                 request.session['email'] = user.email
#                 request.session['role'] = user.role
                
#                 # Set session expiry based on remember_me
#                 if not remember_me:
#                     request.session.set_expiry(0)
                
#                 return JsonResponse({
#                     'success': True,
#                     'message': 'Telecaller login successful!',
#                     'redirect_url': '/tc_dashboard/'
#                 })
#         except CreateUser.DoesNotExist:
#             pass
    
#     return render(request, 'index.html')


def admin_login(request):
    print("Admin login view called")
    
    # If GET request, show the login page
    if request.method == 'GET':
        return render(request, 'index.html')
    
    # If POST request, handle login
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print("Login attempt with email:", email)
        
        # Get current session key (if exists)
        current_session_key = request.session.session_key
        
        # Try admin login first
        try:
            admin_user = admin_user_model.objects.get(email=email)
            
            print("Admin user found:", admin_user.username)
            print("Provided password:", password)
            
            # Verify password
            if password == admin_user.password:
                # Check if user is already logged in on another device
                if admin_user.active_session_key:
                    # If it's the same session, allow login (browser was closed without logout)
                    if admin_user.active_session_key == current_session_key:
                        # Same device, just update session
                        request.session['admin_id'] = admin_user.admin_id
                        request.session['admin_username'] = admin_user.username
                        request.session['admin_email'] = admin_user.email
                        
                        return JsonResponse({
                            'success': True,
                            'message': 'Login successful!',
                            'redirect_url': '/dashboard/' 
                        })
                    
                    # Different session - check if it's still valid
                    from django.contrib.sessions.models import Session
                    try:
                        existing_session = Session.objects.get(session_key=admin_user.active_session_key)
                        # Session exists and is valid - deny new login
                        return JsonResponse({
                            'success': False,
                            'message': 'You are already logged in on another device. Please logout from that device first.'
                        })
                    except Session.DoesNotExist:
                        # Old session expired, allow new login
                        pass
                
                # Clear any old session data
                if admin_user.active_session_key and admin_user.active_session_key != current_session_key:
                    try:
                        from django.contrib.sessions.models import Session
                        Session.objects.filter(session_key=admin_user.active_session_key).delete()
                    except:
                        pass
                
                # Set session
                request.session['admin_id'] = admin_user.admin_id
                request.session['admin_username'] = admin_user.username
                request.session['admin_email'] = admin_user.email
                
                # Save session first to generate session key
                request.session.save()
                
                # Update user with new session key
                admin_user.active_session_key = request.session.session_key
                admin_user.save()
                
                # Return JSON response for success
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect_url': '/dashboard/' 
                })
            else:
                # Return JSON response for invalid password
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid email or password!'
                })  
                
        except admin_user_model.DoesNotExist:
            pass
            
        # Try telecaller login if admin login didn't succeed
        try:
            user = CreateUser.objects.get(email=email)
            
            # Check if user role is allowed to login
            allowed_roles = ['telecaller']
            
            if user.role not in allowed_roles:
                return JsonResponse({
                    'success': False,
                    'message': 'Access denied. Only telecallers can login through this portal.'
                })
            
            # Verify user password
            if password == user.password:
                # Get current session key
                current_session_key = request.session.session_key
                
                # Check if user is already logged in on another device
                if user.active_session_key:
                    # If it's the same session, allow login
                    if user.active_session_key == current_session_key:
                        request.session['tc_admin_id'] = user.admin_id.admin_id
                        request.session['user_type'] = user.role
                        request.session['user_id'] = user.id
                        request.session['username'] = user.username
                        request.session['tc_first_name'] = user.first_name
                        request.session['email'] = user.email
                        request.session['role'] = user.role
                        
                        return JsonResponse({
                            'success': True,
                            'message': 'Telecaller login successful!',
                            'redirect_url': '/tc_dashboard/'
                        })
                    
                    # Different session - check if it's still valid
                    from django.contrib.sessions.models import Session
                    try:
                        existing_session = Session.objects.get(session_key=user.active_session_key)
                        # Session exists and is valid - deny new login
                        return JsonResponse({
                            'success': False,
                            'message': 'You are already logged in on another device. Please logout from that device first.'
                        })
                    except Session.DoesNotExist:
                        # Old session expired, allow new login
                        pass
                
                # Clear any old session data
                if user.active_session_key and user.active_session_key != current_session_key:
                    try:
                        from django.contrib.sessions.models import Session
                        Session.objects.filter(session_key=user.active_session_key).delete()
                    except:
                        pass
                
                # Set user session
                request.session['tc_admin_id'] = user.admin_id.admin_id
                request.session['user_type'] = user.role
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['tc_first_name'] = user.first_name
                request.session['email'] = user.email
                request.session['role'] = user.role
                
                # Save session first to generate session key
                request.session.save()
                
                # Update user with new session key
                user.active_session_key = request.session.session_key
                user.save()
                
                # Create or update TcLogin record
                TcLogin.objects.update_or_create(
                    user_id=user,
                    defaults={
                        'admin_id': user.admin_id.admin_id,
                        'name': user.first_name,
                        'email': user.email,
                        'mobile_no': user.phone_number,
                        'status': 'Active',
                        'login_time': timezone.now(),
                    }
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Telecaller login successful!',
                    'redirect_url': '/tc_dashboard/'
                })
        except CreateUser.DoesNotExist:
            pass
        
        # If we reach here, login failed
        return JsonResponse({
            'success': False,
            'message': 'Invalid email or password!'
        })
    
    return render(request, 'index.html')

def admin_logout(request):
    # Get user info before clearing session
    admin_id = request.session.get('admin_id')
    user_id = request.session.get('user_id')
    
    # Clear session key from database
    if admin_id:
        try:
            admin_user = admin_user_model.objects.get(admin_id=admin_id)
            admin_user.active_session_key = None
            admin_user.save()
        except admin_user_model.DoesNotExist:
            pass
    
    if user_id:
        try:
            user = CreateUser.objects.get(id=user_id)
            user.active_session_key = None
            user.save()
        except CreateUser.DoesNotExist:
            pass
        
    if user_id:
        tc_id_pk = CreateUser.objects.get(pk=user_id)
        try:
            tc_login = TcLogin.objects.get(user_id_id=tc_id_pk)
            tc_login.status = 'Inactive'
            tc_login.logout_time = timezone.now()
            tc_login.save()
        except TcLogin.DoesNotExist:
            pass
    
    # Clear session
    request.session.flush()
    
    return redirect('/')

def create_user(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk=session_admin_id)
    
    print(f"session admin id by admin_user_model primary key- {admin_id_pk}")
    
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("eemail")
        phone_number = request.POST.get("pnumber")
        role = request.POST.get("rrole")
        username = request.POST.get("user_name")
        address = request.POST.get("address")
        password = request.POST.get("pass_word")

        try:
            # Check if username already exists
            if CreateUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                admins = admin_user_model.objects.all()
                return render(request, "create_user.html", {
                    "admins": admins,
                    "form_data": request.POST  # Pass form data back to preserve user input
                })
            
            # Check if email already exists
            if CreateUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email.')
                admins = admin_user_model.objects.all()
                return render(request, "create_user.html", {
                    "admins": admins,
                    "form_data": request.POST
                })

            CreateUser.objects.create(
                admin_id=admin_id_pk,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                role=role,
                username=username,
                address=address,
                password=password
            )
            # Add success message
            messages.success(request, 'User created successfully!')
            return redirect("kg_app:create_user")
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            admins = admin_user_model.objects.all()
            return render(request, "create_user.html", {
                "admins": admins,
                "form_data": request.POST
            })

    admins = admin_user_model.objects.all()
    return render(request, "create_user.html", {"admins": admins})

# api like view for CreateUser model
class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = CreateUser.objects.all()
    serializer_class = UserListSerializer

def import_users_from_excel(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk=session_admin_id)
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Validate file extension
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, 'Please upload a valid Excel file (.xlsx or .xls)')
            return redirect('kg_app:import_users_from_excel')
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Strip whitespace from column names
            df.columns = df.columns.str.strip()
            
            # Required columns
            required_columns = ['first_name', 'last_name', 'email', 'phone_number', 
                              'role', 'username', 'password']
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                messages.error(request, f'Missing required columns: {", ".join(missing_columns)}')
                return redirect('kg_app:import_users_from_excel')
            
            success_count = 0
            error_count = 0
            errors = []
            
            # Process each row
            for index, row in df.iterrows():
                try:
                    # Skip empty rows
                    if pd.isna(row['email']) or pd.isna(row['username']):
                        continue
                    
                    # Check if user already exists
                    if CreateUser.objects.filter(email=row['email']).exists():
                        errors.append(f"Row {index + 2}: User with email {row['email']} already exists")
                        error_count += 1
                        continue
                    
                    if CreateUser.objects.filter(username=row['username']).exists():
                        errors.append(f"Row {index + 2}: Username {row['username']} already exists")
                        error_count += 1
                        continue
                    
                    # Validate role
                    valid_roles = ['telecaller', 'teamlead', 'groundstaff']
                    role = str(row['role']).lower().strip()
                    if role not in valid_roles:
                        errors.append(f"Row {index + 2}: Invalid role '{row['role']}'")
                        error_count += 1
                        continue
                    
                    # Create user
                    user = CreateUser(
                        admin_id=admin_id_pk,  # Assuming current user is admin
                        first_name=str(row['first_name']).strip(),
                        last_name=str(row['last_name']).strip(),
                        email=str(row['email']).strip().lower(),
                        phone_number=str(row['phone_number']).strip(),
                        role=role,
                        username=str(row['username']).strip(),
                        address=str(row.get('address', '')).strip() if pd.notna(row.get('address')) else '',
                        password=(row['password']) # Hash the password
                    )
                    user.save()
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                    error_count += 1
            
            # Display results
            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} users!')
            
            if error_count > 0:
                error_message = f'{error_count} errors occurred:<br>'
                error_message += '<br>'.join(errors[:10])  # Show first 10 errors
                if len(errors) > 10:
                    error_message += f'<br>...and {len(errors) - 10} more errors'
                messages.warning(request, error_message)
            
            if success_count == 0 and error_count == 0:
                messages.info(request, 'No data found in the Excel file')
            
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
        
        return redirect('kg_app:import_users_from_excel')
    
    return render(request, 'create_user.html')

def download_sample_excel_user_create(request):
    """Generate and download a sample Excel template"""
   
    
    # Create sample data
    sample_data = {
        'first_name': ['John', 'Jane'],
        'last_name': ['Doe', 'Smith'],
        'email': ['john.doe@example.com', 'jane.smith@example.com'],
        'phone_number': ['1234567890', '0987654321'],
        'role': ['telecaller', 'teamlead'],
        'username': ['johndoe', 'janesmith'],
        'address': ['123 Main St', '456 Oak Ave'],
        'password': ['password123', 'password456']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Users')
    
    output.seek(0)
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=user_import_template.xlsx'
    
    return response

def assign_task(request):
    session_admin_id = request.session.get('admin_id')
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    create_task_list = Create_task.objects.filter(
        admin_id = admin_id_pk
    )
    update_task_list = task_update.objects.all()
    print(f"Task count: {create_task_list.count()}") 

     # Convert queryset to JSON with all fields from your model
    updated_task_list_json = json.dumps(list(update_task_list.values(
        'task_update_id',
        'updated_by',
        'updated_at',
        'agreement_id',
        'code',
        'new_mobile_number',
        'projection',
        'promise_date',
        'promise_amount',
        'customer_remark',
        'reference_remark',
        'need_group_visit',
        'visit_projection',
        'visit_status',
        'customer_available',
        'vehicle_available',
        'third_party_status',
        'third_party_details',
        'new_update_address',
        'location_image',
        'document_image',
        'location_status',
        'recipt_no',
        'payment_mode',
        'payment_amount',
        'payment_date',
        'updated_at',
    )), default=str)
    
    return render(request, "assign_task.html", {
        "task_list":create_task_list, 
        "updated_task_list":update_task_list,
        "updated_task_list_json": updated_task_list_json
        })

def complete_task(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    create_task_list = Create_task.objects.filter(
        admin_id=admin_id_pk
    ).exclude(
        Q(update_location_status="RF") | Q(update_location_status__isnull=True)
    )
    
    return render(request, "complete_task.html", {"task_list": create_task_list})

def task_delete_complete(request, id):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    emp = get_object_or_404(Create_task, task_id=id)
    emp.delete()
    return redirect('kg_app:complete_task')

def create_task(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    
    admin_id_pk = admin_user_model.objects.get(pk=session_admin_id)
    # Filter users by admin_id and role telecaller
    user_list = CreateUser.objects.filter(
        admin_id=admin_id_pk,
        role='telecaller'
    )
    
    gs_user_list = CreateUser.objects.filter(
        admin_id=admin_id_pk,
        role='groundstaff'
    )
    
    tl_user_list = CreateUser.objects.filter(
        admin_id=admin_id_pk,
        role='teamlead'
    )
    
    if request.method == "POST":    
        print("FULL POST:", request.POST)
        
        print("Create Task POST request data: --- -- - ", request.POST.get("prodduct_type"))
           
        # addreement information
        aggrement_id = request.POST.get("agreement_id")
        customer_name = request.POST.get("customer_name")
        product_type = request.POST.get("prodduct_type")
        tc_name = request.POST.get("tc_name")
        tc_userName = request.POST.get("user_name")
        branch = request.POST.get("branch")
        count_of_cases = request.POST.get("count_of_cases")
        old_or_new = request.POST.get("old_or_new")
        bucket = request.POST.get("bucket")
        mode = request.POST.get("mode")
        npa_status = request.POST.get("npa_status")
        
        # financial details
        pos_amount = request.POST.get("pos_amount")
        total_charges = request.POST.get("total_charges")
        bcc_pending = request.POST.get("bcc_pending")
        penal_pending = request.POST.get("penal_pending")
        emi_amount = request.POST.get("emi_amount")
        emi_due_amount = request.POST.get("emi_due_amount")
        recipt_amount = request.POST.get("recipt_amount")
        recipt_date = request.POST.get("recipt_date")
        disbursement_amount = request.POST.get("disbursement_amount")
        loan_amount = request.POST.get("loan_amount")
        disbursement_date = request.POST.get("disbursement_date")
        emi_start_date = request.POST.get("emi_start_date")
        emi_end_date = request.POST.get("emi_end_date")
        emi_cycle_date = request.POST.get("emi_cycle_date")
        
        # vhicle details
        make = request.POST.get("make")
        manufacturer_description = request.POST.get("manufacturer_description")
        registration_number = request.POST.get("registration_number")
        vehicle_age = request.POST.get("vehicle_age")
        
        # customer details
        employer = request.POST.get("employer")
        father_name = request.POST.get("father_name")
        fe_name = request.POST.get("gs_name")
        fe_Mobile = request.POST.get("fe_Mobile")
        fe_userName = request.POST.get("gs_user_name")
        customer_number = request.POST.get("customer_number")
        pin_code = request.POST.get("pin_code")
        customer_address = request.POST.get("customer_address")
        customer_office_address = request.POST.get("customer_office_address")
        reference_details = request.POST.get("reference_details")
        
        # collection details
        collection_manager_name = request.POST.get("collection_manager_name")
        finance_company_name = request.POST.get("financy_company")
        

        Create_task.objects.create(
            # aggrement information 
            admin_id=admin_id_pk,
            aggrement_id=aggrement_id,
            customer_name=customer_name,
            product_type=product_type,
            tc_name=tc_name,
            tc_userName=tc_userName,
            branch=branch,
            count_of_cases=count_of_cases,
            old_or_new=old_or_new,
            bucket=bucket,
            mode=mode,
            npa_status=npa_status,
            
            # financial details 
            pos_amount=pos_amount,
            total_charges=total_charges,
            bcc_pending=bcc_pending,
            penal_pending=penal_pending,
            emi_amount=emi_amount,
            emi_due_amount=emi_due_amount,
            recipt_amount=recipt_amount,
            recipt_date=recipt_date,
            disbursement_amount=disbursement_amount,
            loan_amount=loan_amount,
            disbursement_date=disbursement_date,
            emi_start_date = emi_start_date,
            emi_end_date = emi_end_date,
            emi_cycle_date = emi_cycle_date,
            
            # vehicle details
            make = make,
            manufacturer_description = manufacturer_description,
            registration_number = registration_number,
            vehicle_age = vehicle_age,
            
            # customer details
            employer = employer,
            father_name = father_name,
            fe_name = fe_name,
            fe_userName = fe_userName,
            fe_mobile_number = fe_Mobile,
            customer_mobile_number = customer_number,
            pin_code = pin_code,
            customer_address = customer_address,
            customer_office_address = customer_office_address,
            reference_details = reference_details,
            
            # collection details 
            collection_manager_name = collection_manager_name,
            finance_company_name = finance_company_name                
        )
        messages.success(request, 'Task created successfully!')
        return redirect("kg_app:create_task")
    
    
    return render(request, "create_task.html", {
        "users": user_list, 
        "gs_users": gs_user_list,
        "tc_user_list": tl_user_list,
        })

#create task list api function
class Create_task_Viewset(viewsets.ModelViewSet):
    queryset = Create_task.objects.all()
    serializer_class = CreateTaskSerializer

def import_tasks_from_excel(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk=session_admin_id)
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Validate file extension
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, 'Please upload a valid Excel file (.xlsx or .xls)')
            return redirect('kg_app:import_tasks')
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Strip whitespace from column names
            df.columns = df.columns.str.strip()
            
            # Required columns (only mandatory fields)
            required_columns = [
                'aggrement_id', 'customer_name', 'product_type', 'tc_name', 
                'branch', 'count_of_cases', 'old_or_new', 'bucket', 'mode', 
                'npa_status', 'pos_amount', 'total_charges', 'bcc_pending', 
                'penal_pending', 'emi_amount', 'emi_due_amount', 'recipt_amount', 
                'recipt_date', 'disbursement_amount', 'loan_amount', 'disbursement_date', 
                'emi_start_date', 'emi_end_date', 'emi_cycle_date', 'make', 
                'father_name', 'fe_name', 'fe_mobile_number', 'customer_mobile_number', 
                'pin_code', 'customer_address', 'customer_office_address', 
                'reference_details', 'collection_manager_name', 'finance_company_name','fe_userName',
                'tc_userName'
            ]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                messages.error(request, f'Missing required columns: {", ".join(missing_columns)}')
                return redirect('kg_app:import_tasks')
            
            success_count = 0
            error_count = 0
            errors = []
            
            # Process each row
            for index, row in df.iterrows():
                try:
                    # Skip empty rows
                    if pd.isna(row['aggrement_id']) or pd.isna(row['customer_name']):
                        continue
                    
                    # Validate mobile numbers (should be 10 digits)
                    fe_mobile = str(row['fe_mobile_number']).strip()
                    customer_mobile = str(row['customer_mobile_number']).strip()
                    
                    if not fe_mobile.isdigit() or len(fe_mobile) != 10:
                        errors.append(f"Row {index + 2}: Invalid FE mobile number")
                        error_count += 1
                        continue
                    
                    if not customer_mobile.isdigit() or len(customer_mobile) != 10:
                        errors.append(f"Row {index + 2}: Invalid customer mobile number")
                        error_count += 1
                        continue
                    
                    # Validate pin code (should be 6 digits)
                    pin_code = str(row['pin_code']).strip()
                    if not pin_code.isdigit() or len(pin_code) != 6:
                        errors.append(f"Row {index + 2}: Invalid pin code")
                        error_count += 1
                        continue
                    
                    # Create task
                    task = Create_task(
                        admin_id=admin_id_pk,
                        
                        # Agreement information
                        aggrement_id=str(row['aggrement_id']).strip(),
                        customer_name=str(row['customer_name']).strip(),
                        product_type=str(row['product_type']).strip(),
                        tc_name=str(row['tc_name']).strip(),
                        tc_userName=str(row['tc_userName']).strip(),
                        branch=str(row['branch']).strip(),
                        count_of_cases=str(row['count_of_cases']).strip(),
                        old_or_new=str(row['old_or_new']).strip(),
                        bucket=str(row['bucket']).strip(),
                        mode=str(row['mode']).strip(),
                        npa_status=str(row['npa_status']).strip(),
                        
                        # Financial details
                        pos_amount=str(row['pos_amount']).strip(),
                        total_charges=str(row['total_charges']).strip(),
                        bcc_pending=str(row['bcc_pending']).strip(),
                        penal_pending=str(row['penal_pending']).strip(),
                        emi_amount=str(row['emi_amount']).strip(),
                        emi_due_amount=str(row['emi_due_amount']).strip(),
                        recipt_amount=str(row['recipt_amount']).strip(),
                        recipt_date=str(row['recipt_date']).strip(),
                        disbursement_amount=str(row['disbursement_amount']).strip(),
                        loan_amount=str(row['loan_amount']).strip(),
                        disbursement_date=str(row['disbursement_date']).strip(),
                        emi_start_date=str(row['emi_start_date']).strip(),
                        emi_end_date=str(row['emi_end_date']).strip(),
                        emi_cycle_date=str(row['emi_cycle_date']).strip(),
                        
                        # Vehicle details
                        make=str(row['make']).strip(),
                        manufacturer_description=str(row.get('manufacturer_description', '')).strip() if pd.notna(row.get('manufacturer_description')) else '',
                        registration_number=str(row.get('registration_number', '')).strip() if pd.notna(row.get('registration_number')) else '',
                        vehicle_age=str(row.get('vehicle_age', '')).strip() if pd.notna(row.get('vehicle_age')) else '',
                        
                        # Customer details
                        employer=str(row.get('employer', '')).strip() if pd.notna(row.get('employer')) else '',
                        father_name=str(row['father_name']).strip(),
                        fe_name=str(row['fe_name']).strip(),
                        fe_userName=str(row['fe_userName']).strip(),
                        fe_mobile_number=fe_mobile,
                        customer_mobile_number=customer_mobile,
                        pin_code=pin_code,
                        customer_address=str(row['customer_address']).strip(),
                        customer_office_address=str(row['customer_office_address']).strip(),
                        reference_details=str(row['reference_details']).strip(),
                        
                        # Collection details
                        collection_manager_name=str(row['collection_manager_name']).strip(),
                        finance_company_name=str(row['finance_company_name']).strip()
                    )
                    task.save()
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                    error_count += 1
            
            # Display results
            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} tasks!')
            
            if error_count > 0:
                error_message = f'{error_count} errors occurred:<br>'
                error_message += '<br>'.join(errors[:10])  # Show first 10 errors
                if len(errors) > 10:
                    error_message += f'<br>...and {len(errors) - 10} more errors'
                messages.warning(request, error_message)
            
            if success_count == 0 and error_count == 0:
                messages.info(request, 'No data found in the Excel file')
            
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
        
        return redirect('kg_app:import_tasks')
    
    return render(request, 'create_task.html')

def download_task_sample_excel(request):
    """Generate and download a sample Excel template for tasks"""
    import io
    from django.http import HttpResponse
    
    # Create sample data with all columns
    sample_data = {
        # Agreement information
        'aggrement_id': ['AGR001', 'AGR002'],
        'customer_name': ['John Doe', 'Jane Smith'],
        'product_type': ['Auto Loan', 'Personal Loan'],
        'tc_name': ['TC001', 'TC002'],
        'tc_userName': ['TC-002', 'TC-003'],
        'branch': ['Mumbai', 'Delhi'],
        'count_of_cases': ['5', '3'],
        'old_or_new': ['New', 'Old'],
        'bucket': ['Bucket1', 'Bucket2'],
        'mode': ['Online', 'Offline'],
        'npa_status': ['Active', 'Inactive'],
        
        # Financial details
        'pos_amount': ['500000', '300000'],
        'total_charges': ['50000', '30000'],
        'bcc_pending': ['5000', '3000'],
        'penal_pending': ['2000', '1000'],
        'emi_amount': ['10000', '8000'],
        'emi_due_amount': ['10000', '8000'],
        'recipt_amount': ['10000', '8000'],
        'recipt_date': ['2024-01-15', '2024-01-20'],
        'disbursement_amount': ['500000', '300000'],
        'loan_amount': ['500000', '300000'],
        'disbursement_date': ['2024-01-01', '2024-01-05'],
        'emi_start_date': ['2024-02-01', '2024-02-05'],
        'emi_end_date': ['2029-01-01', '2029-01-05'],
        'emi_cycle_date': ['1', '5'],
        
        # Vehicle details
        'make': ['Honda City', 'Maruti Swift'],
        'manufacturer_description': ['Honda City 2023 Model', 'Maruti Swift VXI'],
        'registration_number': ['MH01AB1234', 'DL02CD5678'],
        'vehicle_age': ['1 year', '2 years'],
        
        # Customer details
        'employer': ['ABC Corp', 'XYZ Ltd'],
        'father_name': ['Robert Doe', 'David Smith'],
        'fe_name': ['Agent A', 'Agent B'],
        'fe_userName': ['FE-002', 'FE-003'],
        'fe_mobile_number': ['9876543210', '8765432109'],
        'customer_mobile_number': ['9123456789', '8234567890'],
        'pin_code': ['400001', '110001'],
        'customer_address': ['123 Main St, Mumbai', '456 Park Ave, Delhi'],
        'customer_office_address': ['789 Business Park, Mumbai', '321 Corporate Tower, Delhi'],
        'reference_details': ['Friend: Mike, 9999999999', 'Brother: Tom, 8888888888'],
        
        # Collection details
        'collection_manager_name': ['Manager A', 'Manager B'],
        'finance_company_name': ['ABC Finance', 'XYZ Finance']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Tasks')
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Tasks']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=task_import_template.xlsx'
    
    return response

def update_task(request):
    session_admin_id = request.session.get('admin_id')
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    session_admin_username= request.session.get('admin_username')
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    if request.method == "POST":
        aggrement_id = request.POST.get("agreement_id")
        print("Agreement ID for task update:", aggrement_id)
        print("Agreement ID for task update:", request.POST)
        task_id = request.POST.get("task_id")
        model_task_id = Create_task.objects.get(pk = task_id)
        
        # contact information
        code = request.POST.get("code")
        new_mobile_number = request.POST.get("newMobileNumber")

        # projection details 
        projection = request.POST.get("projection")
        promise_date = request.POST.get("promise_date")
        promise_amount = request.POST.get("promise_amt")
        
        # remark 
        customer_remark = request.POST.get("customer_remark")
        reference_remark = request.POST.get("referencr_remark")
        
        #visit details
        need_group_visit = request.POST.get("need_group_visit")
        visit_projection = request.POST.get("visit_projection")
        visit_status = request.POST.get("visit_status")
        
        # customer & vehicle details
        customer_available = request.POST.get("customer_available")
        vehicle_available = request.POST.get("vehicle_available")
        third_party_status = request.POST.get("third_party_status")
        third_party_details = request.POST.get("third_party_details")
        
        # location & status
        new_update_address = request.POST.get("new_update_address")
        document_image = request.FILES.get("document_image")
        location_status = request.POST.get("location_status")

        # payment details 
        recipt_no = request.POST.get("recipt_no")
        payment_mode = request.POST.get("payment_mode")
        payment_amount = request.POST.get("payment_amount")
        payment_date = request.POST.get("payment_date")
        
        task_update.objects.create(
            updated_by = session_admin_username,
            admin_id = admin_id_pk,
            task_id = model_task_id,
            agreement_id = aggrement_id,
            
            # contact information
            code = code,
            new_mobile_number = new_mobile_number,
            
            # projection details 
            projection = projection,
            promise_date = promise_date if promise_date else None,
            promise_amount = promise_amount,
            
            # remark 
            customer_remark = customer_remark,
            reference_remark = reference_remark,
            
            # visit details
            need_group_visit = need_group_visit,
            visit_projection = visit_projection,
            visit_status = visit_status,
            
            # customer & vehicle details
            customer_available = customer_available,
            vehicle_available = vehicle_available,
            third_party_status = third_party_status,
            third_party_details = third_party_details,
            
            # location and status 
            new_update_address = new_update_address,
            document_image = document_image,
            location_status = location_status,
            
            # payment details 
            recipt_no = recipt_no,
            payment_mode = payment_mode,
            payment_amount = payment_amount,
            payment_date = payment_date if payment_date else None
            
        )
        
       # to update category in Create_task model later
        update = Create_task.objects.get(pk=task_id)
        update.category = code if code else None
        update.status = location_status if location_status else None
        update.new_mobile_number = new_mobile_number if new_mobile_number else None

        # projection details - handle empty strings for date fields
        update.update_promise_date = promise_date if promise_date and promise_date.strip() else None
        update.update_promise_amount = promise_amount if promise_amount else None

        # remark 
        update.update_customer_remark = customer_remark if customer_remark else None
        update.update_reference_remark = reference_remark if reference_remark else None

        # visit details 
        update.update_need_group_visit = need_group_visit if need_group_visit else None
        update.update_visit_projection = visit_projection if visit_projection else None

        # customer & vehicle details 
        update.update_customer_available = customer_available if customer_available else None
        update.update_vehicle_available = vehicle_available if vehicle_available else None
        update.update_third_party_status = third_party_status if third_party_status else None
        update.update_third_party_details = third_party_details if third_party_details else None

        # location & status
        update.update_new_address = new_update_address if new_update_address else None
        update.update_location_status = location_status if location_status else None

        # payment details
        update.update_recipt_no = recipt_no if recipt_no else None
        update.update_payment_mode = payment_mode if payment_mode else None
        update.update_payment_amount = payment_amount if payment_amount else None
        update.update_payment_date = payment_date if payment_date and payment_date.strip() else None

        update.save()
        
        messages.success(request, 'task updated successfully')
        return redirect("kg_app:assign_task")
          
    return render(request, "assign_task.html")

def dashboard(request):
    notification(request)  # Call the notification function to update notifications
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    
    create_user_list = CreateUser.objects.filter(admin_id = admin_id_pk)
    create_task_list = Create_task.objects.filter(admin_id = admin_id_pk)[:3]
    user_length = len(create_user_list)
    print("Total users:", user_length)
    
    # Filter users by role
    telecallers_queryset = create_user_list.filter(role='telecaller')
    teamleads_queryset = create_user_list.filter(role='teamlead')
    groundstaff_queryset = create_user_list.filter(role='groundstaff')
    
    telecallers = list(telecallers_queryset[:5].values(
        'id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'active_session_key'
    ))
    
    teamleads = list(teamleads_queryset[:5].values(
        'id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'active_session_key'
    ))
    
    groundstaff = list(groundstaff_queryset[:5].values(
        'id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'active_session_key'
    ))
    
    # Add online/offline status based on active_session_key
    for user in telecallers:
        user['status'] = 'online' if user['active_session_key'] else 'offline'
    
    for user in teamleads:
        user['status'] = 'online' if user['active_session_key'] else 'offline'
    
    for user in groundstaff:
        user['status'] = 'online' if user['active_session_key'] else 'offline'
    
    tc_login = TcLogin.objects.filter(admin_id = session_admin_id)
    tl_login = TlLogin.objects.filter(admin_id = session_admin_id)
    gs_login = GsLogin.objects.filter(admin_id = session_admin_id)
    login_status_len = len(tc_login) + len(tl_login) + len(gs_login)
    # login_status_len = 5
    print("Total login status entries:", login_status_len)
    
    task_list = Create_task.objects.filter(admin_id = session_admin_id)
    task_length = len(task_list)
    
    # Convert to JSON for JavaScript
    telecallers_json = json.dumps(telecallers)
    teamleads_json = json.dumps(teamleads)
    groundstaff_json = json.dumps(groundstaff)
    
    leave_requests = leave_request.objects.filter(
        admin_id = admin_id_pk,
        leave_status = 'Pending'
    )
    
    leave_request_data = leave_request.objects.filter(
        admin_id=admin_id_pk
    ).order_by('-submit_time')[:3]
    print(f"Pending leave requests count: {leave_request_data}")

    leave_requests_length = len(leave_requests)
    
    return render(request, "dashboard.html", {
        "user_length":user_length, 
        "login_status_len":login_status_len,
        "leave_requests_length":leave_requests_length,
        "leave_request_data":leave_request_data,
        "task_length":task_length,
        "user_list":create_user_list,
        "task_list":create_task_list,
        "telecallers_json": telecallers_json,
        "teamleads_json": teamleads_json,
        "groundstaff_json": groundstaff_json,
        })

def groundstaff(request):
    session_admin_id = request.session.get('admin_id')
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    staff_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'groundstaff'
    )
    return render(request, "groundstaff.html",{"data":staff_list})

def gs_login(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    login_status = GsLogin.objects.filter(admin_id = session_admin_id).order_by('-login_time')
    
    print(f"Ground Staff Login Status Count: {login_status.count()}")
    
    return render(request, "gs_login.html", {"login_status":login_status})

def leave(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    leave_request_list = leave_request.objects.filter(admin_id = session_admin_id).order_by('-submit_time')
    return render(request, "leave.html", {"leave_request_list":leave_request_list})

def get_leave_details(request):
    if request.method == 'GET':
        leave_id = request.GET.get('leave_id')
        try:
            leave = leave_request.objects.get(leave_id=leave_id)
            data = {
                'success': True,
                'data': {
                    'leave_id': leave.leave_id,
                    'user_name': leave.user_name,
                    'user_email': leave.user_email,
                    'user_mobile': leave.user_mobile,
                    'role': leave.role,
                    'leave_type': leave.leave_type,
                    'from_date': leave.from_date.strftime('%Y-%m-%d'),
                    'to_date': leave.to_date.strftime('%Y-%m-%d'),
                    'full_day_half': leave.full_day_half,
                    'leave_reason': leave.leave_reason,
                    'leave_desc': leave.leave_desc,
                    'leave_status': leave.leave_status,
                    'submit_time': leave.submit_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'reject_reason': leave.reject_reason
                }
            }
            return JsonResponse(data)
        except leave_request.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Leave request not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def approve_leave(request):
    if request.method == 'POST':
        # Get the session admin_id
        session_admin_id = request.session.get("admin_id")
        
        # Check if admin is logged in
        if not session_admin_id:
            return render(request, 'index.html')
        
        leave_id = request.POST.get('leave_id')
        
        print(f"Approving leave ID: {leave_id} by admin ID: {session_admin_id}")
        
        try:
            # Filter by leave_id, admin_id, and ensure status is Pending
            leave = leave_request.objects.get(
                leave_id=leave_id,
                leave_status='Pending'
            )
            
            # Update status to Approved
            leave.leave_status = 'Approved'
            leave.save()
            
            return redirect("kg_app:leave")

            
        except leave_request.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Leave request not found or already processed'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error: {str(e)}'
            })
    
    return render(request, "leave.html")

def reject_leave(request):
    if request.method == 'POST':
        # Get the session admin_id
        session_admin_id = request.session.get("admin_id")
        
        # Check if admin is logged in
        if not session_admin_id:
            return render(request, 'index.html')
        
        # leave_id = request.POST.get('leave_id')
        reject_reason = request.POST.get('reject_reason')
        
        leave_id = request.POST.get('rej_leave_id')
        
        print(f"Approving leave ID: {leave_id} by admin ID: {session_admin_id}")
        
        # Validate reject reason
        if not reject_reason or not reject_reason.strip():
            return JsonResponse({'success': False, 'message': 'Rejection reason is mandatory'})
        
        try:
            # Filter by leave_id, admin_id, and ensure status is Pending
            leave = leave_request.objects.get(
                leave_id=leave_id,
                leave_status='Pending'
            )
            
            # Update status to Rejected and save reason
            leave.leave_status = 'Rejected'
            leave.reject_reason = reject_reason
            leave.save()
            
            return redirect("kg_app:leave")
            
        except leave_request.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Leave request not found or already processed'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def pending_task(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    create_task_list = Create_task.objects.filter(
        admin_id=admin_id_pk
    ).filter(
        Q(update_location_status = "RF") |
        Q(update_location_status__isnull = True) |
        Q(update_location_status = "")
    )
    
    return render(request, "pending_task.html", {"create_task_list" : create_task_list})

def task_delete(request, id):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    emp = get_object_or_404(Create_task, task_id=id)
    emp.delete()
    return redirect('kg_app:pending_task')   # change to your list page URL name

def tc_login(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    login_status = TcLogin.objects.filter(admin_id = session_admin_id).order_by('-login_time')
    return render(request, "tc_login.html", {"login_status":login_status})

def teamlead(request):
    session_admin_id = request.session.get('admin_id')
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    caller_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'teamlead'
    )
    return render(request, "teamlead.html",{"data":caller_list})

def telecaller(request):
    session_admin_id = request.session.get('admin_id')
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk  = admin_user_model.objects.get(pk = session_admin_id)
    user_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'telecaller'
    )
    return render(request, "telecaller.html",{"data":user_list})

def tl_login(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    login_status = TlLogin.objects.filter(admin_id = session_admin_id).order_by('-login_time')
    return render(request, "tl_login.html", {"login_status":login_status})

def tc_delete(request, id):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    emp = get_object_or_404(CreateUser, id=id)
    emp.delete()
    return redirect('kg_app:telecaller')   # change to your list page URL name

def tl_delete(request, id):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    emp = get_object_or_404(CreateUser, id=id)
    emp.delete()
    return redirect('kg_app:teamlead')   # change to your list page URL name

def gs_delete(request, id):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    emp = get_object_or_404(CreateUser, id=id)
    emp.delete()
    return redirect('kg_app:groundstaff')   # change to your list page URL name

def feddback_history(request):
    session_admin_id = request.session.get("admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk=session_admin_id)
    
    feedback = task_update.objects.filter(
        admin_id = admin_id_pk
    )
    
    return render(request, "feedback_history.html", {"feedback":feedback})    
    
def notification(request):
    # Fetch 4 most recent task updates ordered by updated_at (most recent first)
    # recent_updates = task_update.objects.select_related('admin_id', 'task_id').order_by('-updated_at')[:4]
    recent_updates = task_update.objects.all()[:4]
    
    # Get the count of total updates (for the badge)
    notification_count = task_update.objects.count()
    
    context = {
        'recent_updates': recent_updates,
        'notification_count': notification_count,
    }
    
    return render(request, 'common/header.html', context)





#                ***********************
#           *****                       *****
#        ***                                 ***
#      **                                       **
#     **                                         **
#    **            ***********************         **
#    **           *     TELECALLER VIEW    *       **
#    **            ***********************         **
#     **                                         **
#      **                                       **
#        ***                                 ***
#           *****                       *****
#                ***********************



def tc_dashboard(request):
    session_tc_id = request.session.get("tc_admin_id")
    # navigate to login page if not login
    if not session_tc_id:
        return render(request, 'index.html')
    return render(request, "tc_screens/tc_dashboard.html")

def tc_teamlead(request):
    session_admin_id = request.session.get('tc_admin_id')
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    caller_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'teamlead'
    )
    return render(request, "tc_screens/tc_teamlead.html",{"data":caller_list})

def tc_groundstaff(request):
    session_admin_id = request.session.get('tc_admin_id')
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    staff_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'groundstaff'
    )
    return render(request, "tc_screens/tc_groundstaff.html",{"data":staff_list})

def tc_tl_login(request):
    session_admin_id = request.session.get("tc_admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    
    return render(request, "tc_screens/tc_tl_login.html")

def tc_gs_login(request):
    session_admin_id = request.session.get("tc_admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    return render(request, "tc_screens/tc_gs_login.html")

def tc_assign_task(request):
    session_admin_id = request.session.get('tc_admin_id')
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    create_task_list = Create_task.objects.filter(
        admin_id = admin_id_pk
    )
    update_task_list = task_update.objects.all()

     # Convert queryset to JSON with all fields from your model
    updated_task_list_json = json.dumps(list(update_task_list.values(
        'task_update_id',
        'updated_by',
        'updated_at',
        'agreement_id',
        'code',
        'new_mobile_number',
        'projection',
        'promise_date',
        'promise_amount',
        'customer_remark',
        'reference_remark',
        'need_group_visit',
        'visit_projection',
        'visit_status',
        'customer_available',
        'vehicle_available',
        'third_party_status',
        'third_party_details',
        'new_update_address',
        'location_image',
        'document_image',
        'location_status',
        'recipt_no',
        'payment_mode',
        'payment_amount',
        'payment_date'
    )), default=str)
    
    return render(request, "tc_screens/tc_assign_task.html", {
        "task_list":create_task_list, 
        "updated_task_list":update_task_list,
        "updated_task_list_json": updated_task_list_json
        })

def tc_pending_task(request):
    session_admin_id = request.session.get("tc_admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    return render(request, "tc_screens/tc_pending_task.html")

def tc_complete_task(request):
    session_admin_id = request.session.get("tc_admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    return render(request, "tc_screens/tc_complete_task.html")

def tc_leave(request):
    session_admin_id = request.session.get("tc_admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    return render(request, "tc_screens/tc_leave.html")

def tc_feddback_history(request):
    session_admin_id = request.session.get("tc_admin_id")
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk=session_admin_id)
    
    feedback = task_update.objects.filter(
        admin_id = admin_id_pk
    )
    
    return render(request, "tc_screens/tc_feedback_history.html", {"feedback":feedback})  

def tc_update_task(request):
    session_admin_id = request.session.get('tc_admin_id')
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    session_admin_username= request.session.get('tc_first_name')
    # navigate to login page if not login
    if not session_admin_id:
        return render(request, 'index.html')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    if request.method == "POST":
        aggrement_id = request.POST.get("agreement_id")
        print("Agreement ID for task update:", aggrement_id)
        print("Agreement ID for task update:", request.POST)
        task_id = request.POST.get("task_id")
        model_task_id = Create_task.objects.get(pk = task_id)
        
        # contact information
        code = request.POST.get("code")
        new_mobile_number = request.POST.get("newMobileNumber")

        # projection details 
        projection = request.POST.get("projection")
        promise_date = request.POST.get("promise_date")
        promise_amount = request.POST.get("promise_amt")
        
        # remark 
        customer_remark = request.POST.get("customer_remark")
        reference_remark = request.POST.get("referencr_remark")
        
        #visit details
        need_group_visit = request.POST.get("need_group_visit")
        visit_projection = request.POST.get("visit_projection")
        visit_status = request.POST.get("visit_status")
        
        # customer & vehicle details
        customer_available = request.POST.get("customer_available")
        vehicle_available = request.POST.get("vehicle_available")
        third_party_status = request.POST.get("third_party_status")
        third_party_details = request.POST.get("third_party_details")
        
        # location & status
        new_update_address = request.POST.get("new_update_address")
        document_image = request.FILES.get("document_image")
        location_status = request.POST.get("location_status")

        # payment details 
        recipt_no = request.POST.get("recipt_no")
        payment_mode = request.POST.get("payment_mode")
        payment_amount = request.POST.get("payment_amount")
        payment_date = request.POST.get("payment_date")
        
        task_update.objects.create(
            updated_by = session_admin_username,
            admin_id = admin_id_pk,
            task_id = model_task_id,
            agreement_id = aggrement_id,
            
            # contact information
            code = code,
            new_mobile_number = new_mobile_number,
            
            # projection details 
            projection = projection,
            promise_date = promise_date if promise_date else None,
            promise_amount = promise_amount,
            
            # remark 
            customer_remark = customer_remark,
            reference_remark = reference_remark,
            
            # visit details
            need_group_visit = need_group_visit,
            visit_projection = visit_projection,
            visit_status = visit_status,
            
            # customer & vehicle details
            customer_available = customer_available,
            vehicle_available = vehicle_available,
            third_party_status = third_party_status,
            third_party_details = third_party_details,
            
            # location and status 
            new_update_address = new_update_address,
            document_image = document_image,
            location_status = location_status,
            
            # payment details 
            recipt_no = recipt_no,
            payment_mode = payment_mode,
            payment_amount = payment_amount,
            payment_date = payment_date if payment_date else None
            
        )
        
       # to update category in Create_task model later
        update = Create_task.objects.get(pk=task_id)
        update.category = code if code else None
        update.status = location_status if location_status else None
        update.new_mobile_number = new_mobile_number if new_mobile_number else None

        # projection details - handle empty strings for date fields
        update.update_promise_date = promise_date if promise_date and promise_date.strip() else None
        update.update_promise_amount = promise_amount if promise_amount else None

        # remark 
        update.update_customer_remark = customer_remark if customer_remark else None
        update.update_reference_remark = reference_remark if reference_remark else None

        # visit details 
        update.update_need_group_visit = need_group_visit if need_group_visit else None
        update.update_visit_projection = visit_projection if visit_projection else None

        # customer & vehicle details 
        update.update_customer_available = customer_available if customer_available else None
        update.update_vehicle_available = vehicle_available if vehicle_available else None
        update.update_third_party_status = third_party_status if third_party_status else None
        update.update_third_party_details = third_party_details if third_party_details else None

        # location & status
        update.update_new_address = new_update_address if new_update_address else None
        update.update_location_status = location_status if location_status else None

        # payment details
        update.update_recipt_no = recipt_no if recipt_no else None
        update.update_payment_mode = payment_mode if payment_mode else None
        update.update_payment_amount = payment_amount if payment_amount else None
        update.update_payment_date = payment_date if payment_date and payment_date.strip() else None

        update.save()
        
        messages.success(request, 'task updated successfully')
        return redirect("kg_app:tc_assign_task")
          
    return render(request, "tc_screens/tc_assign_task.html") 




#                ***********************
#           *****                       *****
#        ***                                 ***
#      **                                       **
#     **                                         **
#    **            ***********************         **
#    **           *     API VIEW            *       **
#    **            ***********************         **
#     **                                         **
#      **                                       **
#        ***                                 ***
#           *****                       *****
#                ***********************






# api for updating api_image_status field in Create_task model
@api_view(['PATCH', 'POST'])
def update_api_image_status_drf(request):
    """
    Update only the api_image_status field for a specific task
    """
    task_id = request.data.get('task_id')
    new_status = request.data.get('api_image_status')
    
    # Validation
    if not task_id:
        return Response({
            'success': False,
            'message': 'task_id is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not new_status:
        return Response({
            'success': False,
            'message': 'api_image_status is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        task = Create_task.objects.get(task_id=task_id)
        task.api_image_status = new_status
        task.save(update_fields=['api_image_status'])
        
        return Response({
            'success': True,
            'message': 'API image status updated successfully',
            'data': {
                'task_id': task.task_id,
                'api_image_status': task.api_image_status
            }
        }, status=status.HTTP_200_OK)
        
    except Create_task.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Task with id {task_id} not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
              
        
        
@api_view(['POST'])
def create_gs_login(request):
    """
    API to create a new GS Login record
    Required fields: admin_id, name, email, mobile_no, status, image, longitude, latitude
    """
    try:
        # Get data from request
        user_id = request.data.get('user_id')
        admin_id = request.data.get('admin_id')
        name = request.data.get('name')
        email = request.data.get('email')
        mobile_no = request.data.get('mobile_no')
        status_value = request.data.get('status')
        image = request.FILES.get('image')
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')
        login_time = request.data.get('login_time', None)
        logout_time = request.data.get('logout_time', None)

        # Validate required fields
        if not all([user_id, admin_id, name, email, mobile_no, status_value, image, longitude, latitude, login_time]):
            return Response({
                'success': False,
                'message': 'All fields are required: user_id, admin_id, name, email, mobile_no, status, image, longitude, latitude, login_time'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        # if GsLogin.objects.filter(email=email).exists():
        #     return Response({
        #         'success': False,
        #         'message': 'Email already exists'
        #     }, status=status.HTTP_400_BAD_REQUEST)

        # # Check if mobile number already exists
        # if GsLogin.objects.filter(mobile_no=mobile_no).exists():
        #     return Response({
        #         'success': False,
        #         'message': 'Mobile number already exists'
        #     }, status=status.HTTP_400_BAD_REQUEST)

        # Create new GsLogin record
        try:
            user = CreateUser.objects.get(pk=user_id)
        except CreateUser.DoesNotExist:
            return Response({
                'success': False,
                'message': f'User with id {user_id} does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        gs_login = GsLogin.objects.create(
            user_id=user,
            admin_id=admin_id,
            name=name,
            email=email,
            mobile_no=mobile_no,
            status=status_value,
            image=image,
            longitude=longitude,
            latitude=latitude,
            login_time=login_time if login_time else None,
            logout_time=logout_time if logout_time else None
        )

        # Serialize and return the created object
        serializer = GsLoginSerializer(gs_login)
        
        return Response({
            'success': True,
            'message': 'GS Login record created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        



 # User Login API


@api_view(['POST'])
def create_tl_login(request):
    """
    API to create a new GS Login record
    Required fields: admin_id, name, email, mobile_no, status, image, longitude, latitude
    """
    try:
        # Get data from request
        user_id = request.data.get('user_id')
        admin_id = request.data.get('admin_id')
        name = request.data.get('name')
        email = request.data.get('email')
        mobile_no = request.data.get('mobile_no')
        status_value = request.data.get('status')
        image = request.FILES.get('image')
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')
        login_time = request.data.get('login_time', None)
        logout_time = request.data.get('logout_time', None)

        # Validate required fields
        if not all([user_id, admin_id, name, email, mobile_no, status_value, image, longitude, latitude, login_time]):
            return Response({
                'success': False,
                'message': 'All fields are required: user_id, admin_id, name, email, mobile_no, status, image, longitude, latitude, login_time'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        # if GsLogin.objects.filter(email=email).exists():
        #     return Response({
        #         'success': False,
        #         'message': 'Email already exists'
        #     }, status=status.HTTP_400_BAD_REQUEST)

        # # Check if mobile number already exists
        # if GsLogin.objects.filter(mobile_no=mobile_no).exists():
        #     return Response({
        #         'success': False,
        #         'message': 'Mobile number already exists'
        #     }, status=status.HTTP_400_BAD_REQUEST)

        # Create new GsLogin record
        try:
            user = CreateUser.objects.get(pk=user_id)
        except CreateUser.DoesNotExist:
            return Response({
                'success': False,
                'message': f'User with id {user_id} does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        tl_login = TlLogin.objects.create(
            user_id=user,
            admin_id=admin_id,
            name=name,
            email=email,
            mobile_no=mobile_no,
            status=status_value,
            image=image,
            longitude=longitude,
            latitude=latitude,
            login_time=login_time if login_time else None,
            logout_time=logout_time if logout_time else None
        )

        # Serialize and return the created object
        serializer = TlLoginSerializer(tl_login)
        
        return Response({
            'success': True,
            'message': 'TL Login record created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data = request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = CreateUser.objects.get(email=email)
            
            if user.role == 'telecaller':
                return Response({
                    'success': False,
                    'message': 'Telecaller users are not allowed to login here'
                }, status=status.HTTP_401_UNAUTHORIZED)
            # Check if password matches (plain text comparison for now)
            if user.password == password:
                return Response({
                    'success': True,
                    'message': 'User login successful',
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'role': user.role,
                        'my_admin_id': user.admin_id.admin_id,
                        'phone_number': user.phone_number,
                        'password': user.password,
                        'isMobile_login': user.isMobile_login,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid user Id or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except CreateUser.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        


@api_view(['GET'])
def get_tasks(request):
    """
    GET endpoint to retrieve tasks with optional admin_id filter
    URL: /api/tasks/get/?admin_id=<id>
    """
    admin_id = request.query_params.get('admin_id', None)
    
    if admin_id:
        tasks = Create_task.objects.filter(admin_id=admin_id)
    else:
        tasks = Create_task.objects.all()
    
    serializer = TaskSerializer(tasks, many=True)
    
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_task_by_id(request, task_id):
    """
    GET endpoint to retrieve a single task by task_id
    URL: /api/tasks/get/<task_id>/
    """
    try:
        task = Create_task.objects.get(task_id=task_id)
    except Create_task.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Task not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Optional: Filter by admin_id if provided
    admin_id = request.query_params.get('admin_id', None)
    if admin_id and str(task.admin_id.id) != admin_id:
        return Response({
            'success': False,
            'message': 'Unauthorized access'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TaskSerializer(task)
    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
def update_api_task(request, task_id):
    """
    PUT/PATCH endpoint to update a task by task_id
    URL: /api/tasks/update/<task_id>/
    """
    try:
        task = Create_task.objects.get(task_id=task_id)
    except Create_task.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Task not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Optional: Filter by admin_id if provided
    admin_id = request.query_params.get('admin_id', None)
    if admin_id and str(task.admin_id.id) != admin_id:
        return Response({
            'success': False,
            'message': 'Unauthorized access to update this task'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Use partial=True for PATCH requests
    partial = request.method == 'PATCH'
    serializer = TaskUpdateSerializerMain(task, data=request.data, partial=partial)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Task updated successfully'
            # 'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Validation error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def get_task_updates(request):
    """
    GET endpoint to retrieve task updates with filters
    URL: /api/task-updates/get/
    Query Parameters:
        - admin_id: Filter by admin ID
        - task_id: Filter by task ID
        - agreement_id: Filter by agreement ID
    """
    admin_id = request.query_params.get('admin_id', None)
    task_id = request.query_params.get('task_id', None)
    agreement_id = request.query_params.get('agreement_id', None)
    
    # Start with all task updates
    task_updates = task_update.objects.all()
    
    # Apply filters
    if admin_id:
        task_updates = task_updates.filter(admin_id=admin_id)
    
    if task_id:
        task_updates = task_updates.filter(task_id=task_id)
    
    if agreement_id:
        task_updates = task_updates.filter(agreement_id=agreement_id)
    
    # Order by latest first
    task_updates = task_updates.order_by('-updated_at')
    
    serializer = TaskUpdateSerializer(task_updates, many=True)
    
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_task_update_by_id(request, task_update_id):
    """
    GET endpoint to retrieve a single task update by ID
    URL: /api/task-updates/get/<task_update_id>/
    """
    try:
        task_update_obj = task_update.objects.get(task_update_id=task_update_id)
    except task_update.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Task update not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Optional: Filter by admin_id if provided
    admin_id = request.query_params.get('admin_id', None)
    if admin_id and str(task_update_obj.admin_id.id) != admin_id:
        return Response({
            'success': False,
            'message': 'Unauthorized access'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TaskUpdateSerializer(task_update_obj)
    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_task_update(request):
    """
    POST endpoint to create a new task update
    URL: /api/task-updates/create/
    Supports both JSON and multipart/form-data (for file uploads)
    """
    serializer = TaskUpdateCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        task_update_obj = serializer.save()
        
        # Return the created object with all details
        response_serializer = TaskUpdateSerializer1(task_update_obj)
        
        return Response({
            'success': True,
            'message': 'Task update created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Validation error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
       
class TaskUpdateCreateAPI(APIView):

    def post(self, request):
        serializer = TaskUpdateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Task update created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



class UpdateMobileLoginAPI(APIView):
    def patch(self, request, user_id):
        user = get_object_or_404(CreateUser, id=user_id)

        serializer = UpdateMobileLoginSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Mobile login status updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "status": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_gs_login_by_user_id(request, user_id):
    try:
        gs_login = GsLogin.objects.get(user_id=user_id)

        data = {
            "gs_login_id": gs_login.gs_login_id,
            "user_id": gs_login.user_id.id if gs_login.user_id else None,
            "admin_id": gs_login.admin_id,
            "name": gs_login.name,
            "email": gs_login.email,
            "mobile_no": gs_login.mobile_no,
            "status": gs_login.status,
            "login_time": gs_login.login_time,
            "logout_time": gs_login.logout_time,
            "image": gs_login.image.name if gs_login.image else None,
            "latitude": gs_login.latitude,
            "longitude": gs_login.longitude,
        }

        return Response({
            "status": True,
            "message": "GS login fetched successfully",
            "data": data
        }, status=status.HTTP_200_OK)

    except GsLogin.DoesNotExist:
        return Response({
            "status": False,
            "message": "No GS login found for this user"
        }, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def get_tl_login_by_user_id(request, user_id):
    try:
        tl_login = TlLogin.objects.get(user_id=user_id)

        data = {
            "tl_login_id": tl_login.tl_login_id,
            "user_id": tl_login.user_id.id if tl_login.user_id else None,
            "admin_id": tl_login.admin_id,
            "name": tl_login.name,
            "email": tl_login.email,
            "mobile_no": tl_login.mobile_no,
            "status": tl_login.status,
            "login_time": tl_login.login_time,
            "logout_time": tl_login.logout_time,
            "image": tl_login.image.name if tl_login.image else None,
            "latitude": tl_login.latitude,
            "longitude": tl_login.longitude,
        }

        return Response({
            "status": True,
            "message": "GS login fetched successfully",
            "data": data
        }, status=status.HTTP_200_OK)

    except GsLogin.DoesNotExist:
        return Response({
            "status": False,
            "message": "No GS login found for this user"
        }, status=status.HTTP_404_NOT_FOUND)



# @api_view(['PATCH'])
# # @parser_classes([MultiPartParser, FormParser])
# def update_gs_login(request, gs_login_id):

#     gs_login = get_object_or_404(GsLogin, pk=gs_login_id)
    
#     print("Request data: ------------------- ", gs_login_id, request.data)

#     serializer = GsLoginUpdateSerializer(
#         gs_login,
#         data=request.data,
#         partial=True
#     )

#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {
#                 "status": True,
#                 "message": "GS login updated successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

#     return Response(
#         {
#             "status": False,
#             "errors": serializer.errors
#         },
#         status=status.HTTP_400_BAD_REQUEST
#     )
    
    
@api_view(['PATCH'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def update_gs_login(request, gs_login_id):
    try:
        gs_login = GsLogin.objects.get(gs_login_id=gs_login_id)
    except GsLogin.DoesNotExist:
        return Response(
            {"error": "GS Login not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GsLoginUpdateSerializer(
        gs_login,
        data=request.data,
        partial=True   # 🔥 THIS makes PATCH work
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "GS Login updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def update_tl_login(request, tl_login_id):
    try:
        tl_login = TlLogin.objects.get(tl_login_id=tl_login_id)
    except TlLogin.DoesNotExist:
        return Response(
            {"error": "GS Login not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TlLoginUpdateSerializer(
        tl_login,
        data=request.data,
        partial=True   # 🔥 THIS makes PATCH work
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "GS Login updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestCreateAPIView(APIView):

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Leave request created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class LeaveRequestByUserAPIView(APIView):

    def get(self, request, user_id):
        leaves = leave_request.objects.filter(user_id=user_id)

        if not leaves.exists():
            return Response(
                {"message": "No leave requests found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(
            {
                "message": "Leave requests fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
