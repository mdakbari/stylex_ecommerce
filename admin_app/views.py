from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect

from django.views.decorators.csrf import csrf_exempt
from app.models import *
from admin_app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime
import json


# Create your views here.


# Save Image To Another Server
def save_img_to_another_server(file_obj, text):
    url = "https://images.prathmeshsoni.works/images/?format=json"

    files=[
        # ('file',('demo.png',open('demo.png','rb'),'image/png'))
        ('file', (file_obj.name, text, file_obj.content_type))
    ]
    headers = {
        'Authorization': 'token 9202c558d91744d146cf96f4f9bf464240acfbb9',
        'Origin': 'https://images.prathmeshsoni.works',
        'Referer': f'{url}',
    }

    response = requests.request("POST", url, headers=headers, data={}, files=files)
    try:
        json_data = response.json()
        return json_data['file']
    except:
        return ''


def add_product(request):
    if request.method == 'POST':
        if 'product_form' in request.POST:
            product_name = request.POST.get('product_name')
            product_price = request.POST.get('product_price')
            category = request.POST.get('category')

            if not product_name or not product_price or not category:
                messages.error(request, 'Please enter all fields')
                return redirect('add_product')
            
            product_obj = Product.objects.create(name=product_name, price=product_price, category_id=category)
            product_obj.save()
        elif 'sub_product_form' in request.POST:
            product = request.POST.get('product')
            description = request.POST.get('description')
            images = request.FILES.get('images')

            productsize = request.POST.getlist('productsize')
            url = save_img_to_another_server(images, images.file.read())

            if not product or not description or not images or not productsize:
                messages.error(request, 'Please enter all fields')
                return redirect('add_product')
            

            subproduct_obj = SubProduct.objects.create(product_id=product, description=description, image=url)
            subproduct_obj.product_size_color.set(productsize)
            subproduct_obj.save()
        elif 'size_form' in request.POST:
            product = request.POST.get('product')
            size = request.POST.get('sizes')
            color = request.POST.get('colors')
            quantity = request.POST.get('stock')
            
                       
            if not product or not size or not color or not quantity:
                messages.error(request, 'Please enter all fields')
                return redirect('add_product')  
            elif ProductSizeNColor.objects.filter(product_id=product, size_id=size, color_id=color).exists():
                messages.error(request, 'Size and color is  already exists', extra_tags='size_exists')
                return redirect('add_product')
            
            size_obj = ProductSizeNColor.objects.create(product_id=product, size_id=size, color_id=color, stock_quantity=quantity)
            size_obj.save()


    categories = Category.objects.all()
    product = Product.objects.all()
    size = Size.objects.all()
    color = Color.objects.all()
    sizeandcolor__ = ProductSizeNColor.objects.all()
    
    # print(sizeandcolor__)


    context = {
        'categories':categories,
        'products':product,
        'sizes':size,
        'colors':color,
        'sizeandcolor':sizeandcolor__,
    }

    return render(request, 'add_product.html',context)


def edit_product(request, id):
    product = SubProduct.objects.get(id=id)
    sizeandcolor = ProductSizeNColor.objects.all()
    # print(sizeandcolor)

    excluded_sizes = product.product_size_color.all()
    # print(excluded_sizes)
    available_sizes = sizeandcolor.exclude(id__in=excluded_sizes)

    size_color = product.product_size_color.all()
    # print(product.product_size_color.all())

    if request.method == 'POST':
        description = request.POST.get('description')
        productsize = request.POST.getlist('productsize')
        image = request.FILES.get('images')


        if image is not None:
            url=  save_img_to_another_server(image, image.file.read())
            product.image = url
            product.save()
        else:
            product.image = product.image
            product.save()

        
        # if request.FILES.get('images') is not None:
        #     image = request.FILES.get('images')
        #     url = save_img_to_another_server(image, image.file.read())
        #     product.image = url
        #     print(url)
            
        # else:
        #     image = product.image

        if not description or not productsize:
            messages.error(request, 'Please enter all fields')
            return redirect('edit_product', id=id)
        
        
        size = productsize + list(size_color)   
        
        product.description = description
        product.product_size_color.set(size)

        product.save()
        return redirect('allproduct')
    
    

    context = {
        'product': product,
        'sizeandcolor':available_sizes,



    }
    return render(request, 'edit_product.html', context)

