from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta
from .models import *

import jwt
from functools import wraps
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class SingleDeviceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip for login/logout pages
        if request.path in ['/login/', '/logout/', '/']:
            return self.get_response(request)
        
        # Check admin session
        if 'admin_id' in request.session:
            admin_id = request.session.get('admin_id')
            session_key = request.session.session_key
            
            try:
                admin_user = admin_user_model.objects.get(admin_id=admin_id)
                if admin_user.active_session_key != session_key:
                    # Session hijacked or logged in elsewhere
                    request.session.flush()
                    return redirect('/')
            except admin_user_model.DoesNotExist:
                request.session.flush()
                return redirect('/')
        
        # Check telecaller session
        elif 'user_id' in request.session:
            user_id = request.session.get('user_id')
            session_key = request.session.session_key
            
            try:
                user = CreateUser.objects.get(id=user_id)
                if user.active_session_key != session_key:
                    request.session.flush()
                    return redirect('/')
            except CreateUser.DoesNotExist:
                request.session.flush()
                return redirect('/')
        
        response = self.get_response(request)
        return response
    
    
    
# class AutoLogoutMiddleware:
#     """
#     Automatically set GS users to Inactive
#     if login_time is older than 10 hours.
#     Runs on every request.
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):

#         expiry_time = timezone.now() - timedelta(hours=10)

#         # 🔥 One SQL query updates all expired users
#         GsLogin.objects.filter(
#             status="Active",
#             login_time__lte=expiry_time
#         ).update(
#             status="Inactive",
#             logout_time=timezone.now()
#         )
        
#         TlLogin.objects.filter(
#             status="Active",
#             login_time__lte=expiry_time
#         ).update(
#             status="Inactive",
#             logout_time=timezone.now()
#         )
        
#         TcLogin.objects.filter(
#             status="Active",
#             login_time__lte=expiry_time
#         ).update(
#             status="Inactive",
#             logout_time=timezone.now()
#         )

#         response = self.get_response(request)
#         return response

class AutoLogoutMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        expiry_time = timezone.now() - timedelta(hours=10)

        self._auto_logout(GsLogin, expiry_time)
        self._auto_logout(RepoLogin, expiry_time)
        self._auto_logout(TlLogin, expiry_time)
        self._auto_logout(TcLogin, expiry_time)
        

        response = self.get_response(request)
        return response

    def _auto_logout(self, Model, expiry_time):
        # ✅ Evaluate to a real list immediately — no lazy queryset race condition
        expired_user_ids = list(
            Model.objects.filter(
                status="Active",
                login_time__lte=expiry_time,
                user_id__isnull=False   # ✅ skip null user_id foreign keys
            ).values_list('user_id', flat=True)
        )

        if not expired_user_ids:
            return  # nothing to do, skip all queries

        # ✅ Now safely update the login model
        Model.objects.filter(
            status="Active",
            login_time__lte=expiry_time
        ).update(status="Inactive", logout_time=timezone.now())

        # ✅ Mirror the status to CreateUser
        CreateUser.objects.filter(id__in=expired_user_ids).update(login_status="Inactive")
        

def jwt_required(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return Response({'error': 'Authorization token missing.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            admin = admin_user_model.objects.get(admin_id=payload['admin_id'])

            if admin.active_session_key != token:
                return Response({'error': 'Session expired or logged in elsewhere.'}, status=status.HTTP_401_UNAUTHORIZED)

            request.admin = admin

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.InvalidTokenError, admin_user_model.DoesNotExist):
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

        return f(request, *args, **kwargs)
    return decorated
        
        
        
        
        