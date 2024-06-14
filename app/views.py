
import datetime
import os
from django.shortcuts import get_object_or_404, render,redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from app.models import *
from admin_app.models import *
from django.contrib import messages
import re
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
# from admin_app.views import section
from app.currency import INRToUSDConverter
from django.contrib.auth import logout
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
# from xhtml2pdf import pisa
from django.db.models import Sum
from .utils import encode_id, decode_id


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)



"""
 Chcek user is login or not
"""
def check_user(request):
    try:
        user = request.session.get('user')
        user = User.objects.get(pk=user)
        cart_items = Cart.objects.filter(uname=user)
        firstname = user.name.split(' ')[0]
        lastname = user.name.split(' ')[1]
        visitor = Visitor.objects.first()
        count = visitor.count if visitor else 0
                        
        context = { 'user':user, 'total_items':len(cart_items), 'firstname':firstname, 'lastname':lastname, 'visitor':count }
    except:
        visitor = Visitor.objects.first()
        count = visitor.count if visitor else 0
        
        context = {
            'visitor':count
        }
    return context


# ===============================================================================================================
"""
    Home Page
    New Arrival
    Most Popular
    Search    
"""

def new_product():
    products = SubProduct.objects.order_by('-created_at')[:5]
    return products


def most_buy_product():
    products = SubProduct.objects.annotate(
        total_quantity=Sum('sub_placeorder__quantity')
    ).order_by('-total_quantity')[:10]
    return products

def home(request):
    # User.objects.all().delete()
    # print('asd')
    user_info = check_user(request)
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=30)
    new_arrival = SubProduct.objects.filter(created_at__gte=last_week)
    new_arrival = new_product()
    most_buy = most_buy_product()
    currency(new_arrival,request.session.get('currency'))
    currency(most_buy,request.session.get('currency'))
    # print(new_arrival)
    
    order_status = placeOrder.objects.filter(order_status='Pending', delivery_date__lt=today)
    for order in order_status:
        order.order_status = 'Delivered'
        order.save()

    
    visitor, created = Visitor.objects.get_or_create(id=1)
    visitor.count += 1
    visitor.save()


    count = visitor.count
    # print(count)
    



    context = { **user_info,
                'new_arrival':new_arrival, 
                'popular_products':most_buy,
                'visitor':count,
               }
    return render(request, 'index.html', context)



def search(request):
    user_info = check_user(request)
    if request.method == 'GET':
        search_query = request.GET.get('search_box')
        if search_query:
            temp_ = SubProduct.objects.filter(product__name__icontains=search_query) | SubProduct.objects.filter(description__icontains=search_query) | SubProduct.objects.filter(product__category__name__icontains=search_query)
            
            # print("       hhsh",temp_)
            currency(temp_,request.session.get('currency'))
            context  = {'products':temp_, **user_info, 'search_query':search_query}
            return render(request, 'search.html', context)
        
# ===============================================================================================================

"""
Contact us  line no: 107-121
About us    line no: 124-126
"""

def contact(request):
    context = check_user(request)
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            comments = request.POST.get('comment')

            contact_obj = Contact.objects.create(name=name, email=email, subject=subject, Comments=comments)
            contact_obj.save()
            return redirect('contact')
    except Exception as e:
        print(e)
    return render(request, 'contact.html',context)


def about(request):
    context = check_user(request)
    return render(request, 'about.html', context)

# ===============================================================================================================

"""
                                Currency Convertor for convert INR to USD
                                using API real time update
s"""

def currency(temp_,currency_type):
    
    currency_converter = INRToUSDConverter(api_key='fca_live_YmDDOQ53V2ORAoTPnzY4M8vJOBhlmqbFi6NNmUBp')
    # currency_type = request.session.get('currency')
    print('currency_type = ',currency_type)  
    try:
        if not currency_type:
            currency_type = ''
            # request.session['currency'] = currency_type

        if 'USD' in currency_type:
            for product in temp_:
                product.product.price_usd = currency_converter.convert_inr_to_usd(product.product.price)

        else:
            for product in temp_:
                product.product.price_usd = product.product.price
    except Exception as e:
        print(e)

# ===============================================================================================================


"""
Product Section 
Three section MAN, WOMAN and KIDS
according cate name display product
line no: 166-184

Show Product
Show Product Details
according product id display product details
"""


def section(request, cate):
    user_info = check_user(request)
    # print(user_info)
    # print(request.session['user'])
    try:
        category_obj = get_object_or_404(Category,name__iexact=cate)     
    except:
        return render(request, '404.html', status=404)
    # print(category_obj)
    
    temp_ = SubProduct.objects.filter(product__category=category_obj)
    # print(temp_)
    product_length = len(temp_)

    currency(temp_,request.session.get('currency'))

    context  = {'products':temp_, 
                 'category':category_obj,
                   **user_info,
                   'product_length':product_length
                   }
    return render(request, 'man.html', context)



def show_product(request, id):
    user_info = check_user(request)
    product_obj = SubProduct.objects.get(pk=id)
    # for debuging
    # print(product_obj.product_size_color.all())
    
    product_obj_size = product_obj.product_size_color.all()
    
    unique_sizes = set()
    for item in product_obj_size:
        unique_sizes.add(item.size)
    
    size_for_product = list(unique_sizes)

    unique_colors = set()
    for item in product_obj_size:
        unique_colors.add(item.color)
    color_for_product = list(unique_colors)

    

    if user_info.get('user'):
        check_item_in_cart = Cart.objects.filter(uname=user_info['user'], subproduct=product_obj)
        
        if check_item_in_cart:
            product_obj.in_cart = True
        else:
            product_obj.in_cart = False
    else:
         check_item_in_cart = None

    currency([product_obj],request.session.get('currency'))
    context  = {'product':product_obj,
                 'sizes':size_for_product , 
                'colors':color_for_product,
                 **user_info, 
                 'check_item_in_cart':check_item_in_cart }
    return render(request, 'show_product.html', context)

# ===============================================================================================================


"""
Below function for the are use for ajax request

get_available_colors:- get the available colors based on the selected size
line no: 242-257

check_stock_quantity:- check the stock quantity based on the selected size and color
line no: 259-270

check_stock:- check the stock quantity based on the selected size and color
"""


@csrf_exempt
def get_available_colors(request):
    product_id = request.POST.get('product_id')
    selected_size = request.POST.get('selected_size')
    
    product = Product.objects.get(id=product_id)
    print("Product ID:", product_id)  # Add this line for debugging
    product_size_colors = ProductSizeNColor.objects.filter(product=product, size__name=selected_size)
    
    data =[]
    for item in product_size_colors:
        data.append({'id':item.color.id, 'name':item.color.name})
    
    a = {'list':data}

    return JsonResponse(a, safe=False)

@csrf_exempt
def check_stock_quantity(request):
    product_id = request.POST.get('product_id')
    selected_size = request.POST.get('selected_size')
    selected_color = request.POST.get('selected_color')

    product_size_color = ProductSizeNColor.objects.get(product_id=product_id, size__name=selected_size, color__name=selected_color)

    stock_quantity = product_size_color.stock_quantity

    return JsonResponse({'stock_quantity': stock_quantity})


def check_stock(subproduct_id, selected_size, selected_color):
    product_size_color = ProductSizeNColor.objects.get(product=subproduct_id, size__name=selected_size, color__name=selected_color)
    stock_quantity = product_size_color.stock_quantity
    return stock_quantity

# ===============================================================================================================


def addcart(request,id): 
    if 'user' not in request.session:
        return redirect('login')
    
    
    if request.method == 'POST':
            user = request.session.get('user')
            subproduct_id = id
            user = User.objects.get(pk=user)
        
        
            if 'addcart' in request.POST:
                quantity = request.POST.get('quantity')
                subproduct = SubProduct.objects.get(pk=subproduct_id)
                cart_size = request.POST.get('selected_size')
                cart_color = request.POST.get('selected_color')
                product_id = request.POST.get('product_id')
                
                stock_quantity = check_stock(product_id, cart_size, cart_color)
                print(f'Stock Quantity: {stock_quantity}')


                if stock_quantity>0:    

                    check_cart = Cart.objects.filter(uname=user, subproduct=subproduct, size=cart_size, color=cart_color)
                    
                    if check_cart.exists():

                        cart_obj = Cart.objects.get(uname=user, subproduct=subproduct, size=cart_size, color=cart_color)
                        cart_obj.quantity += int(quantity) if quantity else 1
                        cart_obj.save()
                    else:
                        cart_quantity = int(quantity) if quantity else 1
                        cart_obj = Cart.objects.create(uname=user, subproduct=subproduct, quantity=cart_quantity, size=cart_size, color=cart_color)
                        cart_obj.save()
                    
                return redirect('show_product', id=subproduct_id)
                
            elif 'sort_addcart' in request.POST:
                quantity = 1
                subproduct = SubProduct.objects.get(pk=subproduct_id)
                # default_size = ""
                check_cart = Cart.objects.filter(uname=user, subproduct=subproduct)
                if check_cart:
                    cart_obj = Cart.objects.get(uname=user, subproduct=subproduct)
                    cart_obj.quantity += int(quantity) if quantity else 1
                    cart_obj.save()

                else:
                    cart_quantity = int(quantity) if quantity else 1
                    cart_obj = Cart.objects.create(uname=user, subproduct=subproduct, quantity=cart_quantity)
                    cart_obj.save()
                    
                return redirect('section', cate=subproduct.product.category.name)
            
    return redirect('home')



