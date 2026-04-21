from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

admin.site.site_header = "STAFFLYNK Superadmin"
admin.site.site_title = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Dashboard"


admin.site.register(task_update)

@admin.register(admin_user_model)
class AdminUserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "mobile_number", "created_at")
    search_fields = ("username","email")

@admin.register(CreateUser)
class CreateUserAdmin(admin.ModelAdmin):
    list_display = ("admin_id","id","first_name","last_name","email","phone_number","role","username","address","created_at")
    search_fields = ("first_name","last_name","email","phone_number","username")
    list_filter = ("role","created_at","admin_id")


@admin.register(TcLogin)
class TcLoginAdmin(admin.ModelAdmin):
    list_display = (
        'tc_login_id', 'admin_id', 'name', 'email', 'mobile_no', 'status', 'login_time', 'logout_time'
    )

    search_fields = ('name', 'email', 'mobile_no')
    list_filter = ('status',)
    ordering = ('tc_login_id',)
    
    




@admin.register(TlLogin)
class TLLoginAdmin(admin.ModelAdmin):

    list_display = ('tl_login_id','admin_id','name','email','mobile_no','status','login_time','logout_time','image_preview','longitude','latitude')

    # Search bar fields
    search_fields = ('name', 'email', 'mobile_no')

    # Filters on right side
    list_filter = ('status',)

    # Show small circular image in admin list
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image"



@admin.register(GsLogin)
class GsLoginAdmin(admin.ModelAdmin):

    list_display = ('gs_login_id', 'admin_id', 'name', 'email', 'mobile_no', 'status', 'login_time', 'logout_time', 'image_preview', 'longitude', 'latitude')

    # readonly_fields = ('image_preview',)
    
    # Search bar fields
    search_fields = ('name', 'email', 'mobile_no')

    # Filters on right side
    list_filter = ('status',)
    

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 6px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image"
    
    
@admin.register(leave_request)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("admin_id","user_name","user_email","user_mobile","role","leave_status","submit_time")
    search_fields = ("user_id","user_role","admin_id","leave_status")
    list_filter = ("leave_status","submit_time","from_date","to_date","admin_id")
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'rating', 'category', 'nps_score', 'short_message', 'created_at', 'updated_at']
    list_filter = ['rating', 'category']
    search_fields = ['user_id', 'message']
    readonly_fields = ['user_id', 'created_at', 'updated_at']
    ordering = ['-created_at']
 
    def short_message(self, obj):
        return (obj.message[:60] + '...') if len(obj.message) > 60 else obj.message or '—'
    short_message.short_description = 'Message'
    


@admin.register(email_list)
class EmailListAdmin(admin.ModelAdmin):
    list_display = ("email_id", "email", "created_at")
    search_fields = ("email",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(contact_message)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    
@admin.register(MarqueeMessage)
class MarqueeMessageAdmin(admin.ModelAdmin):
    list_display = ("message", "is_active", "updated_at")
    list_editable = ("is_active",)
    fields = ("message", "is_active")

@admin.register(FCMToken)
class FCMTokenAdmin(admin.ModelAdmin):
    list_display = (
        'token_id',
        'user_id',
        'device_type',
        'device_name',
        'is_active',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'device_type',
        'is_active',
        'created_at',
    )

    search_fields = (
        'user_id__username',   # change if CreateUser uses different field
        'fcm_token',
        'device_name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)

    fieldsets = (
        ('User Information', {
            'fields': ('user_id',)
        }),
        ('Device Information', {
            'fields': (
                'fcm_token',
                'device_type',
                'device_name',
                'is_active',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )



