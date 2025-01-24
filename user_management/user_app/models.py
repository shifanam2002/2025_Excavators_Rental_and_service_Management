from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime


# Create your models here.
class users(AbstractUser):
    usertype = models.IntegerField(default=0)
    phone = models.IntegerField(default='')
    name = models.CharField(max_length=200, default='', null=True)
    place = models.CharField(max_length=200,  default='', null=True)
    district = models.CharField(max_length=200, 
                                choices= [('Kasaragod','Kasaragod'),
                                          ('Kannur','Kannur'),
                                          ('Wayanad','Wayanad'),
                                          ('Kozhikode','Kozhikode'),
                                          ('Malappuram','Malappuram'),
                                          ('Palakkad','Palakkad'),
                                          ('Thrissur','Thrissur'),
                                          ('Ernakulam','Ernakulam'),
                                          ('Idukki','Idukki'),
                                          ('Kottayam','Kottayam'),
                                          ('Alappuzha','Alappuzha'),
                                          ('Pathanamthitta','Pathanamthitta'),
                                          ('Kollam','Kollam'),
                                          ('Thiruvananthapuram','Thiruvananthapuram')],
                                null=True)
    image = models.FileField(null=True,upload_to='uploads/')
    license_number = models.CharField(max_length=20, default='')
    certificates = models.FileField(null=True, blank=True, upload_to='uploads/')
    area_of_expertise = models.CharField(max_length=100, default='', blank=True,choices=[
                ('Engine Repair and Maintenance', 'Engine Repair and Maintenance'),
                ('Hydraulic System Maintenance', 'Hydraulic System Maintenance'),
                ('Cylinder Repair and Replacement', 'Cylinder Repair and Replacement'),
                ('Undercarriage Repair', 'Undercarriage Repair'),
                ('Welding and Fabrication Services', 'Welding and Fabrication Services'),
                ('Electrical System Repairs', 'Electrical System Repairs'),
                ('Attachment Servicing', 'Attachment Servicing'),
                ('Cooling System Repairs', 'Cooling System Repairs'),
                ('Brake and Steering System Repairs', 'Brake and Steering System Repairs'),
                ('Preventative Maintenance Services', 'Preventative Maintenance Services'),
                ('Track and Tread Replacement', 'Track and Tread Replacement'),
                ('Cab and Operator Comfort Repairs', 'Cab and Operator Comfort Repairs')])
    is_approved = models.BooleanField(default=False)
    approval_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    experience = models.CharField(max_length=200,null =True)
    specialization = models.CharField(max_length=200, null =True)
    Address = models.CharField(null=True,max_length=200)
    DOB= models.DateField(null=True)
    services= models.CharField(max_length=100, null=True)
    rate = models.IntegerField(null=True,default=0)
    area = models.CharField(max_length=50, default=0)
    hours = models.TimeField(null=True)
    availability = models.CharField(null=True,max_length=15)
    photoid=  models.FileField(null=True,upload_to='uploads/')
    description = models.CharField(null=True,max_length=550)
    service_name = models.CharField(null=True,max_length=100)
    payment_mode = models.CharField(
        max_length=20,
        choices=[('Select','Select'),('Hourly', 'Hourly'), ('Per Day', 'Per Day')],
        default='null'
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    EXCAVATOR_LICENSE_CHOICES = [
        ('Heavy Equipment Operator License (H-Class)', 'Heavy Equipment Operator License (H-Class)'),
        ('Construction Equipment Operator Certification', 'Construction Equipment Operator Certification'),
        ('Commercial Driver’s License (CDL)', 'Commercial Driver’s License (CDL)'),
        ('Specialized Excavator License', 'Specialized Excavator License'),
        ('Permanent driving license', 'Permanent driving license')
    ]
    license_category = models.CharField(
        max_length=50,
        choices=EXCAVATOR_LICENSE_CHOICES,
        default='h_class'
    )
    Location = models.CharField(null=True,max_length=100)
    longitude=models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    # safety_certificate = models.FileField(null=True, blank=True, upload_to='uploads/')
    safety_precautions = models.TextField(blank=True, null=True)  

    

class Booking(models.Model):
    user_id = models.ForeignKey(users,on_delete=models.CASCADE,null=True)
    driver_id = models.ForeignKey(users,on_delete=models.CASCADE,null=True,related_name='+')
    mech_id = models.ForeignKey(users,on_delete=models.CASCADE,null=True,related_name='+')
    booking_time = models.TimeField(max_length=255,null=True)
    booking_date = models.DateField(max_length=255,null=True)
    
    to_date =models.DateField(max_length=200,null=True)
    approval_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    service_status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Driver Arrived", "Driver Arrived"),
            ("Service Started", "Service Started"),
            ("Completed", "Completed"),
        ],
        default="Pending"
    )
    equipment_type = models.CharField(
        choices=[
            ('mini_excavator', 'Mini Excavator'), 
            ('standard_excavator', 'Standard Excavator')
        ],
        default='null',
        max_length=50
    )
    BOOKING_CHOICES = [
        ('now', 'Now'),
        ('schedule_later', 'Schedule Later'),
    ]
    booking_type = models.CharField(
        choices=BOOKING_CHOICES,
        default='Schedule Later',
        max_length=50
    )
    location = models.CharField(max_length=255,null=True)
    message= models.CharField(max_length=300,null=True)
    
    excavator_make_model = models.CharField(max_length=100, default=" ")
    serial_number = models.CharField(max_length=50, blank=True, null=True,default=" ")
    operating_hours = models.PositiveIntegerField(blank=True, null=True)
    last_service_date = models.DateField(blank=True, null=True, default=None)
    service_type = models.CharField(
        max_length=50,
        choices=[
            ('routine_maintenance', 'Routine Maintenance'),
            ('hydraulic_repair', 'Hydraulic System Repair'),
            ('engine_service', 'Engine Service'),
            ('undercarriage_repair', 'Undercarriage Repair'),
            ('electrical_diagnostics', 'Electrical Diagnostics'),
            ('attachment_installation', 'Attachment Installation'),
        ],
        default='hydraulic_repair'
    )
    issue_description = models.TextField(blank=True)
    priority_level = models.CharField(
        max_length=15,
        choices=[
            ('standard', 'Standard'),
            ('urgent', 'Urgent'),
            ('emergency', 'Emergency'),
        ],
        default= 'standard'
    )
    service_location = models.TextField(default=" ")
    accessibility_info = models.TextField(blank=True, null=True)
    preferred_date = models.DateField(blank=True, null=True,default=None)
    preferred_time_slot = models.CharField(
        max_length=10,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
        ],
        default='evening'
    )
    created_at = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(null=True, blank=True, default=None)  


    
