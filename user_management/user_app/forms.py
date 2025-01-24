from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password
from django.forms import formset_factory
from django.forms import modelformset_factory

#Register Form
class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput,label='Confirm Password*')
    place = forms.CharField(max_length=100,label='Place*')
    image = forms.ImageField(required=False,label='Profile Photo*')

    class Meta:
        model = users
        fields = ['username', 'email', 'place', 'phone', 'image', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'phone' : forms.NumberInput()
            
        }
        help_texts = {'username': None}
        labels = {
            'username': 'User Name ',
            'image': 'Profile Photo ',
            'email' : 'Email ',
            'phone' : 'Phone Number ',
            'password' : 'Password ',
            'confirm_password' : 'Confirm Password ',
            'place' : 'Place '

        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        PasswordChangeForm.validate_password(password)
        return password
        


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter again.")

        return cleaned_data


#Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = users
        fields = [ 'email', 'phone', 'place','image']
        widgets = {         
            "email" : forms.EmailInput,
            "phone" : forms.NumberInput,
            "place" : forms.TextInput
           }
        help_texts={
            "username":None
        }


#Login Form
class LoginForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['username', 'password']
        widgets = {
            "username" : forms.TextInput,
            "password": forms.PasswordInput(attrs={"class":"form-group bg-transparent pswd"}),
           }
        help_texts = {'username':None}


#Forgot Password Form
class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,  
        widget=forms.TextInput(attrs={'class': 'form-group'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


#PasswordChange Form
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm New Password"
    )
    
    
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError("The password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("The password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
             raise ValidationError("The password must contain at least one letter.")
        
        # Add custom validation logic here
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        self.validate_password(new_password1)
        return new_password1
       
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")

        # Ensure the new password is different from the old password
        if old_password and new_password1 and old_password == new_password1:
            self.add_error('new_password1', "The new password must be different from the old password.")
        return cleaned_data

#User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['username', 'email', 'phone', 'place','image']
        help_texts = {'username':None}

# Driver Form
class DriverForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label="Confirm Password"
    )
    EXCAVATOR_LICENSE_CHOICES = [
        ('h_class', 'Heavy Equipment Operator License (H-Class)'),
        ('construction_cert', 'Construction Equipment Operator Certification'),
        ('cdl', 'Commercial Driver’s License (CDL)'),
        ('specialized_excavator', 'Specialized Excavator License'),
        ('permanent driving license', 'Permanent driving license')
    ]
    license_category = forms.ChoiceField(
        choices=EXCAVATOR_LICENSE_CHOICES,
        required=True,
        label="License Category",
        widget=forms.Select()
    )

    class Meta:
        model = users
        fields = [
            'username', 'email', 'phone', 'experience', 'specialization', 'Location','district', 'image',
            'password', 'confirm_password', 'license_number', 'certificates', 'license_category',
            'payment_mode', 'payment_amount'
        ]
        widgets = {
            'email': forms.EmailInput(),
            'phone': forms.NumberInput(attrs={}),
            'experience': forms.TextInput(),
            'specialization': forms.TextInput(),
            'license_number': forms.TextInput(),
            'certificates': forms.ClearableFileInput(),
            'payment_mode': forms.Select(),
            'payment_amount': forms.NumberInput(),
        }
        labels = {
            'username': 'Driver Name',
            'image': 'Driver Photo'
        }
        help_texts = {
            'username': None
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match. Please enter again.")
        return cleaned_data


class DriverFilterForm(forms.Form):
    LOCATION_CHOICES = [
        ('', 'All Locations'),
        ('Kasaragod','Kasaragod'),
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
        ('Thiruvananthapuram','Thiruvananthapuram')
    ]
    district = forms.ChoiceField(choices=LOCATION_CHOICES, required=False)

    EXCAVATOR_LICENSE_CHOICES = [
        ('Heavy Equipment Operator License (H-Class)', 'Heavy Equipment Operator License (H-Class)'),
        ('Construction Equipment Operator Certification', 'Construction Equipment Operator Certification'),
        ('Commercial Driver’s License (CDL)', 'Commercial Driver’s License (CDL)'),
        ('Specialized Excavator License', 'Specialized Excavator License'),
        ('Permanent driving license', 'Permanent driving license')
    ]
    license_category = forms.ChoiceField(choices=EXCAVATOR_LICENSE_CHOICES, required=False)


# Mechanic Form

class MechanicForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
     
    class Meta:
        model = users
        fields = ['username', 'email', 'phone', 'place', 'district', 'area_of_expertise', 'services', 'experience', 'certificates', 'image', 'password']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'phone': forms.NumberInput(),
            'place': forms.TextInput(),
            'district': forms.TextInput(),
            'area_of_expertise': forms.TextInput(attrs={'class': 'text', 'placeholder': 'Hydraulic System, engine repair'}),
            'services': forms.TextInput(attrs={'class': 'text', 'placeholder': 'Enter the Services'}),
            'experience': forms.TextInput(),
            'certificates': forms.ClearableFileInput(),
            'image': forms.ClearableFileInput(),
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Full Name',
            'image': 'Profile Photo',
            'experience': 'Year of Experience',
            'services': 'Services Offered'
        }
        help_texts = {'username': None}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter again.")
        return cleaned_data

class SafetyForm(forms.Form):
    safety_precaution = forms.CharField(widget=forms.TextInput(attrs={'class': 'safety-input'}))

SafetyFormset = formset_factory(SafetyForm, extra=2)
# class SafetyForm(forms.Form):
#     safety_precaution = forms.CharField(max_length=255, required=True, label="Safety Precaution", widget=forms.TextInput)
# SafetyFormset = formset_factory(SafetyForm, extra=1, max_num=3)


    

class MechanicFilterForm(forms.Form):
    LOCATION_CHOICES = [
        ('', 'All Locations'),
        ('Kasaragod','Kasaragod'),
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
        ('Thiruvananthapuram','Thiruvananthapuram')
    ]                                          
    
    EXPERTISE_CHOICES = [
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
        ('Cab and Operator Comfort Repairs', 'Cab and Operator Comfort Repairs')
    ]
    
    district = forms.ChoiceField(choices=LOCATION_CHOICES, required=False)
    area_of_expertise = forms.ChoiceField(choices=EXPERTISE_CHOICES, required=False)
    
class book_form(forms.ModelForm):
    equipment_type = forms.ChoiceField(
        choices=[('mini_excavator', 'Mini Excavator'), ('standard_excavator', 'Standard Excavator')],
        widget=forms.Select(attrs={'class': 'text'}),
        label="Equipment Type"
    )
    BOOKING_CHOICES = [
        ('now', 'Now'),
        ('schedule_later', 'Schedule Later'),
    ]
    booking_type = forms.ChoiceField(
        choices=BOOKING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio'}),
        label="Booking Type"
    )

    class Meta:
        model = Booking
        fields = ['booking_type','location','equipment_type','booking_time', 'booking_date', 'to_date','message']
        widgets = {
            'booking_time': forms.TimeInput(attrs={'class': 'text', 'type': 'time'}),
                'booking_date': forms.DateInput(attrs={'class': 'text', 'type': 'date'}),
            'message': forms.Textarea(attrs={
                # 'class': 'text',
                'placeholder': 'Add the specific purpose',
                'rows': 4
            }),
            'location': forms.TextInput(attrs={
                # 'class': 'text', 
                  # Use a unique and descriptive ID
                'placeholder': 'Add your place'
            }),
            'to_date': forms.DateInput(attrs={'class': 'text', 'type': 'date'}),
        }

        labels= {
            'booking_type': 'When do you want to book?',
            'booking_date': 'From Date',
            'to_date': 'To Date',
            'message': 'Message/Instructions'

        }


class MechanicServiceForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['services', 'description','photoid']
        labels={
            'photoid': 'Service Photo'
        }
        widgets = {
            'description' : forms.Textarea(attrs={'style':'width','rows': 4})
        }

class Mech_book_form(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [ 'excavator_make_model',
            'serial_number',
            'operating_hours',
            'last_service_date',
            'service_type',
            'issue_description',
            'priority_level',
            'service_location',
            'preferred_date',
            'preferred_time_slot',
            ]
        
        widgets = {
            'last_service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'preferred_time_slot': forms.Select(choices=[
                ('morning', 'Morning'),
                ('afternoon', 'Afternoon'),
                ('evening', 'Evening'),
                
            ],
            attrs={'class': 'form-control'}),
            'priority_level': forms.RadioSelect(choices=[
                ('standard', 'Standard'),
                ('urgent', 'Urgent'),
                ('emergency', 'Emergency'),
            ],attrs={'class': 'form-control','type': 'date'}),
            'issue_description': forms.Textarea(attrs={'class': 'form-control','type': 'date','rows': 4}),
            'service_location': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type' : forms.Select(choices=[
                ('routine_maintenance', 'Routine Maintenance'),
                ('hydraulic_repair', 'Hydraulic System Repair'),
                ('engine_service', 'Engine Service'),
                ('undercarriage_repair', 'Undercarriage Repair'),
                ('electrical_diagnostics', 'Electrical Diagnostics'),
                ('attachment_installation', 'Attachment Installation'),
            ],
            attrs={'class': 'form-control'})
        }


        

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation logic here if needed
        return cleaned_data
    
    