def removecart(request,id):
    if 'user' not in request.session:
        return redirect('login')
    item = Cart.objects.get(pk=id)
    item.delete()
    return redirect('cart')

def currancy_cart(temp_,currency_type):
    currency_converter = INRToUSDConverter(api_key='fca_live_YmDDOQ53V2ORAoTPnzY4M8vJOBhlmqbFi6NNmUBp')
    print('currency_type = ', currency_type)

    try:
        if not currency_type:
            currency_type = ''
            # request.session['currency'] = currency_type

        if 'USD' in currency_type:
            for product__ in temp_:
                product__.subproduct.product.price_usd = currency_converter.convert_inr_to_usd(product__.subproduct.product.price)
                product__.total_price_usd = product__.quantity * product__.subproduct.product.price_usd
                # Clear the total_price field when using USD
                product__.total_price = None
        else:
            for product__ in temp_:
                product__.subproduct.product.price_usd = product__.subproduct.product.price 
                # Clear the total_price_usd field when using INR
                product__.total_price_usd = None
                product__.total_price = product__.quantity * product__.subproduct.product.price


    except Exception as e:
        print(e)


def cart(request):
    if 'user' not in request.session:
        return redirect('login')
    user_info = check_user(request)
    
    user = User.objects.get(pk=user_info['user'].id)
    # product_obj = SubProduct.objects.get(pk=user_info['user'].id)


    cart_obj = Cart.objects.filter(uname=user)
    

    
    # product_obj = SubProduct.objects.get(pk=user_info['user'].id)
    # sizes = product_obj.sizes.all()

    currancy_cart(cart_obj,request.session.get('currency'))
    
    for item in cart_obj:
        item.sizes = set(item.subproduct.product_size_color.values_list('size__name', flat=True))
        item.colors = set(item.subproduct.product_size_color.values_list('color__name', flat=True))
        item.total_price = item.quantity * item.subproduct.product.price
    
    
    
    total_cart_price = sum([item.total_price for item in cart_obj if item.total_price is not None])
    total_cart_price_usd = sum([item.total_price_usd for item in cart_obj if item.total_price_usd is not None])

    shipping_price = 50
    shipping_price_usd = 1

    after_shipping_price = total_cart_price + shipping_price
    after_shipping_price_usd = total_cart_price_usd + shipping_price_usd
    
    sizes = Size.objects.all()
    
    context = {
        'users': cart_obj,
        **user_info,
        'total_cart_price': total_cart_price,
        'after_shipping_price': after_shipping_price,
        'number_of_items': len(cart_obj),
        'total_cart_price_usd': total_cart_price_usd,
        'after_shipping_price_usd': after_shipping_price_usd,
        'shipping_price_usd': shipping_price_usd,
        'shipping_price': shipping_price,
        'sizes': sizes
    }
    return render(request, 'cart.html', context)

