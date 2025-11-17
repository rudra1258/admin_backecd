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
        password = request.POST.get("pass_word")

        CreateUser.objects.create(
            admin_id=session_admin_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            role=role,
            username=username,
            password=password
        )

        return redirect("kg_app:create_user")

    admins = admin_user_model.objects.all()
    return render(request, "create_user.html", {"admins": admins})



def assign_task(request):
    return render(request, "assign_task.html")


def complete_task(request):
    return render(request, "complete_task.html")


def create_task(request):
    return render(request, "create_task.html")



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


