import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import View

from payments.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def get_stripe_config(request, slug):
    """ Return public key depends on items' currency."""
    if request.method == 'GET':
        if slug == 'EUR':
            stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
            #stripe не дает на 1 аккаунт создать 2 пары, поэтому это только пример
        if slug == 'USD':
            stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class CreateCheckoutSessionView(View):
    """ View for creating stripe payment."""
    def get(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        item = get_object_or_404(Item, id=item_id)
        domain = "http://130.193.52.110:8082" # here must be actual domain
        if settings.DEBUG:
            domain = "http://127.0.0.1:8082"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        "price_data": {
                            "currency": item.currency,
                            "product_data": {"name": item.name},
                            "unit_amount": int(item.price * 100),  # convert dollars into cents
                        },
                        "quantity": 1,
                    },
                ],
                mode='payment',
                success_url=f'{domain}/payment_success/',
                cancel_url=f'{domain}/payment_failed/',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as err:
            print(err)  # should be in logs
            return JsonResponse({'error': str(err)})


class ItemView(View):
    """ View for item."""
    template_name = 'item.html'

    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        return render(request, self.template_name, {'item': item})


class ItemListView(ListView):
    """ View for all items."""
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'