@csrf_exempt
def get_colors(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        size = request.GET.get('size')

        print(f'Product ID: {product_id}, Size: {size}')
        
        # Query the database to get colors based on the selected size and product ID
        product = Product.objects.get(id=product_id)
        product_size_colors = ProductSizeNColor.objects.filter(product=product, size__name=size)
        
        # Extract color names from the queryset
        colors = [item.color.name for item in product_size_colors]
        
        # Return the list of colors as a JSON response
        return JsonResponse({'colors': colors})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    
def updatecart(request):
    if 'user' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        for item in request.POST:
            if item.startswith('quantity_'):
                cart_id = item.split('_')[1]
                quantity = request.POST[item]
                # {{ item.size }}
                size_key = f'select-size_{cart_id}'
                print(size_key)
                cart_size = request.POST.get(size_key)
                print(cart_size)
                color_key = f'select-color_{cart_id}'
                cart_color = request.POST.get(color_key)


                cart_obj = Cart.objects.get(pk=cart_id)
                cart_obj.quantity = quantity
                cart_obj.color = cart_color
                cart_obj.size = cart_size
                cart_obj.save()
    return redirect('cart')



def checkout(request):
    if 'user' not in request.session:
        return redirect('login')
    
    user_info =check_user(request)
    user = User.objects.get(pk=user_info['user'].id)
    cart_obj = Cart.objects.filter(uname=user)
    

    for item in cart_obj:
        item.total_price = item.quantity * item.subproduct.product.price
    
    currancy_cart(cart_obj,request.session.get('currency'))

    total_cart_price = sum([item.total_price for item in cart_obj if item.total_price is not None])
    total_cart_price_usd = sum([item.total_price_usd for item in cart_obj if item.total_price_usd is not None])

    shipping_price = 50
    shipping_price_usd = 1

    after_shipping_price = total_cart_price + shipping_price
    after_shipping_price_usd = total_cart_price_usd + shipping_price_usd


    state = stateModel.objects.all()

    user_address = AddressModel.objects.filter( user_id=user).first()
    
    
    context = {
        'users':cart_obj,
        **user_info, 
        'state':state,
        'user_address':user_address, 
        'total_cart_price':total_cart_price, 
        'after_shipping_price':after_shipping_price,
        'number_of_items':len(cart_obj),
        'total_cart_price_usd': total_cart_price_usd,
        'after_shipping_price_usd': after_shipping_price_usd,
        'shipping_price_usd': shipping_price_usd,
        'shipping_price': shipping_price
        
        }
    
    return render(request, 'checkout.html',context)



def address(request):
    try:
        if 'user' not in request.session:
            return redirect('login')
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            street_address = request.POST.get('address')
            country = request.POST.get('country')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            phone_number = request.POST.get('phone')
            email = request.POST.get('email')
            user = request.session.get('user')
            user = User.objects.get(pk=user)

            exitsing_address = AddressModel.objects.filter(user_id=user)
            if exitsing_address:
                address_obj = AddressModel.objects.get(user_id=user)
                address_obj.first_name = first_name
                address_obj.last_name = last_name
                address_obj.street_address = street_address
                address_obj.country = country
                address_obj.city = city
                address_obj.state_id = state
                address_obj.pincode = pincode
                address_obj.phone_number = phone_number
                address_obj.email = email
                address_obj.save()
            else:
                address_obj = AddressModel.objects.create(first_name=first_name, last_name=last_name, street_address=street_address, country=country, city=city, state_id=state, pincode=pincode, phone_number=phone_number, email=email, user_id=user)
                address_obj.save()
            return redirect('checkout')


    except Exception as e:
        print(e)
    
    return redirect('checkout')



def place_order(request):
    if 'user' not in request.session:
        return redirect('login')
    else:
        user = request.session.get('user')
        user = User.objects.get(pk=user)
        address_id  = AddressModel.objects.filter(user_id=user).first()


        cart_obj = Cart.objects.filter(uname=user)
        for item in cart_obj:
            item.total_price = item.quantity * item.subproduct.product.price

        total_cart_price = sum([item.total_price for item in cart_obj])
        shipping_charge = 50
        total_quantity = sum([item.quantity for item in cart_obj])
        total_amount = total_cart_price + shipping_charge
        order_date = datetime.date.today()
        order_id = int(datetime.datetime.now().timestamp())
        payment_mode = 'COD'

        delivery_date = order_date + datetime.timedelta(days=7)
        print(f'Delivery Date: {delivery_date}')
        place_order_obj = placeOrder.objects.create(user_id=user, address_id=address_id, order_date=order_date, payment_mode=payment_mode, delivery_date=delivery_date, shipping_charge=shipping_charge, total_quantity=total_quantity, total_amount=total_amount, order_id=order_id)
        place_order_obj.save()
        # print(f'{address_id} - {total_cart_price}   - {total_quantity} -{product_id}  -  {shipping_charge} - {total_amount}  - {order_date} - {order_id}')
       
        for item in cart_obj:
            size_color = item.subproduct.product_size_color.filter(size__name=item.size).first()    

            if size_color:
                purchased_quantity = min(item.quantity, size_color.stock_quantity)
                print(f'Purchased Quantity: {purchased_quantity}')

                if purchased_quantity > 0:
                    sub_placeorder_obj = sub_placeorder.objects.create(
                        order_id=place_order_obj,
                        subproduct_id=item.subproduct,
                        size=item.size,
                        color=item.color,
                        quantity=purchased_quantity,
                        price=item.quantity * item.subproduct.product.price
                    )

                    sub_placeorder_obj.save()

                    size_color.stock_quantity = F('stock_quantity') - purchased_quantity
                    print(f'Stock Quantity: {size_color.stock_quantity}')

                    size_color.save()

            item.delete()
        subject = 'Order Confirmation'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.user_email]
        context = {
            'user': user,
            'order_id': order_id,
            'total_amount': total_amount,
            'order_date': order_date,
            'items': sub_placeorder.objects.filter(order_id=place_order_obj)
        }

        html_message = render_to_string('order_confirmation_email.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            from_email,
            to_email,
            html_message=html_message
        )

        # o_id = place_order_obj.id
        # print(o_id)     

        # try:
        #      return generate_invoice(request, o_id, user)

        # except Exception as e:
        #     print(e)
        hasher_id = encode_id(place_order_obj.order_id)

    return redirect('order_confirm', hasher_id=hasher_id)


