from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from . models import * 
from . forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
import secrets
import string
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
import json
from django.views.decorators.csrf import csrf_exempt
from payments.models import *
from geopy.distance import geodesic
import geocoder
from django.views import View






# Create your views here.
# def index(request):
#     return render(request,'index.html')


#User Login
def doLogin(request):
    form = LoginForm()
    if request.method == "POST":
        user = authenticate(request,username=request.POST["username"],password=request.POST["password"],is_approved=1)
        print(user)
        if user is None:
            messages.error(request, 'Your account has been deactivated due to unauthorized login attempt.',extra_tags='fail')
            return redirect('/login')
        else:
            data= users.objects.get(username=user)
            print(data)
            login(request, user)
            data = users.objects.get(username=user)
            request.session['ut']=data.usertype
            request.session['uid']=data.id
            messages.success(request, f'Login Successfull!! Welcome {data.username}', extra_tags='suc')
            return redirect('/')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})  


#User Logout
def logout(request):
    auth.logout(request)                
    return redirect('/') 


#User Register
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if users.objects.filter(email=email).exists():
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'z': True})
            else:
                try:
                    # Create new user
                    k= form.save(commit=False)
                    k.password=make_password(form.cleaned_data['password'])
                    k.usertype = 0
                    k.save()
                    messages.success(request, 'Your registration has been successful! You can login now.',extra_tags='suc')
                    return redirect('/login')
                except Exception as e:
                    form.add_error(None, f'An error occurred while saving the form: {e}')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


#User ForgotPassword
def forgotpswd(request):
    return render(request, 'forgotpswd.html', {'user': request.user})


#User Profile
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


#User Generate Password
def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


#User Reset Password
def reset_password(request):
    if request.method == "POST":
                user = users.objects.get(username=request.POST['username'])
                new_password = generate_random_password()
                user.password = make_password(new_password)
                user.save()
                subject = 'password'
                message = "your password is " + str(new_password)
                email_from = settings.EMAIL_HOST_USER
                recepient_list = [user.email]  
                send_mail(subject,message,email_from,recepient_list)
    else:
        return render(request,"forgotpswd.html")
    return redirect('/login')