class spareForm(forms.ModelForm):
    class Meta:
        model = Spares
        fields = ['part_name','supplier','type','price','image','description','availability','material','warranty','modal_name','quantity']    


class SpareUpdateForm(forms.ModelForm):
    class Meta:
        model = Spares
        fields = ['part_name','supplier','price','image','type','description','availability','material','warranty','modal_name','quantity']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'required': False}),
        }


class SpareContacts(forms.ModelForm):
    excavator_type = forms.ChoiceField(
    label="Excavator Type",
    choices=[
        ('mini', 'Mini Excavator'),
        ('crawler', 'Crawler Excavator'),
        ('wheeled', 'Wheeled Excavator'),
        ('dragline', 'Dragline Excavator'),
        ('suction', 'Suction Excavator'),
        ('long_reach', 'Long Reach Excavator'),
        ('hydraulic', 'Hydraulic Excavator'),
        ('skid_steer', 'Skid-Steer Excavator'),
    ]

    )
    class Meta:
        model = SpareContact
        fields = ['email','phone','excavator_type','quantity','requirement']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact number'}),
            'excavator_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'requirement': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Specify your requirements', 'rows': 4}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1, 
                'max': 5, 
                'placeholder': 'Rate out of 5'
            }),
        }
        labels = {
            'rating': 'Rate the Driver',
        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields =['name','email','phone','message']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address', 'city', 'state', 'pincode']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Pincode'}),
        }

