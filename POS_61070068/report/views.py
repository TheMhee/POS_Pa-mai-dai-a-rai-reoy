from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Cart, Order, Order_Product, Product, ProductType

# Create your views here.
@login_required
def report_search(request, day, month, year, week):
    report_type = ''
    orders = Order.objects.all()
    date_time = datetime.now()
    need_time = 0
    print(orders)
    if day != 0:
        orders = Order.objects.filter(date_time__day=day)
        report_type = 'day'
        need_time = day
    elif week != 0:
        orders = Order.objects.filter(date_time__week=week)
        report_type = 'week'
        need_time = week
    elif month != 0:
        orders = Order.objects.filter(date_time__month=month)
        report_type = 'month'
        need_time = month
    elif year != 0:
        orders = Order.objects.filter(date_time__year=year)
        report_type = 'year'
        need_time = year
    print(orders)
    orders_list = []
    sold_list = []
    sold_temp = []
    total_price = 0
    for order in orders:
        order_obj = {}
        order_obj['detail'] = order
        products = Product.objects.filter(order__id=order.id)
        obj = []
        for product in products:
            # หาสินค้าที่ถูกสั่งตามออเดอร์
            amount = Order_Product.objects.filter(
                order_id=order.id).filter(product_id=product.id)[0].amount
            product_detail = {
                'product_detail': product,
                'amount': amount,
            }
            obj.append(product_detail)

            # รวมสินค้าทั้งหมดที่ถูกสั่ง
            sold_detail = {}
            if product not in sold_temp:
                sold_temp.append(product)
                sold_detail = {
                    'product': product,
                    'amount': amount,
                }
                sold_list.append(sold_detail)
            else:
                sold_list[sold_temp.index(product)]['amount'] += amount

        order_obj['product'] = obj
        orders_list.append(order_obj)

        total_price += order.total_price

    print(sold_list)
    context = {
        'orders': orders_list,
        'sold': sold_list,
        'date_time': date_time,
        'need_time': need_time,
        'total_price': total_price,
        'report_type': report_type
    }
    return render(request, template_name='report/report_search.html', context=context)


@login_required
def report(request, report_type):
    orders = Order.objects.all().order_by('date_time')
    date_time = datetime.now()
    need_time = ''
    sale_list = []
    total_price = 0
    day = ''

    # รับเวลาอดีตจาก ออเดอร์แรก
    if report_type == 'day':
        before = orders[0].date_time.date()
    elif report_type == 'week':
        before = str(orders[0].date_time.isocalendar()[1]) + \
            '-'+str(orders[0].date_time.year)
    elif report_type == 'month':
        before = str(orders[0].date_time.month) + \
            '-'+str(orders[0].date_time.year)
    elif report_type == 'year':
        before = orders[0].date_time.year
    b_date = orders[0].date_time

    sale_obj = {
        'date_time': '',
        'total_price': 0,
        'amount': 0,
    }

    for order in orders:
        # รับเวลาปัจจุบัน
        if report_type == 'day':
            present = order.date_time.date()
        elif report_type == 'week':
            present = str(order.date_time.isocalendar()[
                          1])+'-'+str(order.date_time.year)
        elif report_type == 'month':
            present = str(order.date_time.month)+'-'+str(order.date_time.year)
        elif report_type == 'year':
            present = order.date_time.year

        # ตัดรอบเมื่อปัจจุบันไม่ตรงกับอดีต
        if present != before:
            print(sale_obj, "test")
            sale_obj['date_time'] = b_date
            sale_obj['week_time'] = b_date.isocalendar()[1]
            sale_list.append(sale_obj)
            sale_obj = {
                'total_price': 0,
                'amount': 0,
            }

        sale_obj['total_price'] += order.total_price

        products = Product.objects.filter(order__id=order.id)
        for product in products:
            amount = Order_Product.objects.filter(
                order_id=order.id).filter(product_id=product.id)[0].amount
            sale_obj['amount'] += amount

        # ตัดรอบเมื่อเป็นออเดอร์สุดท้ายแล้วยังไม่สามารถตัดรอบจากเงื่อไขก่อนได้
        if order == orders[orders.count()-1] and present == before:
            sale_obj['date_time'] = b_date
            sale_obj['week_time'] = order.date_time.isocalendar()[1]
            #print(sale_obj, "test")
            sale_list.append(sale_obj)
            sale_obj = {
                'total_price': 0,
                'amount': 0,
            }

        before = present
        b_date = order.date_time
        sale_list.sort(key=lambda x: x['date_time'], reverse=True)
    context = {
        'sale_list': sale_list,
        'report_type': report_type,
    }
    return render(request, template_name='report/report.html', context=context)