#User Update Profile
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            if users.objects.filter(email=email).exclude(id=request.user.id).exists():
                form.add_error('email', 'Email already exists')
            else:
                try:
                    user = form.save(commit=False)
                    if form.cleaned_data.get('password'):
                        user.password = make_password(form.cleaned_data['password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('/profile')
                except Exception as e:
                    form.add_error(None, f'An error occurred while updating the profile: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'place': request.user.place,
            'phone': request.user.phone,
            'image': request.user.image
        }
        form = ProfileForm(initial=initial_data, instance=request.user)
    return render(request, 'update_form.html', {'form': form})


#User Change Password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)  
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('/login')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change_form.html', {'form': form})


# ListView
class MyModelListView(ListView):
    model = users
    template_name = 'model_list.html'  
    context_object_name = 'mymodels'

    def get_queryset(self):
        return users.objects.filter(is_superuser=False)


# updateview
class MyModelUpdateView(UpdateView):
    model = users
    form_class = UserForm
    template_name = 'model_update.html'
    context_object_name = 'Mmodel'
    success_url = reverse_lazy('modellist_driver')


# CreateView
class MyModelCreateView(CreateView):
    model = users
    form_class = UserForm
    template_name = 'model_create.html'
    success_url = reverse_lazy('model_list') 

def header(request):
    return render(request, 'header.html')

def myProfile(request):
    return render(request,'myProfile.html')

def footer(request):
    return render(request,'footer.html')

def services(request):
    return render(request,'services.html')

def excavators(request):
    return render(request, 'excavators.html')

# *********************************************************************************************************************
def spare_parts(request):
    # if request.method == 'POST':
    #     form = spareForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('spare_parts')
    # else:
    #     form = spareForm()

    spares = Spares.objects.all()
    return render(request , 'spare_parts.html',{'spares':spares})


def spare_view(request):
    if request.method == 'POST':
        form = SpareContacts(request.POST)
        if form.is_valid():
            form.save()
            return redirect('spare_view')
    else:
        form = SpareContacts()    

    spares = Spares.objects.all()  
    return render(request, 'spare_view.html',{'spares':spares,'form':form})


def spare_update_view(request, pk):
    spare = get_object_or_404(Spares, pk=pk)
    
    if request.method == 'POST':
        form = SpareUpdateForm(request.POST, request.FILES, instance=spare)
        if form.is_valid():
            form.save()
            return redirect('spare_parts') 
        else:
            print(form.errors) 
    else:
        form = SpareUpdateForm(instance=spare)

    return render(request, 'spare_update.html', {'form': form})


def spare_delete(request,delete_id):
    instance= get_object_or_404(Spares,id= delete_id) 
    instance.delete()
    return redirect('spare_parts')

def spare_request(request):
    spare_requests = SpareContact.objects.select_related('spares').all()
    return render(request, 'spare_request.html', {'requests': spare_requests})

def add_spare(request):
    if request.method == 'POST':
        form = spareForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('spare_parts')
    else:
        form = spareForm()

    # spares = Spares.objects.all()
    return render(request , 'add_spare.html',{'form':form})


# @login_required
# def cart_view(request):
#     if request.method == 'POST':
#         spare_id = request.POST.get('spare_id')
#         spare = get_object_or_404(Spares, id=spare_id)
#         # Logic to add the spare to the cart
#         Cart.objects.create(user=request.user, spare=spare)
#         return redirect('cart_view') 


@login_required
def cart_view(request):
    if request.method == 'POST':
        spare_id = request.POST.get('spare_id')
        spare = get_object_or_404(Spares, id=spare_id)
        Cart.objects.create(user=request.user, spare=spare)
        return redirect('cart_view')
    cart_items = Cart.objects.filter(user=request.user,is_paid=False)
    cart_item_ids = [item.id for item in cart_items]
    print(cart_item_ids, 'printing the cart item ids')
    total_price = sum(item.spare.price * item.quantity for item in cart_items)
    return render(request, 'cart_view.html', {'cart_items': cart_items, 'total_price': total_price,'cart_item_ids':cart_item_ids})

    
@login_required
def buy_now(request):
    if request.method == 'POST':
        spare_id = request.POST.get('spare_id')
        spare = get_object_or_404(Spares, id=spare_id)
        # Logic for immediate purchase
        return redirect('checkout', spare_id=spare.id)

def checkout(request, spare_id):
    spare = get_object_or_404(Spares, id=spare_id)
    addresses = Address.objects.all()
    form = AddressForm()  # Initialize the form for the popup
    return render(request, 'checkout.html', {'spare': spare, 'addresses': addresses, 'form': form})

def buy_all(request):
    cart_items = Cart.objects.filter(user=request.user, is_paid=False)
    total_price = sum(item.spare.price * item.quantity for item in cart_items)
    cart_item_ids = [item.id for item in cart_items]
    addresses = Address.objects.filter(user=request.user)
    form = AddressForm()

    print('Total price:', total_price)
    print('cart_item_ids:', cart_item_ids)

    if request.method == 'POST':

        selected_address_id = request.POST.get('address')  # Assuming you have a form field for address selection
        selected_address = Address.objects.get(id=selected_address_id) if selected_address_id else None
     
        for item in cart_items:
            spare = item.spare
            if spare.stock >= item.quantity:  
                spare.stock -= item.quantity
                spare.save()

        # cart_items.delete()
        payment_method = request.POST.get('payment_method')
        order = Order.objects.create(address=selected_address, total_amount=total_price)

        # Redirect based on the selected payment method
        if payment_method == 'credit_card':
            return redirect(f'/payments/payment/?total_amount={total_price}&cart_item_ids={cart_item_ids}')
        elif payment_method == 'gpay':
            return redirect(f'/payments/gpay/?total_amount={total_price}&cart_item_ids={cart_item_ids}')
        elif payment_method == 'cash_on_delivery':
            return redirect(f'/payments/cash-on-delivery/?total_amount={total_price}&cart_item_ids={cart_item_ids}')
        else:
            # If no valid payment method is selected, reload the page
            messages.error(request, "Please select a valid payment method.")
            return redirect('buy_all')
        # return redirect('buy_all')
    
    return render(request, 'buy_all.html', {'cart_items': cart_items,
                                            'total_price': total_price,
                                            'addresses': addresses, 
                                            'form': form,
                                            'cart_item_ids':cart_item_ids})

def address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)  
            address.user = request.user        
            address.save() 
            return redirect('buy_all') 

    addresses = Address.objects.filter(user=request.user)
 
    return redirect('buy_all',{'addresses': addresses})


def spare_detail(request, pk):
    spare = get_object_or_404(Spares, pk=pk)
    return render(request, 'spare_detail.html', {'spare': spare})


@login_required
def remove_cart(request, remove_id):
    if request.method == 'POST':
        instance = get_object_or_404(Cart, id=remove_id, user=request.user)
        instance.delete()
        return redirect('cart_view')
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def update_quantity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON body
            cart_id = data.get('cart_id')  # Get cart item ID
            change = int(data.get('change'))  # Get quantity change (+1 or -1)
            
            # Fetch the cart item
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            cart_item.quantity = max(1, cart_item.quantity + change)  # Ensure quantity stays >= 1
            cart_item.save()  # Save updated quantity
            
            return JsonResponse({'success': True})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# def address_view(request):
#     if request.method == 'POST':
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('address_view')  # Redirect to the same page after saving
#     else:
#         form = AddressForm()

#     # Fetch all saved addresses to display on the page
#     addresses = Address.objects.all()
#     return render(request, 'address_page.html', {'form': form, 'addresses': addresses})

# ********************************************************************************************************

# Driver details
def driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]

            # Check if email already exists
            if users.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email.', extra_tags='pop')
                return render(request, 'driver.html', {'form': form})

            try:
                # Save the user with additional customizations
                user = form.save(commit=False)
                user.is_approved = False  
                user.usertype = 2  
                user.latitude = None
                user.longitude = None
                user.password = make_password(form.cleaned_data['password'])  
                user.save()
                
                messages.success(
                    request,'Your registration request has been submitted successfully. Please wait for admin approval.')
                return redirect('/login')
            except Exception as e:
                # print(f"Error saving form: {e}")
                # messages.error(request, f"An error occurred: {e}")
                form.add_error(None, f'An error occurred while saving the form: {e}')
                return render(request, 'driver.html', {'form': form})
        else:
            # If form is invalid, print errors for debugging
            # print(form.errors)
            messages.error(request, 'Please correct the errors in the form.')
            return render(request, 'driver.html', {'form': form})
    else:
        form = DriverForm()
    return render(request, 'driver.html', {'form': form})


