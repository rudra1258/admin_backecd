from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

admin.site.site_header = "MK Association Superadmin"
admin.site.site_title = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Dashboard"


admin.site.register(admin_user_model)

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
