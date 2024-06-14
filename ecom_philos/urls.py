"""
URL configuration for ecom_philos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from .views import *
from app.views import *
from admin_app.views import *
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/login/', auth_views.LoginView.as_view(template_name='admin_login.html'), name='admin_login'),
    path('admin/', admin.site.urls),

    path('get_product_sizencolor/' ,get_product_sizencolor , name='get_product_sizencolor'),
    path('get_available_colors/' ,get_available_colors , name='get_available_colors'),
    path('edit_product_sizencolor/' ,edit_product_sizencolor , name='edit_product_sizencolor'),
    path('check_stock_quantity/' ,check_stock_quantity , name='check_stock_quantity'),

    path('admin_side/', admin_side, name='admin_side'),
    path('add_category/', add_category, name='add_category'),
    path('add_size/', add_size, name='add_size'),
    path('add_color/', add_color, name='add_color'),
    path('allproduct/', allproduct, name='allproduct'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:id>', edit_product, name='edit_product'),
    path('edit_quantity/<int:id>', edit_quantity, name='edit_quantity'),
    path('edit_quantity/getstock/' ,getstock , name='getstock'),
    path('edit_quantity/getcolor/', getcolor , name='getcolor'),
    path('remove_product/<int:id>', remove_product, name='remove'),
    path('remove_products/<int:id>', remove_products, name='remove_products'),
    path('order_list/', order_list, name='order_list'),
    path('user_list/', user_list, name='user_list'),
    path('product_list/', product_list, name='product_list'),
    path('contact_list/', contact_list, name='contact_list'),
    
    path('order_detail/<int:order_id>', order_detail, name='order_detail'),
    path('order_delete/<int:order_id>', order_delete, name='order_delete'),
    
    path('1/', redirect_to_admin, name='redirect_to_admin'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin_logout/', admin_logout, name='admin_logout'),
    
    
    

    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_cus, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),

    # path('social-auth/', include('social_django.urls', namespace='social')),
    path('invoice/<int:order_id>/', invoice, name='invoice'),
    path('generate_invoice/<int:order_id>/', generate_invoice, name='generate_invoice'),

    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('cart/', cart, name='cart'),
    path('addcart/<int:id>', addcart, name='addcart'),
    path('get_colors/', get_colors , name='get_colors'),
    path('removecart/<int:id>', removecart, name='removecart'),
    path('updatecart/', updatecart, name='updatecart'),
    path('checkout/', checkout, name='checkout'),
    path('address/', address, name='address'),
    path('placeorder/', place_order, name='placeorder'),
    path('order_confirm/<str:hasher_id>/', order_confirm, name='order_confirm'),
    path('order_history/', order_history, name='order_history'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('return_order/<int:order_id>/', return_order, name='return_order'),
    path('show_product/<int:id>/', show_product, name='show_product'),
    path('<str:cate>/' ,section , name='section'),


]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "app.views.custom_page_not_found"