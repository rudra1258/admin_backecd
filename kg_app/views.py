from django.shortcuts import render, redirect
from django.http import JsonResponse
from . models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import pandas as pd
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

def admin_login(request):
    print("Admin login view called")
    
    # If GET request, show the login page
    if request.method == 'GET':
        return render(request, 'index.html')
    
    # If POST request, handle login
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        print("Login attempt with email:", email)
        print("Password entered:", password)
        
        try:
            # Check if user exists
            admin_user = admin_user_model.objects.get(email=email)
            
            print("password of user:", admin_user)
            print("Provided password:", password)
            print("Stored hashed password:", admin_user.email)
            
            # Verify password
            if (password == admin_user.password):
                
                # Set session
                request.session['admin_id'] = admin_user.admin_id
                request.session['admin_username'] = admin_user.username
                request.session['admin_email'] = admin_user.email
                
                
                
                # Return JSON response for success
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect_url': '/dashboard/'  # Change this to your actual dashboard URL
                })
            else:
                # Return JSON response for invalid password
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid email or password!'
                })  
                
        except admin_user_model.DoesNotExist:
            # Return JSON response for user not found
            return JsonResponse({
                'success': False,
                'message': 'Invalid email or password!'
            })
    return render(request, 'index.html')




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

        CreateUser.objects.create(
            admin_id = admin_id_pk,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            role = role,
            username = username,
            address = address,
            password = password
        )
        # Add success message
        messages.success(request, 'User created successfully!')
        return redirect("kg_app:create_user")

    admins = admin_user_model.objects.all()
    # return redirect("kg_app:create_user")
    return render(request, "create_user.html", {"admins": admins})


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
            return redirect('import_users')
        
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
                        password=make_password(str(row['password']))  # Hash the password
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
    import io
    from django.http import HttpResponse
    
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
    return render(request, "assign_task.html")


def complete_task(request):
    return render(request, "complete_task.html")


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
    
    if request.method == "POST":    
        print("FULL POST:", request.POST)
        
        print("Create Task POST request data: --- -- - ", request.POST.get("prodduct_type"))
           
        # addreement information
        aggrement_id = request.POST.get("agreement_id")
        customer_name = request.POST.get("customer_name")
        product_type = request.POST.get("prodduct_type")
        tc_name = request.POST.get("tc_name")
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
        fe_name = request.POST.get("fe_name")
        fe_Mobile = request.POST.get("fe_Mobile")
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
    
    
    return render(request, "create_task.html", {"users": user_list})



def dashboard(request):
    return render(request, "dashboard.html")


def groundstaff(request):
    session_admin_id = request.session.get('admin_id')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    staff_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'groundstaff'
    )
    return render(request, "groundstaff.html",{"data":staff_list})


def gs_login(request):
    return render(request, "gs_login.html")

def leave(request):
    return render(request, "leave.html")

def pending_task(request):
    return render(request, "pending_task.html")

def tc_login(request):
    return render(request, "tc_login.html")

def teamlead(request):
    session_admin_id = request.session.get('admin_id')
    admin_id_pk = admin_user_model.objects.get(pk = session_admin_id)
    caller_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'teamlead'
    )
    return render(request, "teamlead.html",{"data":caller_list})


def telecaller(request):
    session_admin_id = request.session.get('admin_id')
    admin_id_pk  = admin_user_model.objects.get(pk = session_admin_id)
    user_list = CreateUser.objects.filter(
        admin_id = admin_id_pk,
        role = 'telecaller'
    )
    return render(request, "telecaller.html",{"data":user_list})

def tl_login(request):
    return render(request, "tl_login.html")