class UpdateLocationView(View):
    def get(self, request):
            id = request.user.id
            user = get_object_or_404(users, id=id, usertype=2)
            g = geocoder.ip('me') 
            if g.latlng:  
                user.latitude = g.latlng[0]
                user.longitude = g.latlng[1]
                user.save()  
                messages.success(request, 'Location updated successfully.', extra_tags='suc')
            else:
                messages.error(request, 'Unable to retrieve location. Please try again.', extra_tags='fail')
            return redirect('/')
    

    


class mymodeldriver(ListView):             
    model = users                       
    template_name = 'modellist_driver.html'
    context_object_name = 'Mmodel'   
    def get_queryset(self):
        return users.objects.filter(is_superuser=False,usertype=2,is_approved=False)       
    

def approve_driver(request, driver_id):
    driver = get_object_or_404(users, id=driver_id)
    driver.approval_status = 'Approved'
    driver.is_active = True
    driver.is_approved = True
    driver.save()
    messages.success(request, f'{driver.username} has been approved.')
    return redirect('modellist_driver')  # Redirects to the driver list page

def reject_driver(request, driver_id):
    driver = get_object_or_404(users, id=driver_id)
    driver.approval_status = 'Rejected'
    driver.is_approved = False
    driver.save()
    messages.warning(request, f'{driver.driverName} has been rejected.')
    return redirect('modellist_driver') 





