from django.db import models

# Create your models here.
class admin_user_model(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username}"
    



class CreateUser(models.Model):
    ROLE_CHOICES = [
        ('telecaller', 'Telecaller'),
        ('teamlead', 'Team Lead'),
        ('groundstaff', 'Ground Staff'),
    ]
    admin_id = models.ForeignKey(admin_user_model, on_delete=models.CASCADE,default=1)
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    username = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


class Create_task(models.Model):
    # task id 
    task_id = models.AutoField(primary_key = True)
    admin_id = models.ForeignKey(admin_user_model, on_delete = models.CASCADE)
    
    # category section
    category = models.CharField(max_length = 100, null=True, blank=True)
    
    # aggrement information
    aggrement_id = models.CharField(max_length = 50)
    customer_name = models.CharField(max_length = 100)
    product_type = models.CharField(max_length = 50)
    tc_name = models.CharField(max_length = 100)
    branch = models.CharField(max_length = 100)
    count_of_cases = models.CharField(max_length = 20)
    old_or_new = models.CharField(max_length = 20)
    bucket = models.CharField(max_length = 15)
    mode = models.CharField(max_length = 30)
    npa_status = models.CharField(max_length = 50)
    
    # financial details
    pos_amount = models.CharField(max_length = 50)
    total_charges = models.CharField(max_length = 30)
    bcc_pending = models.CharField(max_length = 20)
    penal_pending = models.CharField(max_length = 20)
    emi_amount = models.CharField(max_length = 30)
    emi_due_amount = models.CharField(max_length = 30)
    recipt_amount = models.CharField(max_length = 30)
    recipt_date = models.CharField(max_length = 20)
    disbursement_amount = models.CharField(max_length = 30)
    loan_amount = models.CharField(max_length = 30)
    disbursement_date = models.CharField(max_length = 20)
    emi_start_date = models.CharField(max_length = 20)
    emi_end_date = models.CharField(max_length = 20)
    emi_cycle_date = models.CharField(max_length = 20)
    
    # vehicle details 
    make = models.CharField(max_length = 100)
    manufacturer_description = models.CharField(max_length = 500, null=True, blank=True)
    registration_number = models.CharField(max_length = 30, null=True, blank=True)
    vehicle_age = models.CharField(max_length = 20, null=True, blank=True)
    
    # customer details 
    employer = models.CharField(max_length = 100, null=True, blank=True)
    father_name = models.CharField(max_length = 50)
    fe_name = models.CharField(max_length = 50)
    fe_mobile_number = models.CharField(max_length = 10)
    customer_mobile_number = models.CharField(max_length = 10)
    pin_code = models.CharField(max_length = 6)
    customer_address = models.CharField(max_length = 500)
    customer_office_address = models.CharField(max_length = 500)
    reference_details = models.CharField(max_length = 500)
    
    # collection details
    collection_manager_name = models.CharField(max_length = 100)
    finance_company_name = models.CharField(max_length = 200)


class task_update(models.Model):
    task_update_id = models.AutoField(primary_key = True)
    
    updated_by = models.CharField(max_length = 100, null = True, blank = True)
    
    #data form admin table
    admin_id = models.ForeignKey(admin_user_model, on_delete = models.CASCADE)
    
    #data from create task table
    task_id = models.ForeignKey(Create_task, on_delete = models.CASCADE)
    agreement_id = models.CharField(max_length = 50)
    
    # contact information
    code = models.CharField(max_length = 10)
    new_mobile_number = models.CharField(max_length = 15)
    
    # projection details 
    projection = models.CharField(max_length = 100)
    promise_date = models.DateTimeField(max_length = 20)
    promise_amount = models.CharField(max_length = 30)
    
    # remark 
    customer_remark = models.CharField(max_length = 500)
    reference_remark = models.CharField(max_length = 500)
    
    # visit details
    need_group_visit = models.CharField(max_length = 10)
    visit_projection = models.CharField(max_length = 100)
    visit_status = models.CharField(max_length = 20)
    
    # customer & vehicle details
    customer_available = models.CharField(max_length = 20)
    vehicle_available = models.CharField(max_length = 10)
    third_party_status = models.CharField(max_length = 10)
    third_party_details = models.CharField(max_length = 500)
    
    # location & status
    new_update_address = models.CharField(max_length = 500)
    location_image = models.ImageField(upload_to='location_image/', null=True, blank=True)
    location_status = models.CharField(max_length = 20)
    
    # payment details
    payment_info = models.CharField(max_length = 500)
    payment_mode = models.CharField(max_length = 50)
    payment_amount = models.CharField(max_length = 30)
    payment_date = models.DateTimeField(max_length = 20)
    
    # update 
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    
    
    
    
    


class TcLogin(models.Model):
    tc_login_id = models.AutoField(primary_key=True)

    admin_id = models.CharField(max_length=20) 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)

    status = models.CharField(max_length=20)  
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"





class TlLogin(models.Model):
    tl_login_id = models.AutoField(primary_key=True)   # Primary Key
    admin_id = models.CharField(max_length=50)         # Admin ID
    name = models.CharField(max_length=100)            # Name
    email = models.EmailField(unique=True)             # Email (unique)
    mobile_no = models.CharField(max_length=15, unique=True)  # Mobile (unique)
    
    status = models.CharField(max_length=20)           # Active / Inactive
    
    login_time = models.DateTimeField(null=True, blank=True)   # Login Time
    logout_time = models.DateTimeField(null=True, blank=True)  # Logout Time

    image = models.ImageField(upload_to='tl_images/', null=True, blank=True)  # Profile Image
    
    longitude = models.FloatField(null=True, blank=True)   # GPS Longitude
    latitude = models.FloatField(null=True, blank=True)    # GPS Latitude

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    


class GsLogin(models.Model):
    gs_login_id = models.AutoField(primary_key=True)
    admin_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=20)  # Active / Inactive
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    image = models.ImageField(upload_to='gs_login/', null=True, blank=True)

    longitude = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

