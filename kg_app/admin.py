from django.contrib import admin
from .models import *
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