def mechanics(request):
    if request.method == 'POST':
        form = MechanicForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if users.objects.filter(email=email).exists():
                form = MechanicForm()
                return render(request, 'login.html', {'form': form, 'z': True})
            else:
                try:
                    k = form.save(commit=False)
                    k.is_approved = False
                    k.usertype=3
                    k.latitude = None
                    k.longitude = None
                    k.save()  # This saves the hashed password now
                    messages.success(request, 'Your request has been sent successfully! You have to wait for admin approval.')
                    return redirect('/login')
                except Exception as e:
                    form.add_error(None, f'An error occurred while saving the form: {e}')
        else:
            return render(request, 'mechanics.html', {'form': form})
    else:
        form = MechanicForm()
    return render(request, 'mechanics.html', {'form': form})



class UpdateMechanicLocationView(View):
    def get(self, request, id):
        user = get_object_or_404(users, id=id, usertype=3) 
        g = geocoder.ip('me')
        if g.latlng:
            user.latitude = g.latlng[0]
            user.longitude = g.latlng[1]
            user.save()
            messages.success(request, 'Location updated successfully.',extra_tags='suc')
        else:
            messages.error(request, 'Unable to fetch location. Please try again.',extra_tags= 'fail')
        return redirect('/')  


class mymodelmechanic(ListView):             
    model = users                       
    template_name = 'modellist_mechanic.html'
    context_object_name = 'Mymodelp'
    def get_queryset(self):
        return users.objects.filter(is_superuser=False,usertype=3,is_approved=False)
        


    



def approve_mechanic(request, mechanic_id):
    mechanic = get_object_or_404(users, id=mechanic_id)
    mechanic.approval_status = 'Approved'
    mechanic.is_active =  True
    mechanic.is_approved = True   
    mechanic.save()
    messages.success(request, f'{mechanic.username} has been approved.')
    return redirect('modellist_mechanic')  # Redirects to the mechanic list page

def reject_mechanic(request, mechanic_id):
    mechanic = get_object_or_404(users, id=mechanic_id)
    mechanic.approval_status = 'Rejected'
    mechanic.is_approved = False
    mechanic.save()
    messages.warning(request, f'{mechanic.username} has been rejected.')
    return redirect('modellist_mechanic')  # Redirects to the mechanic list page

def model_delete(request,delete_id):
    instance= get_object_or_404(users,id= delete_id) 
    instance.delete()
    return redirect('model_list')




# ************************************************************************************************************************
class user_view_driver(ListView):
    model = users
    template_name = 'view_driver.html'
    context_object_name = 'Mmodel'
    
    def get_queryset(self):
        return users.objects.filter(is_superuser=False, usertype=2, is_approved=True)