class Spares(models.Model):
    CATEGORIES_CHOICES=[
        ('Engine','Engine Component'),
        ('Hydraulics','Hydraulics'),
        ('Electrical','Electrical Part'),
        ('undercarriage','Undercarriage Part'),
        ('Attachment',' Attachment'),
        ('Drive Components','Drive Components'),
        ('Braking System','Braking System'),
        ('fuel system','Fuel system'),
        ('Excavator Bucket','Excavator Bucket')
    ]
    part_name = models.CharField(max_length=100, default=" ")
    supplier = models.CharField(max_length=100, default=" ")
    price = models.IntegerField(blank=True, null=True)
    image = models.ImageField(null=True,upload_to='uploads/')
    type = models.CharField(max_length=100,choices=CATEGORIES_CHOICES,default='select type') 
    description = models.CharField(max_length=300,null=True)
    material = models.CharField(max_length=200,
                                choices=[('metals','Metals'),
                                         ('Polymers','Polymers'),
                                         ('Synthetic Polymers','Synthetic Polymers'),
                                         ('Ceramics','Ceramics')],
                                default='metals')
    availability = models.CharField(max_length=50,
                                    choices=[('In Stock','In Stock'),
                                             ('Out Stock','Out of Stock')],
                                    default='')
    modal_name = models.CharField(max_length=20,null=True)
    warranty = models.IntegerField(null=True)
    quantity = models.PositiveIntegerField( blank=True,null=True)



class SpareContact(models.Model):
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

    excavator_type = models.CharField(max_length=10, choices=EXCAVATOR_TYPE_CHOICES,default= "Mini Excavator")
    quantity = models.PositiveIntegerField( blank=True,null=True)
    requirement = models.CharField(max_length=300, null=True)
    email = models.EmailField(null=True) 
    phone = models.IntegerField(null=True)
    spares =  models.ForeignKey(Spares, on_delete=models.CASCADE, null=True)




class Contact(models.Model):
    name = models.CharField(max_length=300, null=True)
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    phone =models.IntegerField(null=True)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spare = models.ForeignKey('Spares', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', null=True)  
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}, {self.city}"