def edit_quantity(request,id):
    product = SubProduct.objects.get(id=id)
    # print(product)
    sizeandcolor = ProductSizeNColor.objects.filter(product=product.product_id)
    # print(sizeandcolor)

    unique_sizes = [size.size for size in sizeandcolor]
    sizes = set(unique_sizes)
    # print(sizes)

    unique_colors = [color.color for color in sizeandcolor]
    colors = set(unique_colors)
    # print(colors)


    if request.method == 'POST':
        product_id = request.POST.get('product')
        size_id = request.POST.get('sizes')
        color_id = request.POST.get('colors')
        stock_quantity = request.POST.get('stock')
        # print(product_id)
        # print(size_id)
        # print(color_id)
        # print(stock_quantity)
        if not product_id or not size_id or not color_id or not stock_quantity:
            messages.error(request, 'Please enter all fields')
            return redirect('edit_quantity', id=id)
        # elif size_id
        try:
            stock_obj = ProductSizeNColor.objects.get(product_id=product_id, size_id=size_id, color_id=color_id)
            stock_obj.stock_quantity = stock_quantity
            stock_obj.save()
        except ProductSizeNColor.DoesNotExist:
            stock_obj = ProductSizeNColor.objects.create(product_id=product_id, size_id=size_id, color_id=color_id, stock_quantity=stock_quantity)
            stock_obj.save()
        
    context = {
        'product':product,
        'sizeandcolor':sizeandcolor,
        'sizes':sizes,
        'colors':colors,

    }

    return render(request, 'edit_quantity.html', context)



def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if not category_name:
            messages.error(request, 'Please enter a category')
            return redirect('add_category')
        else:
            category_obj = Category.objects.filter(name=category_name)
            if category_obj.exists():
                messages.error(request, 'Category already exists')
                return redirect('add_category')
        category_obj = Category.objects.create(name=category_name)
        category_obj.save()
    return render(request, 'add_category.html')

def add_size(request):
    if request.method == 'POST':
        size_name = request.POST.get('size_name')

        if not size_name:
            messages.error(request, 'Please enter a size')
            return redirect('add_size')
        else:
            size_obj = Size.objects.filter(name=size_name)
            if size_obj.exists():
                messages.error(request, 'Size already exists')
                return redirect('add_size')
        
        size_obj = Size.objects.create(name=size_name)
        size_obj.save()
    return render(request, 'add_size.html')

def add_color(request):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        if not color_name:
            messages.error(request, 'Please enter a color')
            return redirect('add_color')
        else:
            color_obj = Color.objects.filter(name=color_name)
            if color_obj.exists():
                messages.error(request, 'Color already exists')
                return redirect('add_color')
            
        color_obj = Color.objects.create(name=color_name)
        color_obj.save()
    return render(request, 'add_color.html')




@csrf_exempt
def getcolor(request):
    size_id = request.GET.get('size_id')
    product_id = request.GET.get('product_id')
    
    colors = ProductSizeNColor.objects.filter(size_id=size_id, product_id=product_id)
    
    data = [{'id': color.color.id, 'name': color.color.name} for color in colors]
    
    return JsonResponse({'colors': data})

@csrf_exempt
def getstock(request):
    product_id = request.GET.get('product_id')
    size_id = request.GET.get('size_id')
    color_id = request.GET.get('color_id')
    
    try:
        stock_obj = ProductSizeNColor.objects.get(product_id=product_id, size_id=size_id, color_id=color_id)
        stock = stock_obj.stock_quantity
    except ProductSizeNColor.DoesNotExist:
        stock = 0
    return JsonResponse({'stock':stock})



@login_required(login_url='/admin/login/?next=/admin_side/')
def remove_product(request, id):
    product = SubProduct.objects.get(id=id)
    product.delete()
    return redirect('allproduct')