def currency_order(temp_, currency_type):
    currency_converter = INRToUSDConverter(api_key='fca_live_YmDDOQ53V2ORAoTPnzY4M8vJOBhlmqbFi6NNmUBp')
    # print('currency_type = ', currency_type)

    try:
        if not currency_type:
            currency_type = ''

            for order_obj in temp_:
                order_obj.price_usd = currency_converter.convert_inr_to_usd(order_obj.price)
                # print(order_obj.price_usd)
                
        else:
            for order_obj in temp_:
                order_obj.price_usd = order_obj.price
                order_obj.total_price_usd = order_obj.order_id.total_amount


    except Exception as e:
        print(e)




def order_confirm(request, hasher_id):
    if 'user' not in request.session:
        return redirect('login')
    else:
        order_id = decode_id(hasher_id)
        order = get_object_or_404(placeOrder, order_id=order_id)
        order_obj = sub_placeorder.objects.filter(order_id=order)
        currency_order(order_obj, request.session.get('currency'))
        context = {'order': order_obj, 'order_id':'order_id'}
        return render(request, 'order_confirm.html', context)


def order_history(request):
    if 'user' not in request.session:
        return redirect('login')
    else:
        user_info = check_user(request)
        user_id = request.session.get('user')
        user = User.objects.get(pk=user_id)
        
        order_obj1 = placeOrder.objects.filter(user_id=user)
        # print(order_obj1)
        order_obj = sub_placeorder.objects.filter(order_id__user_id=user)
        # print(order_obj)
        
        order_objs = []
        for order in order_obj1:
            order_items = sub_placeorder.objects.filter(order_id=order)
            order_objs.append({'order': order, 'items': order_items})
        # print(order_objs)

        order_objs.sort(key=lambda x: x['order'].order_date, reverse=True)

        curency_history(order_objs, request.session.get('currency'))


    context = {'orders': order_objs, **user_info}
    return render(request, 'order_history.html', context)

def curency_history(temp_, currency_type):
    currency_converter = INRToUSDConverter(api_key='fca_live_YmDDOQ53V2ORAoTPnzY4M8vJOBhlmqbFi6NNmUBp')
    # print('currency_type = ', currency_type)
    try:
        if not currency_type:
            currency_type = ''

        if 'USD' in currency_type:
            for order_obj in temp_:
                for item in order_obj['items']:
                    item.price_usd = currency_converter.convert_inr_to_usd(item.price)
                    # print("cuurency",item.price_usd)

                
                    
        else:
            for order_obj in temp_:
                for item in order_obj['items']:
                    item.price_usd = item.price


    except Exception as e:
        print(e)


def return_order(request, order_id):
    if 'user' not in request.session:
        return redirect('login')
    else:
        order_obj = placeOrder.objects.get(pk=order_id)
        if (datetime.date.today() - order_obj.order_date).days < 50:
            sub_order_obj = sub_placeorder.objects.filter(order_id=order_obj)

            for item in sub_order_obj:
                size_color = item.subproduct_id.product_size_color.filter(size__name=item.size, color__name=item.color).first()
                size_color.stock_quantity = F('stock_quantity') + item.quantity
                # print(f'Stock Quantity: {size_color.stock_quantity}')
                size_color.save()
        order_obj.order_status = 'Returned'
        order_obj.save()
        return redirect('order_history')

