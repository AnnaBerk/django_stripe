from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('buy/<int:item_id>/', views.CreateCheckoutSessionView.as_view(), name='buy_item'), # create a checkout session
    path('item/<int:item_id>/', views.ItemView.as_view(), name='item'),
    path('config/', views.get_stripe_config),
]