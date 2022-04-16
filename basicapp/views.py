import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt

from api_keys import *

stripe.api_key = STRIPE_SEC_KEY


def index2(request):
    return render(request, 'basicapp/checkout.html')


@csrf_exempt
def checkout(request):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 2000,
                    'product_data': {
                        'name': 'Stubborn Attachments',
                        'images': ['https://i.imgur.com/EHyR2nP.png'],
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('basicapp:checkout_done')),
        cancel_url=request.build_absolute_uri(reverse('basicapp:index2')),
    )
    return JsonResponse({'id': checkout_session.id})


def index(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        customer = stripe.Customer.create(
            email=request.POST.get('email'),
            name=request.POST.get('name'),
            source=request.POST.get('stripeToken')
        )

        charge = stripe.Charge.create(
            amount=amount * 100,
            currency='usd',
            description='Donation',
            customer=customer,
        )
        return redirect('basicapp:checkout_done')
    return render(request, 'basicapp/index.html')


def checkout_done(request):
    return render(request, 'basicapp/success.html')
