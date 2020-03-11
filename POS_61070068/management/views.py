

from builtins import object

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from shop.models import Product, ProductType

# Create your views here.

@login_required
def manage(request, manage_type):
    typee = ProductType.objects.all()
    products = Product.objects.all()
    type_want = typee
    search_name = request.GET.get('inputname', '')
    search_type = request.GET.get('inputtype')

    products = products.filter(name__contains=search_name)

    if search_type:
        products = products.filter(ProductType__name=search_type)
        type_want = type_want.filter(name=search_type)
        
    context = {
        'type' : typee,
        'type_want' : type_want,
        'product' : products,
        'search_name' : search_name,
        'search_type' : search_type,
        'manage_type' : manage_type, # 1 คือแสดงรายการสินค้า 2 แสดงรายการประเภทสินค้า
    }
    print(type_want)
    return render(request, template_name='management/manage.html', context=context)

@login_required
def edit(request, manage_type, id):
    typee = ProductType.objects.all()
    products = []
    message = ''
    if manage_type == 'product': 
        products = Product.objects.get(pk=id)
    elif manage_type == 'type':
        typee = typee.get(pk=id)
    
    if request.method == 'POST' and manage_type == 'type':
            typee.name = request.POST.get('input_name')
            typee.description = request.POST.get('input_desc')
            typee.save()
            message = 'Edit %s product type sucessfully' %typee.name

    elif request.method == 'POST' and manage_type == 'product':
            products = Product.objects.get(pk=id)
            products.name = request.POST.get('input_name')
            products.description = request.POST.get('input_desc')
            products.price = request.POST.get('input_price')
            products.ProductType_id = request.POST.get('input_type')
            products.save()
            message = 'Edit product : %s sucessfully' %products.name

    context = {
        'manage_type':manage_type,
        'product':products,
        'type':typee,
        'message':message
    }
    return render(request, template_name='management/edit.html', context=context)

@login_required
def create(request, manage_type):
    typee = ProductType.objects.all()
    message = ''
    if request.method == 'POST' and manage_type == 'type':
            typee = ProductType()
            typee.name = request.POST.get('input_name')
            typee.description = request.POST.get('input_desc')
            typee.save()
            message = 'Create %s product type sucessful' %typee.name

    elif request.method == 'POST' and manage_type == 'product':
            products = Product()
            products.name = request.POST.get('input_name')
            products.description = request.POST.get('input_desc')
            products.price = request.POST.get('input_price')
            products.ProductType_id = request.POST.get('input_type')
            products.save()
            message = 'Create product : %s sucessful' %products.name
    context = {
        'manage_type':manage_type,
        'type':typee,
        'message':message
    }
    return render(request, template_name='management/create.html', context=context)
    
@login_required
def delete(request, manage_type, id):
    if manage_type == 'product':
        print(1)
        product = Product.objects.get(pk=id)
        product.delete()
    else:
        typee = ProductType.objects.get(pk=id)
        typee.delete()
    return redirect(to='manage', manage_type=manage_type)
