from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    # path('',views.index),
    path('login',views.doLogin, name='login'),
    path('register',views.Register),
    path('forgotpswd/',views.forgotpswd),
    path('logout',views.logout),
    path('generate_random_password',views.generate_random_password),
    path('reset_password',views.reset_password,name='password_change'),
    path('profile',views.profile),
    path('edit_profile',views.edit_profile),
    path('password_change_form',views.change_password),
    path('header',views.header),
    path('excavators',views.excavators),
    path('driver',views.driver),
    path('mechanics',views.mechanics),
    path('footer',views.footer),
    path('services',views.services),
    path('mini_exca',views.mini_exca),
    path('mech_login',views.mech_login),
    path('book_now',views.book_now),
    path('bok_now',views.bok_now),
    path('myProfile',views.myProfile), 
    # path('spare_view',views..spare_view),
    path('spare_parts', views.spare_parts, name='spare_parts'),
    path('spare_view', views.spare_view, name='spare_view'),
    path('spare_update/<int:pk>/', spare_update_view, name='spare_update'),
    path('spare_request', spare_request, name='spare_request'),
    path('rate_booking/<int:booking_id>/', views.rate_booking, name='rate_booking'),


    # path('contact_spare/', views.contact_spare, name='contact_spare'),




# Views updateview, listview, createview
    path('model_list', MyModelListView.as_view(), name='model_list'),
    path('model_update/<int:pk>/', MyModelUpdateView.as_view(), name='model_update'),
    path('model_create', MyModelCreateView.as_view(), name='model_create'),
    path('modellist_driver',mymodeldriver.as_view(), name= 'modellist_driver'),
    path('approve_driver/<int:driver_id>/', views.approve_driver, name='approve_driver'),
    path('reject_driver/<int:driver_id>/', views.reject_driver, name='reject_driver'),
    path('modellist_mechanic',mymodelmechanic.as_view(), name='modellist_mechanic'),
    path('approve_mechanic/<int:mechanic_id>/', views.approve_mechanic, name='approve_mechanic'),
    path('reject_mechanic/<int:mechanic_id>/', views.reject_mechanic, name='reject_mechanic'),
    path('view_driver',user_view_driver.as_view(), name='user_view_driver'),
    # path('spare_parts',mySpare.as_view(),name='spare_parts'),

    path('model_delete/<int:delete_id>/',views.model_delete, name='model_delete'),
    path('spare_delete/<int:delete_id>/',views.spare_delete, name='spare_delete'),
    # path('remove_cart/<int:remove_id>/',views.remove_cart, name='remove_from_cart'),
    path('remove_cart/<int:remove_id>/', views.remove_cart, name='remove_from_cart'),

    path('view_mech',user_view_mech.as_view(),name='view_mech'),
    path('view_order_details',views.view_order_details),
    # path('view_book',vw_booking.as_view(), name='view_book'),
    path('view_book',views.view_book, name='view_book'),
    path('accept_booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('update_service_status/<int:booking_id>/', views.update_service_status, name='update_service_status'),
    path('update_mechanic_status/<int:booking_id>/',views.update_mechanic_status, name = 'update_mechanic_status'),
    path('vw_userbook',views.vw_userbook, name='vw_userbook.html'),
    path('vw_mechanic',views.vw_mechanic, name='vw_mechanic.html'),
    path('req_driver',views.req_driver, name='req_driver'),
    path('req_mech',views.req_mech, name='req_mech'),
    path('add_service', views.add_service, name='add_service'),
    path('contact',views.contact, name='contact'),
    path('view_contact',views.view_contact, name='view_contact'),
    path('add_spare',views.add_spare, name='add_spare'),
    path('buy-now/', views.buy_now, name='buy_now'),
    path('cart_view', views.cart_view, name='cart_view'),
    path('spare/<int:pk>/',views.spare_detail, name= 'spare_detail'),
    path('update_quantity/',views.update_quantity, name='update_quantity'),
    path('checkout/<int:spare_id>/', views.checkout, name='checkout'),
    path('addresses/', views.address_view, name='address_view'),
    path('buy_all/', views.buy_all, name='buy_all'),
    path('mechanic/<int:id>/update-location/', UpdateMechanicLocationView.as_view(), name='update_mechanic_location'),
    path('driver/update-location/', UpdateLocationView.as_view(), name='update_driver_location'),


    


    # path('checkout',views.buy_now,name='checkout')
    # path('cart_view',views.cart_view,name='cart_view')



    # path('service_list/', views.service_list, name='service_list')


]