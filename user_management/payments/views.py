from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, Payment
from datetime import datetime
from django.views.generic import TemplateView
from django.http import JsonResponse,HttpResponseNotAllowed
from .models import *
from django.utils.timezone import now
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required






def payment(request):
    total_amount = request.GET.get('total_amount', None)
    cart_item_ids = request.GET.get('cart_item_ids', None)

    print("Total Amount:", total_amount)
    print("Cart Item IDs:", cart_item_ids)  

    if not total_amount:
        messages.error(request, "No cart items selected for payment." , extra_tags='fail')
        return redirect('cart_view')      
    

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')               

        if not (card_number and expiry_date and cvv):
            messages.error(request, "All payment details are required.")
            return redirect('payment')

        try:
            expiry_month, expiry_year = map(int, expiry_date.split('/'))
            current_year = int(datetime.now().strftime('%y'))
            current_month = datetime.now().month
            if expiry_year < current_year or (expiry_year == current_year and expiry_month < current_month):
                messages.error(request, "Card has expired.")
                return redirect('payment')

            payment = Payment.objects.create(
                user=request.user,
                amount=float(total_amount),
                card_number=card_number[-4:],  
                date=datetime.now(),
            )

            
            cart_items = Cart.objects.filter(id__in=cart_item_ids.split(','), user=request.user)
            for item in cart_items:
                item.is_paid = True
                item.save()

            messages.success(request, "Payment successful! Thank you for your purchase.")
            return redirect('success_page')  
        
        except Exception as e:
            messages.error(request, f"Error processing payment: {str(e)}")
            return redirect('payment')

    return render(request, 'payment.html',{'total_amount': total_amount})



class PaymentSuccessView(TemplateView):
    template_name = 'payment_success.html'


        

# def gpay_payment(request):
#     if request.method == 'GET':
#         total_amount = request.GET.get('total_amount')
#         cart_item_ids = request.GET.get('cart_item_ids')
#         context = {
#             'total_amount': total_amount,
#             'cart_item_ids': cart_item_ids,
#         }
#         return render(request, 'gpay_payment.html', context)
    
#     if request.method == 'POST':
#         upi_id = request.POST.get('upi_id')
#         total_amount = request.POST.get('total_amount', '')
#         cart_item_ids = request.POST.get('cart_item_ids', '')
#         print('cart_item_ids',cart_item_ids)

#         if validate_upi_id(upi_id):
#             # Assuming you have access to the Cart and Address objects.
#             try:
#                 # Fetch the cart and address instances
#                 cart = Cart.objects.get(id=cart_item_ids)
#                 address = Address.objects.filter(user=request.user).first()  # Replace with the correct logic to get address

#                 # Create the order
#                 order = Order.objects.create(
#                     payment_method='ONLINE',
#                     expected_date=now().date(),
#                     status='Pending',
#                     cart=cart,
#                     address=address,
#                 )

#                 # Redirect to success page with UPI ID
#                 return redirect(f'/payments/payment_success/?upi_id={upi_id}&status=success')

#             except Cart.DoesNotExist:
#                 return render(request, 'gpay_payment.html', {
#                     'error_message': 'Invalid cart item. Please try again.',
#                     'total_amount': total_amount,
#                     'cart_item_ids': cart_item_ids,
#                 })

#         else:
#             # Render the same page with an error message
#             context = {
#                 'error_message': 'Invalid UPI ID. Please try again.',
#                 'total_amount': total_amount,
#                 'cart_item_ids': cart_item_ids,
#             }
#             return render(request, 'gpay_payment.html', context)


