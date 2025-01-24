from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from user_app.models import users


# Create your models here.



class Category(models.Model):
    image = models.FileField(null=True, upload_to='uploads/')
    name = models.CharField(null=True, max_length=200)
    description = models.CharField(null=True, max_length=300)

    def __str__(self):
        return self.name


class Excavator(models.Model):
    image = models.FileField(null=True, upload_to='uploads/')
    excavator_name = models.CharField(null=True, max_length=200)
    price = models.IntegerField(null=True)
    company_name = models.CharField(null=True, max_length=200)
    location = models.CharField(null=True, max_length=200)
    Availability = models.CharField(
        max_length=50,
        choices=[('Available for rent', 'Available for rent'), ('Not Available', 'Not Available')],
        default='Available for rent'  # Correct default to a valid choice
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='excavators',null=True)
    payment_mode = models.CharField(
        max_length=20,
        choices=[('Select','Select'),('Hourly', 'Hourly'), ('Per Day', 'Per Day')],
        default='null'
    )   
    
    

class contact(models.Model):    
    full_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True) 
    phone = models.IntegerField(null=True) 
    is_enquired = models.BooleanField(default=False)

    quantity = models.PositiveIntegerField( blank=True,null=True)
    excavator_model = models.CharField(max_length=100,null=True)
    EXCAVATOR_TYPE_CHOICES =[
        ('mini', 'Mini Excavator'),
        ('crawler', 'Crawler Excavator'),
        ('wheeled', 'Wheeled Excavator'),
        ('dragline', 'Dragline Excavator'),
        ('suction', 'Suction Excavator'),
        ('long_reach', 'Long Reach Excavator'),
        ('hydraulic', 'Hydraulic Excavator'),
        ('skid_steer', 'Skid-Steer Excavator'),
    ]
    excavator_type = models.CharField(max_length=10, choices=EXCAVATOR_TYPE_CHOICES,default= " ")
    rental_days = models.PositiveIntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    location = models.CharField(null=True, max_length=200)
    operator_required = models.BooleanField(default=False)  
    # total_cost = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # e.g., $1,500.00
    payment_method = models.CharField(max_length=50,choices=[('Credit Card', 'Credit Card'),('Bank Transfer', 'Bank Transfer'),('Cash', 'Cash'),],default='Cash')
    requirement = models.CharField(max_length=300, null=True)
    id_proof = models.FileField(upload_to='uploads/id_proofs/', null=True) 
    created_at = models.DateTimeField(auto_now_add=True,null=True)  
    updated_at = models.DateTimeField(auto_now=True )      
    user = models.ForeignKey(users, on_delete=models.CASCADE,null=True)
    excavator = models.ForeignKey(Excavator, on_delete=models.CASCADE,null=True)


class Safety(models.Model):
    safety_title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=200,null=True)
    precaution = models.TextField(null=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(users, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.safety_title


    