class user_view_driver(ListView):
    model = users
    template_name = 'view_driver.html'
    context_object_name = 'Mmodel'
    
    def get_queryset(self):
        # Get the current user's location
        current_user = self.request.user
        if current_user and not current_user.is_superuser:
            g = geocoder.ip('me')  
            lat, long = g.latlng if g.latlng else (0, 0)
            coords_1 = (lat, long)

            nearby_mechanics = users.objects.filter(usertype=2, is_approved=True)

            location_filter = self.request.GET.get('district', '')
            expertise_filter = self.request.GET.get('license_category', '')


            if location_filter:
                nearby_mechanics = nearby_mechanics.filter(district__icontains=location_filter)
            if expertise_filter:
                nearby_mechanics = nearby_mechanics.filter(license_category__icontains=expertise_filter)


            # Calculate distances
            for mechanic in nearby_mechanics:
                if mechanic.latitude and mechanic.longitude:  
                    coords_2 = (mechanic.latitude, mechanic.longitude)
                    distance = geodesic(coords_1, coords_2).km
                    mechanic.dis = round(distance, 2)  
                else:
                    mechanic.dis = float('inf')  
            # Sort mechanics by distance
            sorted_mechanics = sorted
            sorted_mechanics = sorted(nearby_mechanics, key=lambda mechanic: mechanic.dis)
            return sorted_mechanics[:10]  
        return users.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DriverFilterForm(self.request.GET)
        return context
    
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = book_form() 
        context['is_logged_in'] = self.request.user.is_authenticated and self.request.user.is_active 
        return context
    
    # def post(self, request, *args, **kwargs):  
    #     if not request.user.is_authenticated or not request.user.is_active:
    #         messages.error(request, "Please log in to book a driver.")
    #         return redirect('login')

    #     form = book_form(request.POST)
    #     print("Form data received:", request.POST)  # Debug print

    #     if form.is_valid():
    #         booking = form.save(commit=False)
    #         booking.user_id = request.user  # Assign user instance directly
            
    #         driver_id = request.POST.get('driver_id')
    #         driver = get_object_or_404(users, id=driver_id, is_superuser=False, usertype=2, is_approved=True)
    #         booking.driver_id = driver
    #         booking.save()
    #         messages.success(request, "Booking request submitted successfully!")

    #         return redirect('view_driver') 

    #     else:
    #         print("Form errors:", form.errors)
    #         context = self.get_context_data()
    #         context['form'] = form
    #         messages.error(request, "There was an error with your booking. Please try again.")
    #         return self.render_to_response(context)



# *********************************************************************************************************************   
   

# class user_view_mech(ListView):
#     model =  users
#     template_name = 'view_mech.html'
#     context_object_name = 'Mymodelp'
    
#     def get_queryset(self):
#         return users.objects.filter(is_superuser=False,usertype=3,is_approved=True)

class user_view_mech(ListView):
    model =  users
    template_name = 'view_mech.html'
    context_object_name = 'Mymodelp'
    
    def get_queryset(self):
        print("get_queryset called")  # Debug

        # Get the current user's location
        current_user = self.request.user
        if current_user and not current_user.is_superuser:
            print("Current user:", current_user.username)  # Debug

            g = geocoder.ip('me')  # Get current user's latitude and longitude
            lat, long = g.latlng if g.latlng else (0, 0)
            print("User's location:", lat, long)
            coords_1 = (lat, long)

            # Fetch approved mechanics
            nearby_mechanics = users.objects.filter(usertype=3, is_approved=True)
            print("Mechanics fetched:", nearby_mechanics.count())

            location_filter = self.request.GET.get('district', '')
            expertise_filter = self.request.GET.get('area_of_expertise', '')
            print("Filters received - Location:", location_filter, ", Expertise:", expertise_filter)  # Debug


            if location_filter:
                nearby_mechanics = nearby_mechanics.filter(district__icontains=location_filter)
            if expertise_filter:
                nearby_mechanics = nearby_mechanics.filter(area_of_expertise__icontains=expertise_filter)

            print("Filtered mechanics:", nearby_mechanics.count())  # Debug
            for mechanic in nearby_mechanics:
                if mechanic.latitude and mechanic.longitude:  
                    coords_2 = (mechanic.latitude, mechanic.longitude)
                    distance = geodesic(coords_1, coords_2).km
                    mechanic.dis = round(distance, 2)  
                else:
                    mechanic.dis = float('inf')  

            # Sort mechanics by distance
            sorted_mechanics = sorted
            sorted_mechanics = sorted(nearby_mechanics, key=lambda mechanic: mechanic.dis)
            return sorted_mechanics[:10]  # Return top 10 nearby mechanics
        print("No mechanics found")
        return users.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MechanicFilterForm(self.request.GET)
        return context


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mechanics = context['Mymodelp']
        
        # Attach safety measures to each mechanic
        for mechanic in mechanics:
            mechanic.safety_measures = Safety.objects.filter(user=mechanic)

        context['is_logged_in'] = self.request.user.is_authenticated and self.request.user.is_active
        return context

    # Create a dictionary to map mechanics to their safety measures
        # safety_data = Safety.objects.filter(user__in=mechanics).values('user_id', 'safety_title', 'precaution')
        # safety_dict = {}
        # for safety in safety_data:
        #     if safety['user_id'] not in safety_dict:
        #         safety_dict[safety['user_id']] = []
        #     safety_dict[safety['user_id']].append(safety)

        # # Attach safety measures to each mechanic
        # for mechanic in mechanics:
        #     mechanic.safety_measures = safety_dict.get(mechanic.id, [])

        return context