def gpay_payment(request):
    if request.method == 'GET':
        total_amount = request.GET.get('total_amount')
        cart_item_ids = request.GET.get('cart_item_ids')

        if not total_amount or not cart_item_ids:
            # Handle the case where required parameters are missing
            return render(request, 'error.html', {
                'error_message': 'Required parameters are missing.',
            })

        context = {
            'total_amount': total_amount,
            'cart_item_ids': cart_item_ids,
        }
        return render(request, 'gpay_payment.html', context)

    if request.method == 'POST':
        upi_id = request.POST.get('upi_id')
        total_amount = request.POST.get('total_amount', '')
        cart_item_ids = request.POST.get('cart_item_ids')

        if not cart_item_ids:
            return render(request, 'gpay_payment.html', {
                'error_message': 'Cart ID is missing. Please try again.',
                'total_amount': total_amount,
            })

        if validate_upi_id(upi_id):
            try:
                cart_item_ids_list = [int(item) for item in cart_item_ids.strip('[]').split(',')]
                cart_items = Cart.objects.filter(id__in=cart_item_ids_list)

                if not cart_items.exists():
                    return render(request, 'gpay_payment.html', {
                        'error_message': 'No matching cart items found.',
                        'total_amount': total_amount,
                    })

                addresss = Address.objects.filter(user=request.user).first()
                expected_date = datetime.now().date() + timedelta(days=5)
                # spares= Spares.objects.filter(id=cart_items.first().spares.id).first()
                # print('spares',spares)

                for cart in cart_items:
                    Order.objects.create(
                        user=request.user,
                        payment_method='ONLINE',
                        # expected_date=now().date(),
                        status='Pending',
                        cart=cart,
                        # sparess=spares,
                        address=addresss,
                        expected_date=expected_date,
                    )
                cart_items.update(is_paid=True)
                messages.success(request, "Order confirmed successfully" , extra_tags='suc')
                return redirect(f'/payments/payment_success/?upi_id={upi_id}&status=success')

            except Exception as e:
                return render(request, 'gpay_payment.html', {
                    'error_message': f'An error occurred: {e}',
                    'total_amount': total_amount,
                })

        return render(request, 'gpay_payment.html', {
            'error_message': 'Invalid UPI ID. Please try again.',
            'total_amount': total_amount,
        })

    # If request.method is neither GET nor POST
    return HttpResponseNotAllowed(['GET', 'POST'])


def validate_upi_id(upi_id):
    # Add UPI ID validation logic here
    return '@' in upi_id and len(upi_id) > 5






def cash_on_delivery(request):
    # Fetch the latest address for the logged-in user
    user_address = Address.objects.filter(user=request.user).first()
    expected_date = datetime.now().date() + timedelta(days=5)
    
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user, is_paid=False)

        if cart_items.exists() and user_address:
            try:
                # Create orders for each cart item
                for cart in cart_items:
                    Order.objects.create(
                        user=request.user,
                        payment_method="COD",
                        status="Pending",
                        cart=cart,
                        address=user_address,
                        expected_date=expected_date,
                    )
                
                # Update the cart items as paid
                cart_items.update(is_paid=True)
                
                # Show success message and redirect
                messages.success(request, "Order confirmed successfully with COD!" , extra_tags='suc')
                return redirect('cash_on_delivery')

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('cash_on_delivery')

        messages.error(request, "No unpaid cart items found or no saved address available.", extra_tags='fail')
        return redirect('cash_on_delivery')

    return render(request, 'cash_on_delivery.html', {
        'delivery_address': user_address,
        'expected_date': expected_date,
    })
def confirm_cod(request):
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        expected_date = request.POST.get('expected_date')

        order = Order.objects.create(
            payment_method="COD",
            delivery_address=delivery_address,
            expected_date=expected_date,
            status="Confirmed",
        )

        return render(request, 'order_success.html', {'order_id': order.id})
    







def view_orders(request):
    # Fetch orders with related cart and address, and spare via cart
    orders = Order.objects.select_related('cart__spare', 'address').order_by('-created_at')
    
    # Print debug information for verification
    print(f"Orders Count: {orders.count()}")
    for order in orders:
        spare = order.cart.spare
        total_amount = request.GET.get('total_amount')
    
        print(f"Order ID: {order.id}, Address: {order.address}, Spare: {spare.part_name}, Price: {spare.price}, Quantity: {order.cart.quantity}, Total:{total_amount}")
    
    return render(request, 'view_orders.html', {'orders': orders})


@login_required
# def view_payments(request):
#     # Get the payments related to the logged-in user
#     payments = Order.objects.filter(user=request.user).order_by('-created_at')

#     return render(request, 'payment_history.html', {
#         'payments': payments,
#     })

def view_payments(request):
    # Fetch payments related to the logged-in user
    payments = Order.objects.filter(user=request.user, cart__is_paid=True).select_related('cart__spare').order_by('-created_at')

    # Calculate payment amount for display
    for payment in payments:
        payment.amount = payment.cart.spare.price * payment.cart.quantity

    return render(request, 'payment_history.html', {'payments': payments})
