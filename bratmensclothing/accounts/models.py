from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)  
    username = models.CharField(max_length=100) 
    email = models.EmailField(max_length=255, unique=True)  
    phone_number = models.CharField(max_length=15,null=True) 
    profile = models.ImageField(upload_to='profiles/', null=True, blank=True) 
    address = models.TextField(null=True) 
    password = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True) 
    isBlocked = models.BooleanField(default=False) 

    def __str__(self):
        return self.username