import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View

from payments.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def get_stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        item = get_object_or_404(Item, id=item_id)
        domain = "https://mysite.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": item.name},
                            "unit_amount": int(item.price*100), # convert a dollars to cents
                        },
                        "quantity": 1,
                    },
                ],
                mode='payment',
                success_url=domain + '/success/',
                cancel_url=domain + '/cancel/'
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as err:
            print(err)  # should be in loggs
            return JsonResponse({'error': str(err)})


class ItemView(TemplateView):
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        item_id = kwargs['item_id']
        item = get_object_or_404(Item, id=item_id)
        context = super(ItemView,
                        self).get_context_data(**kwargs)
        context.update({
            "item": item,
        })
        return context

# def get_item(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     context = {
#         'item': item,
#     }
#     return render(request, 'item.html', context)