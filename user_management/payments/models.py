from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from exca.models import *
from user_app.models import *

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=4)  # Save only the last 4 digits
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} of Rs. {self.amount}"


class Order(models.Model):
    PAYMENT_METHODS = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Gpay Payment'),
        ('CREDIT', 'Credit Payment'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='COD')
    expected_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders',null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders',null=True)
    Spares = models.ForeignKey(Spares, on_delete=models.CASCADE, related_name='orders',null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    spares = models.ForeignKey(Spares, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)