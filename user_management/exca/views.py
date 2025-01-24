from pyexpat.errors import messages
from django.shortcuts import render
from . models import * 
from . forms import *
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from user_app.forms import spareForm
from geopy.distance import geodesic
import geocoder
from django.forms import formset_factory






# class MiniExcavatorView(ListView):
#     model = Excavator
#     template_name = 'mini_exca.html'
#     context_object_name = 'excavators'  # This sets the name used in the template

#     def get_queryset(self):
#         return Excavator.objects.filter(Availability = 'Available for rent')


def mini_exca(request, id):   
    category_instance = get_object_or_404(Category, id=id)
    excavators = Excavator.objects.filter(category=category_instance)   

    if request.method == "POST":
        print(request.POST)  # Debugging: Print POST data
        form = contactForm(request.POST, request.FILES)  
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            # Retrieve the excavator_id from POST data
            excavator_id = request.POST.get('excavator.id')
            print(excavator_id, 'excavator_id')  # Debugging: Print excavator_id

            if excavator_id:
                try:
                    excavator = Excavator.objects.get(id=excavator_id)
                    booking.excavator = excavator
                except Excavator.DoesNotExist:
                    print("Invalid Excavator ID")
            else:
                print("Excavator ID not provided")
            
            booking.save() 
            return redirect('mini_exca', id=id)
        else:
            print(form.errors)
    else:
        form = contactForm()

    return render(request, 'mini_exca.html', {
        'category': category_instance,
        'excavators': excavators,
        'form': form,
      
    })


def add_excavator(request):
    if request.method == 'POST':
        if 'add_excavator' in request.POST:  # Check which form was submitted
            exca_form = addexcavatorForm(request.POST, request.FILES)
            if exca_form.is_valid():
                exca_form.save()
                return redirect('add_excavator')
        elif 'add_category' in request.POST:  # Check which form was submitted
            category_form = addcategoryForm(request.POST, request.FILES)
            if category_form.is_valid():
                # category = category_form.save(commit=False)
                category_form.save()
                return redirect('add_excavator')
    else:
        exca_form = addexcavatorForm()
        category_form = addcategoryForm()

    return render(request, 'add_excavator.html', {
        'exca_form': exca_form,
        'category_form': category_form,
    })

def view_cate(request):
    categories = Category.objects.all()
    return render(request, 'view_cate.html',{'categories':categories})

def view_exca(request):
    categories = Excavator.objects.all()
    return render(request, 'view_exca.html',{'categories':categories})    

def update_cate_view(request, id):
    print(Category.id)
    category = get_object_or_404(Category, id=id)  # Fetch the category to update
    
    if request.method == 'POST':
        form = addcategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_cate')  
    else:
        form = addcategoryForm(instance=category)
    
    return render(request, 'update_cate.html', {'form': form})

def update_exca_view(request, id):
    print(Excavator.id)
    category = get_object_or_404(Excavator, id=id)  # Fetch the category to update
    
    if request.method == 'POST':
        form = addexcavatorForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_exca')  
    else:
        form = addexcavatorForm(instance=category)
    
    return render(request, 'update_exca.html', {'form': form})

def cate_delete(request,delete_id):
    instance= get_object_or_404(Category,id=delete_id) 
    instance.delete()
    return redirect('view_cate')


def index(request):
    categories=Category.objects.all()
    print(categories)
    return render(request,'index.html',{'categories': categories})


def category_view(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    excavators = category_obj.excavators.all()  # Get all excavators in this category

    form = contactForm()
    return render(request, 'mini_exca.html', {
        'category': category_obj, 
        'excavators': excavators,
        'form' : form})

def contact_supplier(request,id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mini_exca',id=id)  
        else:
            print(form.errors)
    else:
        form = contactForm()
        print(form.errors)
    return render(request, 'mini_exca.html', {'form': form, 'category': category})

class book_view(ListView):
    model = contact
    template_name = 'book_request.html'
    context_object_name = 'datas'

    def get_queryset(self):
        return contact.objects.select_related('excavator').all()


def safety(request):
    return render(request,'safety.html')

def update_enquiry(request, id):
    if request.method == "POST":
        enquiry = get_object_or_404(contact, id=id)
        enquiry.is_enquired = True
        enquiry.save()
    return redirect('book_request')



def search(request):
    search_query = request.GET.get('search', '')
    
    # Split the search_query by commas and strip whitespace
    criteria = [item.strip() for item in search_query.split(',')]

    # Start with all excavators
    excavators = Excavator.objects.all()

    if criteria:
        # Initialize query filters
        query_filters = Q()
        
        for criterion in criteria:
            # Check if the criterion is a digit (indicating a price)
            if criterion.isdigit():
                query_filters |= Q(price__gte=float(criterion))
            else:
                # Add filters for excavator_name, location, and category
                query_filters |= (
                    Q(excavator_name__icontains=criterion) |
                    Q(location__icontains=criterion) 
                    # Q(category__icontains=criterion)
                )

        # Apply filters to the excavators queryset
        excavators = excavators.filter(query_filters)

    # Render your template with the filtered results
    return render(request, 'index.html', {'excavators': excavators,'search_query': search_query})




def vw_rentals(request):
    confirmed_bookings = contact.objects.filter(user=request.user)
    rental_booking= Excavator.objects.all()
    return render(request, 'vw_rentals.html', {'rentals': confirmed_bookings,'rental_booking':rental_booking})



# def add_safety(request):
#     SafetyFormSet = formset_factory(SafetyForm, extra=3)  

#     if request.method == 'POST':
#         formset = SafetyFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data:  
#                     form.save()
#             messages.success(request, 'Safety information added successfully', extra_tags='suc')
#             return redirect('index')
#     else:
#         formset = SafetyFormSet()

#     return render(request, 'add_safety.html', {'formset': formset})

def add_safety(request):
    if request.method == 'POST':
        safety_title = request.POST.get('safety_title')
        description = request.POST.get('description')
        precautions = request.POST.getlist('safety_precaution')  # Get all precautions as a list
        print(f"Title: {safety_title}")


        # Save precautions
        for precaution in precautions:
            if precaution.strip():  # Save only non-empty precautions
                Safety.objects.create(precaution=precaution, safety_title=safety_title, description=description,user=request.user)

        # Redirect to success page or render the form again
        return redirect('safety')

    return render(request, 'add_safety.html')