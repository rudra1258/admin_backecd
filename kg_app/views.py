from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
# Create your views here.


# def index(request):
#     return render(request, "index.html")

def admin_login(request):
    print("Admin login view called")
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
            print("Stored hashed password:", admin_user.password)
            
            # Verify password
            if (password == admin_user.password):
            # if (True):
                # Set session
                request.session['admin_id'] = admin_user.admin_id
                request.session['admin_username'] = admin_user.username
                request.session['admin_email'] = admin_user.email
                
                # Set session expiry
                # request.session.set_expiry(60 * 1) # 1 minute for testing
                
                messages.success(request, 'Login successful!')
                return render(request, 'dashboard.html', {'email': email})  # Change to your dashboard URL name
            else:
                messages.error(request, 'Invalid email or password!')
                return render(request, 'index.html', {'email': email})
                
        except admin_user_model.DoesNotExist:
            messages.error(request, 'Invalid email or password!')
            return render(request, 'index.html', {'email': email})
    
    return render(request, 'index.html')


def assign_task(request):
    return render(request, "assign_task.html")


def complete_task(request):
    return render(request, "complete_task.html")


def create_task(request):
    return render(request, "create_task.html")

def create_user(request):
    return render(request, "create_user.html")

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