@login_required
def book_now(request):   
    # mechanics = users.objects.filter(is_superuser=False, usertype=3, is_approved=True)
    if request.method == 'POST':
        form = Mech_book_form(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user_id = request.user  # Assign user instance directly
            mech_id = request.POST.get('mech_id') or request.GET.get('mech_id')
            mechanic = get_object_or_404(users, id=mech_id, is_superuser=False, usertype=3, is_approved=True)
            booking.mech_id = mechanic
            booking.save()
            messages.success(request, "Booking request submitted successfully!")

            return redirect('/book_now') 

    else:
        # Render an empty form if the request is not POST
        mech_id = request.GET.get('mech_id')

        form = Mech_book_form()
        print(form.errors)
    return render(request, 'book_now.html', {'form': form, 'mech_id':mech_id})

@login_required
def bok_now(request):   
    driver_id = request.GET.get('driver_id')
    if request.method == 'POST':
        form = book_form(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user_id = request.user  # Assign user instance directly
            driver_id = request.POST.get('driver_id') or driver_id

            if not driver_id:
                messages.error(request, "Driver ID is required.")
                return redirect('/bok_now')

            # Fetch the driver object and validate it
            try:
                driver = get_object_or_404(users, id=driver_id, is_superuser=False, usertype=2, is_approved=True)
                booking.driver_id = driver
                booking.save()
                messages.success(request, "Booking request submitted successfully!")
                return redirect('/bok_now')
            except Exception as e:
                messages.error(request, f"Error processing booking: {str(e)}")
                return redirect('/bok_now')
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")
    else:
        # If not a POST request, initialize an empty form
        form = book_form()

    # Render the page with the form and the driver_id (if any)
    return render(request, 'bok_now.html', {'form': form, 'driver_id': driver_id})


# ****************************************************************************************************************


def view_order_details(request, mymodel_id):
    mymodel_instance = get_object_or_404(users, id=mymodel_id)
    context = {
        'mymodel_instance': mymodel_instance,    }
    return render(request, 'view_mech.html', context) 

def mini_exca(request):
    return render(request, 'mini_exca.html')

def mech_login(request):
    return render(request,'mech_login.html')

def view_driver(request):
    if request.method == 'POST':
        form = book_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_driver')
    else:
        form = book_form()
    return render(request, 'view_driver.html', {'form':form})





def view_book(request):
    driver_bookings=Booking.objects.filter(driver_id=request.user.id)
    mechanic_bookings = Booking.objects.filter(mech_id=request.user.id)
    return render(request,'view_book.html',{
        'driver_bookings': driver_bookings,
        'mechanic_bookings': mechanic_bookings,
        })


class vw_booking(ListView):
    model = Booking
    template_name = 'view_book.html'
    context_object_name = 'bookings'
    def get_queryset(self):
            print("Logged-in user ID:", self.request.user.id)
            # Filter bookings by the logged-in driver (user)
            book=Booking.objects.filter(driver_id=self.request.user)
            print(book)
            return book


def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.approval_status = 'Accepted'
    booking.save()
    messages.success(request, "Booking accepted successfully!")
    return redirect('view_book')



def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.approval_status = 'Rejected'
    booking.save()
    messages.success(request, "Booking rejected successfully!")
    return redirect('view_book')

def req_driver(request):
    # Fetch booking requests that are pending or in-progress for the logged-in user
    pending_bookings = Booking.objects.filter(user_id=request.user.id, approval_status='Pending').exclude(driver_id=None)
    return render(request, 'req_driver.html', {'bookings': pending_bookings})

def req_mech(request):
    pending_bookings = Booking.objects.filter(user_id=request.user.id, approval_status='Pending').exclude(mech_id=None)
    return render(request, 'req_mech.html', {'bookings': pending_bookings})

def vw_userbook(request):
    # Fetch confirmed bookings for the logged-in user
    confirmed_bookings = Booking.objects.filter(user_id=request.user.id, approval_status='Accepted',).exclude(driver_id=None)   
    return render(request, 'vw_userbook.html', {'bookings': confirmed_bookings})

def vw_mechanic(request):
    confirmed_bookings = Booking.objects.filter(user_id=request.user.id, approval_status='Accepted').exclude(mech_id=None)
    return render(request, 'vw_mechanic.html', {'bookings': confirmed_bookings})



def add_service(request):
    if request.method == 'POST':
        form = MechanicServiceForm(request.FILES, request.POST) 
        if form.is_valid():
            service = form.save(commit=False)
            service.mechanic = request.user  # Assuming the mechanic is logged in
            service.save()
            return redirect('service_list')
    else:
        form = MechanicServiceForm()

    return render(request, 'add_service.html' ,{'form':form})


def update_service_status(request, booking_id):
    if request.method == "POST":
        # Get the booking record
        booking = get_object_or_404(Booking, id=booking_id, driver_id=request.user)
        # Get the new status from the POST request
        new_status = request.POST.get("status")
        if new_status in ["Driver Arrived", "Service Started", "Completed"]:
            booking.service_status = new_status
            booking.save()
            messages.success(request, 'Status updated successfully!')
        else:
            messages.error(request,"Invalid status")

        return redirect('view_book')
    else:
        messages.error(request,"Invalid request method")
        return redirect("view_book")



# ***********************************************************************************************************


def update_mechanic_status(request, booking_id):
    if request.method == "POST":
        # Get the booking record
        booking = get_object_or_404(Booking, id=booking_id, mech_id=request.user)
        # Get the new status from the POST request
        new_status = request.POST.get("status")
        if new_status in ["Mechanic Arrived", "Repair Started", "Completed"]:
            booking.service_status = new_status
            booking.save()
            messages.success(request, 'Status updated successfully!')
        else:
            messages.error(request,"Invalid status")

        return redirect('view_book')
    else:
        messages.error(request,"Invalid request method")
        return redirect("view_book")

# ****************************************************************************************************

class CustomLoginView(LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    



def rate_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == "POST":
        form = RatingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('/vw_userbook')  # Redirect to the bookings page or any other page
    else:
        form = RatingForm(instance=booking)
    
    return render(request, 'rate_booking.html', {'form': form, 'booking': booking})


def contact(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contact')
    else:
        form = ContactUsForm()
    return render(request, 'contact.html',{'form':form})

def view_contact(request):
    contacts = Contact.objects.all()
    return render(request,'view_contact.html',{'contacts':contacts})


# def view_orders(request):
#     orders=Cart.objects.all()
#     return render(request,'view_orders.html',{'orders':orders})


