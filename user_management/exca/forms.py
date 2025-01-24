from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
from user_app.forms import spareForm

class addexcavatorForm(forms.ModelForm):
    Availability = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'text'}),
        choices=[('Available for rent', 'Available for rent'),('Not Available', 'Not Available')],
    )
    
    class Meta:
        model =  Excavator
        fields = ['image','excavator_name','payment_mode', 'price','company_name','location','Availability','category']
       
    
        

class addcategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['image','name','description']
        labels = {
            'name ' : 'Excavator category name'
        }
        widget = {
            'image': forms.FileInput(attrs={'class':'form-group'}),
            'name': forms.TextInput(attrs={'class':'form-group'}),
            'description': forms.TextInput(attrs={'class':'form-group'}),

        }

class contactForm(forms.ModelForm):
    weight = forms.ChoiceField(
        choices=[('38700 Kg','38700 Kg'),
                 ('53100 Kg','53100 Kg'),
                 ('46400 Kg','46400 Kg'),
                 ('63900 Kg','63900 Kg'),
                 ('57400 Kg','57400 Kg')],
        widget=forms.Select(attrs={'placeholder': 'Select a value'})
    )

    # payment_method = forms.ChoiceField(
    #     choices = [('Credit Card', 'Credit Card'),
    #         ('Bank Transfer', 'Bank Transfer'),
    #         ('Cash', 'Cash')]
    # )
    excavator_type =  forms.ChoiceField(
        choices=[('mini', 'Mini Excavator'),
        ('crawler', 'Crawler Excavator'),
        ('wheeled', 'Wheeled Excavator'),
        ('dragline', 'Dragline Excavator'),
        ('suction', 'Suction Excavator'),
        ('long_reach', 'Long Reach Excavator'),
        ('hydraulic', 'Hydraulic Excavator'),
        ('skid_steer', 'Skid-Steer Excavator'),]
    )


    class Meta:
        model = contact
        fields = ['full_name', 'email','phone','weight','requirement','excavator_model','excavator_type',
                  'rental_days','start_date','end_date','location','operator_required','id_proof'
                  ]
        labels = {
            'weight' : 'Max Operating Weight', 
            'requirement' : 'Requirement Details'
        }
        widgets = {
            'requirement': forms.Textarea(attrs={
                'class': 'text',
                'placeholder': 'Additional Details about your requirements',
                'rows': 4
        }),
            'phone' : forms.NumberInput(attrs = {'placeholder':'Enter Contact number'}),
            'email' : forms.EmailInput(attrs = {'placeholder':'Enter your email address'}),
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date' : forms.DateInput(attrs={'type':'date'}),
            'id_proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),


        }



class ExcavatorSearchForm(forms.Form):
    model = forms.CharField(max_length=100, required=False, label="Model")
    excavator_type = forms.ChoiceField(
        choices=[('', 'All')] + contact.EXCAVATOR_TYPE_CHOICES, 
        required=False, 
        label="Type"
    )
    min_weight = forms.IntegerField(required=False, label="Min Weight (Kg)")
    max_weight = forms.IntegerField(required=False, label="Max Weight (Kg)")


class SafetyForm(forms.ModelForm):
    class Meta:
        model = Safety
        fields = ['safety_title', 'created_by']