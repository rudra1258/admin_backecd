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
        return f"{self.admin_id} - {self.username}"
    



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
    task_id = models.AutoField(primary_key = True)
    admin_id = models.ForeignKey(admin_user_model, on_delete = models.CASCADE)
    adreement_id = models.CharField(max_length = 50)
    customer_name = models.CharField(max_length = 100)
    product_type = models.CharField(max_length = 50)
    tc_name = models.CharField(max_length = 100)
    branch = models.CharField(max_length = 100)
    count_of_cases = models.CharField(max_length = 20)
    old_or_new = models.CharField(max_length = 20)
    bucket = models.CharField(max_length = 15)
    mode = models.CharField(max_length = 30)
    npa_status = models.CharField(max_length = 50)
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
    make = models.CharField(max_length = 100)
    father_name = models.CharField(max_length = 50)
    fe_name = models.CharField(max_length = 50)
    fe_mobile_number = models.CharField(max_length = 10)
    customer_mobile_number = models.CharField(max_length = 10)
    pin_code = models.CharField(max_length = 6)
    customer_address = models.CharField(max_length = 500)
    customer_office_address = models.CharField(max_length = 500)
    reference_details = models.CharField(max_length = 500)
    collection_manager_name = models.CharField(max_length = 100)
    finance_company_name = models.CharField(max_length = 200)

