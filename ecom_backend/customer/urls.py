from .views.customer_view import CustomerViewSet
from .views.shipping_address_view import ShippingAddressView
from django.urls import path,include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet,basename = 'customers')
router.register(r'shipping-addresses', ShippingAddressView, basename ='shipping-addresses')

urlpatterns =[
    path('',include(router.urls),)
]