from django.shortcuts import render
from . models import *
# Create your views here.


def index(request):
    return render(request, "index.html")


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


