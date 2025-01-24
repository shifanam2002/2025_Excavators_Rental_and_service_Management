from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    # path('excavators',mini_exca, name= 'mini_exca'),
    path('add_excavator', add_excavator, name='add_excavator'),
    path('',views.index),
    path('category/<int:category_id>/', category_view, name='mini_exca'),
    path('contact_supplier/<int:id>/', views.contact_supplier, name='contact_supplier'),
    path('book_request',book_view.as_view(), name='book_request'),
    path('safety',views.safety, name='safety'),
    path('update-enquiry/<int:id>/', update_enquiry, name='update_enquiry'),
    path('mini_exca/<int:id>/', views.mini_exca, name='mini_exca'),
    path('search', views.search, name='search'),
    path('vw_rentals',views.vw_rentals, name='vw_rentals'),
    path('view_cate',views.view_cate, name='view_cate'),
    path('view_exca',views.view_exca, name='view_exca'),
    path('update_cate/<int:id>/', update_cate_view, name='update_cate'),
    path('update_exca/<int:id>/', update_exca_view, name='update_exca'),
    path('cate_delete/<int:delete_id>/',views.cate_delete, name='cate_delete'),
    path('add-safety/', views.add_safety, name='add_safety'),







]