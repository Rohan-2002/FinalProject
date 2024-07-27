from django import urls, views
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
import razorpay
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Product_master, product_detail,slider,colour,cart_items,category,customer_address,Orders,payment
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# Create your views here.

#home page view
def home(request):
    sliders = slider.objects.all()
    prod = Product_master.objects.all()
    cat = category.objects.all()
    data = {
        'sliders':sliders,
        'prod':prod
    }
    return render(request, 'home.html', data)

#log-in page 
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'invalid username or password')
            return redirect('login')

    return render(request, 'forms/login.html')

#sign-up page
def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['cpassword']
            
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'username already exists')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'email already exists')
                    return redirect('signup')
                else:   
                     user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                     user.save()
                     messages.success(request, 'Account created successfully')
                     return redirect('login')
        else:
            messages.warning(request, 'password do not match')
            return redirect('signup')
    return render(request, 'forms/signup.html')

#user log-out
def logout_user(request):
    logout(request)
    return redirect('home')

# change password page
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = auth.authenticate(username=request.user.username, password=current_password)
        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('changepassword')
            else:
                messages.error(request, 'The new password and confirm password do not match.')
        else:
            messages.error(request, 'Your current password is incorrect.')
    return render(request, 'forms/changepassword.html')

#single product view page
def productview(request,id):
    product = Product_master.objects.get(pk=id)
    images = product_detail.objects.filter(product=product) #.values('product_image_1','product_image_2','product_image_3').distinct()
    sizes = product_detail.objects.filter(product=product).values('prod_size__size_id','prod_size__product_size').distinct()
    colours = product_detail.objects.filter(product=product).values('prod_colour__colour_id','prod_colour__product_colour').distinct()

    data = {
        'product':product,
        'images':images,
        'sizes':sizes,
        'colours':colours,
    }
    return render(request, 'productview.html',data)

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product_master.objects.get(product_id=product_id)
    cart_item = cart_items(customer=user, product=product) 
    cart_item.save()

    # Return a JSON response indicating success
    response_data = {'success': True, 'message': 'is added to your shopping cart!'}
    return JsonResponse(response_data)

def cart(request):
    user = request.user
    cart = cart_items.objects.filter(customer=user)
    total = 0
    for product in cart:
        value = product.quantity * product.product.product_price
        total += value 
    totalamount = total 
    cart_quantity = len(cart)
    
    return render(request, 'cart.html', locals())


def plus_in_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        cart_item = cart_items.objects.get(product=prod_id)
        cart_item.quantity+=1
        cart_item.save()
    
        cart = cart_items.objects.filter(customer=user)
        total = 0
        for product in cart:
            value = product.quantity * product.product.product_price
            total += value 
        totalamount = total
        data = {
            'id':cart_item.product.product_name,
            'quantity':cart_item.quantity,
            'totalamount': totalamount,
            }        

        return JsonResponse(data)


def minus_in_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        cart_item = cart_items.objects.get(product=prod_id)
        cart_item.quantity-=1
        cart_item.save()
        
        cart = cart_items.objects.filter(customer=user)
        total = 0
        for product in cart:
            value = product.quantity * product.product.product_price
            total += value 
        totalamount = total

        data = {
            'id':cart_item.product.product_name,
            'quantity':cart_item.quantity,
            'totalamount': totalamount,
            }        

        return JsonResponse(data)

def remove_from_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        cart_item = cart_items.objects.filter(product=prod_id)
        cart_item.delete()
        
        cart = cart_items.objects.filter(customer=user)
        total = 0
        for product in cart:
            value = product.quantity * product.product.product_price
            total += value 
        totalamount = total

        data = {
            'totalamount': totalamount,
            }        

        return JsonResponse(data)
    

def contactus(request):
    return render(request, 'contactus.html')


def myorder(request):
    return render(request, 'myorder.html')

def checkout(request):
    address_show = customer_address.objects.filter(customer=request.user)
    cart_item = cart_items.objects.filter(customer=request.user)
    total = 0
    for product in cart_item:
        value = product.quantity * product.product.product_price
        total += value 
    totalamount = total
    razorpayamount = int(totalamount*100)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    data = {"amount":razorpayamount, "currency":"INR"}
    payment_response = client.order.create(data=data)
    print(payment_response)
    order_id = payment_response['id']
    order_status = payment_response['status']
    if order_status == 'created':
        Payment = payment(
            customer=request.user,
            total_amount = razorpayamount,
            razorpay_order_id = order_id,
            razorpay_payment_status = order_status
        )
        Payment.save()


    if request.method == "POST":
        user = request.user
        firstName = request.POST['f-name']
        lastName = request.POST['l-name']
        Address1 = request.POST['addline-1']
        Address2 = request.POST['addline-2']
        state = request.POST['country-state']
        landmark = request.POST['landmark']
        pincode = request.POST['p-code']
        mobile_num = request.POST['m-number']
        city = request.POST['city']
        address = customer_address.objects.create(customer=user,first_name=firstName,last_name=lastName,mobile_number=mobile_num,address_line_1=Address1,address_line_2=Address2,landmark=landmark,state=state,pin_code=pincode,city=city)
        address.save()

    
    return render(request, 'checkout.html', locals())


def confirmation(request): 
    if request.method == 'POST':
        address_id = request.POST.get('address_id')  
        address = customer_address.objects.filter(id=address_id)
        cart_item = cart_items.objects.filter(customer=request.user)
        total_product = cart_item.count()
        

        total = 0
        for product in cart_item:
            value = product.quantity * product.product.product_price
            total += value 
        totalamount = total 
        amount =totalamount*100

        # order = Orders.objects.create(customer=request.user,shipping_address=address,total_amount=amount,quantity=total_product)
        # order.save()

        
        

    return render(request, 'confirmation.html', locals())

def search(request):
    product = Product_master.objects.all()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            tubers = product.filter(product_description__icontains=keyword)
    return render(request, 'search.html',locals())


