

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
 
    
class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Create_task
        fields = '__all__'
 
        
class GsLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = GsLogin
        fields = '__all__'
        
# get & update task serializer 
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Create_task
        fields = '__all__'
        read_only_fields = ['task_id']


class TaskUpdateSerializerMain(serializers.ModelSerializer):
    class Meta:
        model = Create_task
        fields = [
            # Update details
            'status',
            'new_mobile_number',
            'api_image_status',
            'category',
            
            # Projection details
            'update_promise_date',
            'update_promise_amount',
            
            # Remarks
            'update_customer_remark',
            'update_reference_remark',
            
            # Visit details
            'update_need_group_visit',
            'update_visit_projection',
            
            # Customer & vehicle details
            'update_customer_available',
            'update_vehicle_available',
            'update_third_party_status',
            'update_third_party_details',
            
            # Location & status
            'update_new_address',
            'update_location_status',
            
            # Payment details
            'update_recipt_no',
            'update_payment_mode',
            'update_payment_amount',
            'update_payment_date',
            
            # location details for mobile 
            'latitude',
            'longitude',
        ]
    

# Serializer for task creation & get
class TaskUpdateSerializer1(serializers.ModelSerializer):
    # Read-only fields to display related data
    admin_name = serializers.CharField(source='admin_id.username', read_only=True)
    task_customer_name = serializers.CharField(source='task_id.customer_name', read_only=True)
    
    class Meta:
        model = task_update
        fields = '__all__'
        read_only_fields = ['task_update_id', 'updated_at']


class TaskUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = task_update
        fields = [
            'updated_by',
            'admin_id',
            'task_id',
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
            # 'location_image',
            # 'document_image',
            'location_status',
            'recipt_no',
            'payment_mode',
            'payment_amount',
            'payment_date',
        ]
    
    def validate_admin_id(self, value):
        """Validate that admin_id exists"""
        if not admin_user_model.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid admin_id")
        return value
    
    def validate_task_id(self, value):
        """Validate that task_id exists"""
        if not Create_task.objects.filter(task_id=value.task_id).exists():
            raise serializers.ValidationError("Invalid task_id")
        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    admin_id = serializers.PrimaryKeyRelatedField(
        queryset=admin_user_model.objects.all()
    )
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Create_task.objects.all()
    )

    class Meta:
        model = task_update
        fields = "__all__"

# update login status for mobile to prevent multiple login
class UpdateMobileLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUser
        fields = ['isMobile_login']

#gs punch in update serializer
class GsLoginUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GsLogin
        fields = [
            'status',
            'login_time',
            'logout_time',
            'image',
            'latitude',
            'longitude',
        ]

# leave request post method 
class LeaveRequestSerializer(serializers.ModelSerializer):
    admin_id = serializers.PrimaryKeyRelatedField(
        queryset=admin_user_model.objects.all()
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CreateUser.objects.all()
    )

    class Meta:
        model = leave_request
        fields = [
            'leave_id',
            'admin_id',
            'user_id',
            'user_name',
            'user_email',
            'user_mobile',
            'role',
            'leave_type',
            'from_date',
            'to_date',
            'full_day_half',
            'leave_reason',
            'leave_desc',
            'leave_status',
            'submit_time',
            'reject_reason',
        ]
        read_only_fields = ['leave_id', 'submit_time', 'leave_status']