from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
from django.contrib import messages
from .models import *
from . forms import *
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# def home(request):
#     return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops})

class product_details_view(View):
    def get(self, request,pk):
        product = Product.objects.get(pk = pk)
        item_in_cart = False
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_in_cart':item_in_cart})



# def product_detail(request):
#     return render(request, 'app/productdetail.html')
@login_required
def add_to_cart(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    Cart(user=request.user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user] 
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'cart':cart,'total_amount':total_amount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')
        
@login_required    
def plus_cart(request):
    if request.method == "GET":
        user = request.user
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product = product_id) & Q(user = user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user] 
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
            data = {
                'quantity':c.quantity,
                'amount' : amount,
                'total_amount':amount + shipping_amount,
            }
            return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == "GET":
        user = request.user
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product = product_id) & Q(user = user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user] 
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
            
            data = {
                'quantity':c.quantity,
                'amount' : amount,
                'total_amount':amount + shipping_amount,
            }
            return JsonResponse(data)

@login_required    
def remove_cart(request):
    if request.method == "GET":
        user = request.user
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=user))
        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = Cart.objects.filter(user=user) 

        if cart_product.exists():
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount

            data = {
                'amount': amount,
                'total_amount': amount + shipping_amount,
                'cart_empty': False
            }
        else:
            data = {
                'amount': 0.0,
                'total_amount': 0.0,
                'cart_empty': True
            }
        return JsonResponse(data)

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

class Customerprofile(View):
    def get(self, request):
        fm = customerProfileForm()
        return render(request,'app/profile.html',{'form':fm,'active':'btn-primary'})
    def post(self,request):
        fm = customerProfileForm(request.POST)
        if fm.is_valid():
            usr = request.user
            name = fm.cleaned_data['name']
            area = fm.cleaned_data['locality']
            city = fm.cleaned_data['city']
            division = fm.cleaned_data['division']
            reg = Customer(user=usr,name = name, locality = area, city = city, division = division)
            reg.save()
            messages.success(request, "Congratulations! Your profile data has been submitted.")
            fm=customerProfileForm()
        return render(request, 'app/profile.html',{'form':fm,'active':'btn-primary'})

class Address(View):
    def get(self,request):
        fm = Customer.objects.filter(user = request.user)
        return render(request,'app/address.html',{'form':fm,'active':'btn-primary'})

@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user).order_by('ordered_date')
    return render(request, 'app/orders.html',{'order_placed':order_placed})


class mobile_view(View):
    def get(self, request, data = None):
            if data == None:
                mobiles = Product.objects.filter(category = 'M')
            elif data == 'xiaomi' or data == 'samsung' or data == 'pixel' or data == 'apple':
                mobiles = Product.objects.filter(category = 'M').filter(brand=data)
            elif data == 'below':
                mobiles = Product.objects.filter(category = 'M').filter(discount_price__lt = 50000)
            elif data == 'above':
                mobiles = Product.objects.filter(category = 'M').filter(discount_price__gt = 50000)
            return render(request, 'app/mobile.html',{'mobiles':mobiles})
            
class laptop_view(View):
    def get(self, request, data = None):
            if data == None:
                laptops = Product.objects.filter(category = 'L')
            elif data == 'Macbook' or data == 'HP' or data == 'Dell' or data == 'Lenevo':
                laptops = Product.objects.filter(category = 'L').filter(brand=data)
            elif data == 'below':
                laptops = Product.objects.filter(category = 'L').filter(discount_price__lt = 50000)
            elif data == 'above':
                laptops = Product.objects.filter(category = 'L').filter(discount_price__gt = 50000)
            return render(request, 'app/laptop.html',{'laptops':laptops})


class topwear_view(View):
    def get(self, request, data = None):
            if data == None:
                topwear = Product.objects.filter(category = 'TW')
            elif data == 'shirt' or data == 't-shirt' or data == 'tops' or data == 'punjabi' or data == 'tops':
                topwear = Product.objects.filter(category = 'TW').filter(title=data)
            elif data == 'below':
                topwear = Product.objects.filter(category = 'TW').filter(discount_price__lt = 2000)
            elif data == 'above':
                topwear = Product.objects.filter(category = 'TW').filter(discount_price__gt = 2000)
            return render(request, 'app/topwear.html',{'topwear':topwear})
            

class customerregistration(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Your account has been created.")
            form.save()
            form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

class custom_logout_view(View):
    def get(self,request):
        logout(request)
        return redirect('login')
    
@login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user] 
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'address':address,'total_amount':total_amount,'cart_item':cart_item})

@login_required
def payment_done(request):
    user = request.user
    customer_id = request.GET.get('customerID')
    print('Customer id',customer_id)
    customer = Customer.objects.get(id=customer_id)
    cart = Cart.objects.filter(user=user)
    
    for c in cart:
        OrderPlaced(user=user,customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
    