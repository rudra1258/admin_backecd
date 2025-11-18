from django.shortcuts import render, redirect
from django.http import JsonResponse
from . models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
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
            
            print("Retrieved user:", admin_user)
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



def assign_task(request):
    return render(request, "assign_task.html")


def complete_task(request):
    return render(request, "complete_task.html")


def create_task(request):
    session_admin_id = request.session.get("admin_id")
    
    # navigate to login page if not login
    if not session_admin_id:
        messages.error(request, 'Please login to continue.')
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
    return render(request, "groundstaff.html")


def gs_login(request):
    return render(request, "gs_login.html")

def leave(request):
    return render(request, "leave.html")

def pending_task(request):
    return render(request, "pending_task.html")

def tc_login(request):
    return render(request, "tc_login.html")

def teamlead(request):
    return render(request, "teamlead.html")

def telecaller(request):
    return render(request, "telecaller.html")

def tl_login(request):
    return render(request, "tl_login.html")


