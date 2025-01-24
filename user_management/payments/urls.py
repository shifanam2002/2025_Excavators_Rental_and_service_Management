from django.urls import path
from . import views

urlpatterns  = [
    path('payment/',views.payment,name='payment'),
    # path('payment/', views.process_payment, name='payment'),
    # path('payment_history/', views.view_payments, name='payment_history'),
    path('payment_success/',views.PaymentSuccessView.as_view(),name='payment_success'),
    path('gpay_payment/',views.gpay_payment,name='gpay_payment'),
    path('cash_on_delivery/',views.cash_on_delivery,name='cash_on_delivery') ,
    path('view_orders/',views.view_orders,name='view_orders'),
    path('payment_history/',views.view_payments,name='payment_history'),
]


