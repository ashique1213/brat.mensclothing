from django.db import models

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Tshirt', 'T-shirt'),
        ('Shirt', 'Shirt'),
        ('Jeans', 'Jeans'),
        ('Pants', 'Pants'),
    ]

    category_id = models.AutoField(primary_key=True)  
    brand_name = models.CharField(max_length=255)    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    category_unit = models.CharField(max_length=50)   
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True)       

    def __str__(self):
        return self.category 