@login_required
def report_search_day(request, day, month, year):
    orders = Order.objects.all()
    report_type = 'day'
    need_time = day
    print(orders)
    orders = Order.objects.filter(date_time__day=day).filter(
        date_time__month=month).filter(date_time__year=year)
    date_time = orders[0].date_time
    orders_list = []
    sold_list = []
    sold_temp = []
    total_price = 0
    for order in orders:
        order_obj = {}
        order_obj['detail'] = order
        products = Product.objects.filter(order__id=order.id)
        obj = []
        for product in products:
            # หาสินค้าที่ถูกสั่งตามออเดอร์
            amount = Order_Product.objects.filter(
                order_id=order.id).filter(product_id=product.id)[0].amount
            product_detail = {
                'product_detail': product,
                'amount': amount,
            }
            obj.append(product_detail)

            # รวมสินค้าทั้งหมดที่ถูกสั่ง
            sold_detail = {}
            if product not in sold_temp:
                sold_temp.append(product)
                sold_detail = {
                    'product': product,
                    'amount': amount,
                }
                sold_list.append(sold_detail)
            else:
                sold_list[sold_temp.index(product)]['amount'] += amount

        order_obj['product'] = obj
        orders_list.append(order_obj)

        total_price += order.total_price

    print(sold_list)
    context = {
        'orders': orders_list,
        'sold': sold_list,
        'date_time': date_time,
        'need_time': need_time,
        'total_price': total_price,
        'report_type': report_type
    }
    return render(request, template_name='report/report_search.html', context=context)


@login_required
def report_search_month(request, month, year):
    orders = Order.objects.all()
    report_type = 'month'
    need_time = month
    orders = Order.objects.filter(
        date_time__month=month).filter(date_time__year=year)
    date_time = orders[0].date_time
    orders_list = []
    sold_list = []
    sold_temp = []
    total_price = 0
    for order in orders:
        order_obj = {}
        order_obj['detail'] = order
        products = Product.objects.filter(order__id=order.id)
        obj = []
        for product in products:
            # หาสินค้าที่ถูกสั่งตามออเดอร์
            amount = Order_Product.objects.filter(
                order_id=order.id).filter(product_id=product.id)[0].amount
            product_detail = {
                'product_detail': product,
                'amount': amount,
            }
            obj.append(product_detail)

            # รวมสินค้าทั้งหมดที่ถูกสั่ง
            sold_detail = {}
            if product not in sold_temp:
                sold_temp.append(product)
                sold_detail = {
                    'product': product,
                    'amount': amount,
                }
                sold_list.append(sold_detail)
            else:
                sold_list[sold_temp.index(product)]['amount'] += amount

        order_obj['product'] = obj
        orders_list.append(order_obj)

        total_price += order.total_price

    
    context = {
        'orders': orders_list,
        'sold': sold_list,
        'date_time': date_time,
        'need_time': need_time,
        'total_price': total_price,
        'report_type': report_type
    }
    return render(request, template_name='report/report_search.html', context=context)


@login_required
def report_search_year(request, year):
    orders = Order.objects.all()
    report_type = 'year'
    need_time = year
    
    orders = Order.objects.filter(date_time__year=year)
    date_time = orders[0].date_time
    orders_list = []
    sold_list = []
    sold_temp = []
    total_price = 0
    for order in orders:
        order_obj = {}
        order_obj['detail'] = order
        products = Product.objects.filter(order__id=order.id)
        obj = []
        for product in products:
            # หาสินค้าที่ถูกสั่งตามออเดอร์
            amount = Order_Product.objects.filter(
                order_id=order.id).filter(product_id=product.id)[0].amount
            product_detail = {
                'product_detail': product,
                'amount': amount,
            }
            obj.append(product_detail)

            # รวมสินค้าทั้งหมดที่ถูกสั่ง
            sold_detail = {}
            if product not in sold_temp:
                sold_temp.append(product)
                sold_detail = {
                    'product': product,
                    'amount': amount,
                }
                sold_list.append(sold_detail)
            else:
                sold_list[sold_temp.index(product)]['amount'] += amount

        order_obj['product'] = obj
        orders_list.append(order_obj)

        total_price += order.total_price

    
    context = {
        'orders': orders_list,
        'sold': sold_list,
        'date_time': date_time,
        'need_time': need_time,
        'total_price': total_price,
        'report_type': report_type
    }
    return render(request, template_name='report/report_search.html', context=context)


@login_required
def report_search_week(request, year, week):
    orders = Order.objects.all()
    report_type = 'week'
    need_time = week
    
    orders = Order.objects.filter(
        date_time__year=year).filter(date_time__week=week)
    orders_list = []
    sold_list = []
    sold_temp = []
    total_price = 0
    for order in orders:
        order_obj = {}
        order_obj['detail'] = order
        date_time = order.date_time
        products = Product.objects.filter(order__id=order.id)
        obj = []
        for product in products:
            # หาสินค้าที่ถูกสั่งตามออเดอร์
            amount = Order_Product.objects.filter(
                order_id=order.id).filter(product_id=product.id)[0].amount
            product_detail = {
                'product_detail': product,
                'amount': amount,
            }
            obj.append(product_detail)

            # รวมสินค้าทั้งหมดที่ถูกสั่ง
            sold_detail = {}
            if product not in sold_temp:
                sold_temp.append(product)
                sold_detail = {
                    'product': product,
                    'amount': amount,
                }
                sold_list.append(sold_detail)
            else:
                sold_list[sold_temp.index(product)]['amount'] += amount

        order_obj['product'] = obj
        orders_list.append(order_obj)

        total_price += order.total_price

    
    context = {
        'orders': orders_list,
        'sold': sold_list,
        'date_time': date_time,
        'need_time': need_time,
        'total_price': total_price,
        'report_type': report_type
    }
    return render(request, template_name='report/report_search.html', context=context)