def cancel_order(request, order_id):
    if 'user' not in request.session:
        return redirect('login')
    else:
        order_obj = placeOrder.objects.get(pk=order_id)
        # if difference between order date and current date is less than 7 days

        if (datetime.date.today() - order_obj.order_date).days < 50:
            sub_order_obj = sub_placeorder.objects.filter(order_id=order_obj)

            for item in sub_order_obj:
                size_color = item.subproduct_id.product_size_color.filter(size__name=item.size, color__name=item.color).first()
                size_color.stock_quantity = F('stock_quantity') + item.quantity
                print(f'Stock Quantity: {size_color.stock_quantity}')
                size_color.save()
            order_obj.order_status = 'Cancelled'
            order_obj.save()    
            # order_obj.delete()

            # print(order_obj)
        else:
            print('Order cannot be cancelled')        
        return redirect('order_history')


def invoice(request, order_id): 
    if 'user' not in request.session:
        return redirect('login')
    else:
        user = request.session.get('user')
        user = User.objects.get(pk=user)
        order_obj = sub_placeorder.objects.filter(order_id=order_id)
        
        currency_order(order_obj, request.session.get('currency'))
        subtotal = sum([item.price for item in order_obj])
        shipping_charge = 50
        


        context = {'order': order_obj, 'subtotal': subtotal, 'shipping_charge': shipping_charge, 'total': subtotal + shipping_charge, 'user': user}
    return render(request, 'invoice.html', context)



def generate_invoice(request, order_id):

    user= request.session.get('user')
    order_obj = sub_placeorder.objects.filter(order_id=order_id)
    subtotal = sum([item.price for item in order_obj])
    shipping_charge = 50
    invoice_html = render_to_string('invoice.html', {
        'order': order_obj, 'subtotal': subtotal, 'shipping_charge': shipping_charge, 'total': subtotal + shipping_charge, 'user': user
        
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    # pisa_status = pisa.CreatePDF(invoice_html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('PDF generation error', status=500)

    # return response

    

#  AUTHENTICATION   
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        has_error= False
        
        if ' ' in username:
            messages.error(request, 'Username Cannot Contain Spaces', extra_tags='user_registration_username')
            has_error = True

        
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&_\-])[A-Za-z\d@$!%*?&_-]{8,}$', user_password):
            messages.error(request, 'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character ex.P@ssword123', extra_tags='user_registration_password')
            has_error = True

        if User.objects.filter(user_name=username).exists() :
            messages.error(request, 'Username Already Exists', extra_tags='user_registration_username')
            has_error = True
        elif User.objects.filter(user_email=user_email).exists():
            messages.error(request, 'Email Already Exists', extra_tags='user_registration_email')
            has_error = True

        if has_error:
            context = { 
                'name': name,
                'username': username,
                'user_email': user_email,
                'password': user_password,
            }
            return render(request, 'register.html', context)
        
        else:
            user = User.objects.create(name=name, user_name=username, user_email=user_email)
            user.set_password(user_password)
            user.save()
            messages.success(request, 'Account Created Successfully !!', extra_tags='user_registration_success')
            return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.user:
        try:
            obj = User.objects.get(user_name=request.user.username)
            request.session['user'] = obj.id
        except:
            if request.user.is_authenticated:
                logout(request)

    if 'user' in request.session:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_name=username)
        except User.DoesNotExist:
            messages.error(request, 'Username Does Not Exist !!', extra_tags='user_login_username')
            return render(request, 'login.html')

        if check_password(password, user.user_password):
            request.session['user'] = user.id
            return redirect('home')
        else:
            
            messages.error(request, 'Incorrect Password !!', extra_tags='user_login_password')
            return render(request, 'login.html')

    return render(request, 'login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            if not User.objects.filter(user_email=email).exists():
                messages.error(request, 'Email Does Not Exist !!', extra_tags='user_forgot_password_email')
                return render(request, 'forgot_password')
            elif not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&]{8,}$', new_password):
                messages.error(request, 'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character ex.P@ssword123', extra_tags='user_registration_password')
                return redirect('forgot_password')
            else:
                user = User.objects.get(user_email=email)
                user.set_password(new_password)
                user.save()
                return redirect('login')
        except Exception as e:
            print(e)
            
    
    return render(request, 'forgot_password.html')

def logout_cus(request):
    
    try:
        del request.session['user']
    except:
        pass
    if request.user.is_authenticated:
        logout(request)
        
    return redirect('home')







