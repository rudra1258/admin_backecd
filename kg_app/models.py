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
    password = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
