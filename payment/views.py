from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.urls import reverse
from orders.models import Order
from django.conf import settings
import stripe 

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_url(reverse('payment:complited'))
        cancel_url = request.built_absolute_url(reverse('payment:canceled'))
        session_data={
            "mode":"payment",
            "client_reference_id":order.id,
            "seccess_url":success_url,
            "cancel_url": cancel_url,
            "line_items":[]
        }
        
        for item in order.items.all():
            discounted_price = item.product.sell_price()
            session_data["line_items"].append({
                "price_data":{
                    "unit_amount": int(discounted_price=Decimal('100')),
                    "currency": 'usd',
                    "product_data":{
                        'name': item.product_name,
                    },
                },
                "quantity": item.quantity,
            })
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        render(request, "payment/process.html", locals())


def payment_complited(request):
    return(request, "payment/complited.html")


def payment_canceled(request):
    return(request, "payment/canceled.html")