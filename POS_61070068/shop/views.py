
from os.path import exists

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from shop.models import Cart, Order, Order_Product, Product, ProductType


# Create your views here.
@login_required
def index(request):
    product = Product.objects.all()
    types = ProductType.objects.all()
    input_name = request.GET.get('input_name', "")
    input_type = request.GET.get('input_type')
    if input_name:
        product = Product.objects.filter(name__contains=input_name)
    if input_type:
        product = Product.objects.filter(ProductType__name=input_type)
    
    cart = Cart.objects.all()
    incart = Cart.objects.raw('SELECT * FROM shop_cart INNER JOIN shop_product WHERE shop_cart.product_id = shop_product.id')
    price = 0
    for item in incart:
        price += item.price*item.amount

    context = {
        'product':product,
        'cart':incart,
        'price':price,
        'type':types,
        'search_type':input_type,
        'search_name':input_name,
    }
    return render(request, template_name='shop/index.html', context=context)

@login_required
def Add_To_Cart(request, id):
    product = Product.objects.all()
    item = Product.objects.get(pk=id)
    print(item)
    if not(Cart.objects.filter(product_id=item.id).exists()):
        cart = Cart(product_id=item.id)
    else:
        cart = Cart.objects.get(product_id=item.id)
        cart.amount += 1
    
    cart.save()
    #print(cart)

    return redirect(to='index')

@login_required
def sale(request):
    cart = Cart.objects.all()
    #incart = Cart.objects.raw('SELECT * FROM shop_cart INNER JOIN shop_product WHERE shop_cart.product_id = shop_product.id')
    if(cart.count()>0):
        cart_list = []
        price = 0
        print(cart)
        order = Order()
        order.save()
        
        for item in cart:
            product = Product.objects.filter(pk=item.product_id)[0]
            price += product.price*item.amount
            order.products.add(product)
            op = Order_Product.objects.filter(order_id = order.id).filter(product_id = item.product_id)[0]
            op.amount = item.amount
            op.save()

        order.total_price = price
        order.save()

        Cart.objects.raw('DELETE FROM shop_cart')
        Cart.objects.all().delete()
    context ={
        'product':Product.objects.all(),
        'type':ProductType.objects.all(),
        'msg':'Create order id : %s successful' %order.id,
    }
    #return redirect(to='index')
    return render(request, template_name='shop/index.html', context=context)

@login_required
def delete(request, id):
    cart = Cart.objects.get(product_id=id)
    cart.delete()
    return redirect(to='index')

@login_required
def recalculate(request, id, amount):
    print(id)
    cart = Cart.objects.get(product_id=id)
    cart.amount = amount
    cart.save()
    return redirect(to='index')

def my_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            #next_url = request.POST.get('next_url')
            #if next_url:
            #    return redirect(next_url)
            #else:
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    return render(request, template_name='login.html', context=context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('my_login')