@login_required(login_url='/admin/login/?next=/admin_side/')
def allproduct(request):
    products = SubProduct.objects.all().order_by('-created_at')
   
   
    context = {
        'products':products,
    }
    return render(request, 'all_product.html',context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def remove_products(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product_list')


@login_required(login_url='/admin/login/?next=/admin_side/')
def product_list(request):
    # print('product_list')
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products':products,
    }
    return render(request, 'product_list.html', context)

@login_required(login_url='/admin/login/?next=/admin_side/')
def admin_side(request):
    return redirect('admin_dashboard')

@staff_member_required
def admin_logout(request):
    logout(request)
    return redirect('admin_side')

@login_required(login_url='/admin/login/?next=/admin_side/')
def user_list(request):
    users = User.objects.all().order_by('-created_at')
    context = {
        'users':users,
    }
    return render(request, 'user_list.html', context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def order_list(request):
    orders = placeOrder.objects.all().order_by('-order_date')
    # print(orders)
    context = {
        'orders':orders,
    }
    return render(request, 'order_list.html',context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at')
    # print(contacts)
    
    context = {
        'contacts':contacts,
    }
    return render(request, 'contact_list.html', context)

@login_required(login_url='/admin/login/?next=/admin_side/')
def order_detail(request, order_id):
    order = get_object_or_404(placeOrder, order_id=order_id)
    order_items = sub_placeorder.objects.filter(order_id=order)
  
    subtotal = sum([item.subproduct_id.product.price * item.quantity for item in order_items])
    shipping_charge = 50
    total = subtotal + shipping_charge

    context = {
        'order': order,
        'order_items': order_items,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'total': total,
    }
    return render(request, 'order_detail.html', context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def order_delete(request, order_id):
    order = get_object_or_404(placeOrder, order_id=order_id)
    order.delete()
    return redirect('order_list')


def redirect_to_admin(request):
    return redirect('admin_dashboard')

def admin_logout(request):
    logout(request)
    return redirect('admin_side')

@login_required(login_url='/admin/login/?next=/admin_side/')
def admin_dashboard(request):
    total_booking = placeOrder.objects.all().count()
    total_user = User.objects.all().count()
    total_product = SubProduct.objects.all().count()

    total_earning = sum([order.total_amount for order in placeOrder.objects.all()])
    # print(total_earning)
    # print("-----------------------------           ", total_booking, total_user, total_product)

    return_order = placeOrder.objects.filter(order_status='Returned').count()
    cancel_order = placeOrder.objects.filter(order_status='Cancelled').count()
    delivered_order = placeOrder.objects.filter(order_status='Delivered').count()

    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year, 12, 31)
    print(datetime.now())
    man_purchases = sub_placeorder.objects.filter(
        subproduct_id__product_id__category__name__icontains='Man',
        created_at__range=(start_date, end_date)
    ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('quantity')).values('month', 'total')

    woman_purchases = sub_placeorder.objects.filter(
        subproduct_id__product__category__name__icontains='Woman',
        created_at__range=(start_date, end_date)
    ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('quantity')).values('month', 'total')

    kid_purchases = sub_placeorder.objects.filter(
        subproduct_id__product__category__name__icontains='Kid',
        created_at__range=(start_date, end_date)
    ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('quantity')).values('month', 'total')

    print(man_purchases)
    def format_monthly_data(queryset):
        monthly_data = {i: 0 for i in range(1, 13)}
        for item in queryset:
            monthly_data[item['month'].month] = item['total']
        return [monthly_data[i] for i in range(1, 13)]

    man_purchases_monthly = format_monthly_data(man_purchases)
    print(man_purchases_monthly)
    woman_purchases_monthly = format_monthly_data(woman_purchases)
    kid_purchases_monthly = format_monthly_data(kid_purchases)

    print(man_purchases_monthly,woman_purchases_monthly,kid_purchases_monthly)

    total_earning_monthly = placeOrder.objects.filter(
        order_date__range=(start_date, end_date)
    ).annotate(month=TruncMonth('order_date')).values('month').annotate(total=Sum('total_amount')).values('month', 'total')

    total_earning_Monthly =  format_monthly_data(total_earning_monthly)
    # print(total_earning_Monthly)
    # print(total)


    
    context = {
        'total_booking':total_booking,
        'total_user':total_user,
        'total_product':total_product,
        'total_earning':total_earning,
        'return_order':return_order,
        'cancel_order':cancel_order,
        'delivered_order':delivered_order,
       'man_purchases_monthly': json.dumps(man_purchases_monthly),
        'woman_purchases_monthly': json.dumps(woman_purchases_monthly),
        'kids_purchases_monthly': json.dumps(kid_purchases_monthly), 
        'total_earning_Monthly': json.dumps(total_earning_Monthly),
    }
    return render(request, 'admin_dashboard.html', context)





@csrf_exempt
def get_product_sizencolor(requset):
    product_id = requset.POST.get('id')
    product = Product.objects.get(id=product_id)
    productsizecolor = ProductSizeNColor.objects.filter(product=product)
    data = []
    for sizecolor in productsizecolor:
        product_name = f'{sizecolor.product.name} - {sizecolor.size.name}-{sizecolor.color.name}'
        data.append({
            'product_name':product_name,
            'id':sizecolor.id
        })
    a = {'list':data}
    return JsonResponse(a, safe=False)


@csrf_exempt
def edit_product_sizencolor(request):
    product_id = request.POST.get('id')
    selected_size_ids = request.POST.getlist('selected_sizes')  # Get the selected size IDs

    product = Product.objects.get(id=product_id)
    product_size_colors = ProductSizeNColor.objects.filter(product=product)
    data = []
    for sizecolor in product_size_colors:
        product_name = f' {sizecolor.product.name} - {sizecolor.size.name} - {sizecolor.color.name}'
        data.append({
            'product_name': product_name,
            'id': sizecolor.id
        })

    response_data = {'list': data}
    return JsonResponse(response_data, safe=False)