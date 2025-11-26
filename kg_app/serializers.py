

from rest_framework import serializers
from .models import *

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUser
        # fields = '__all__'
        fields = ['id','admin_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'username', 'address', 'password', 'created_at']

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)