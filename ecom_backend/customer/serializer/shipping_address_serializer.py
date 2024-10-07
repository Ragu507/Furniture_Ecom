from ..models import ShippingAddress
from rest_framework import serializers
from .customer_serializer import CustomerListSerializer

class ShippingAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country']

class ShippingAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country']

class ShippingAddressListSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()  

    class Meta:
        model = ShippingAddress
        fields = ['id', 'customer', 'address_line1', 'address_line2','city', 'state', 'zip_code', 'country']
