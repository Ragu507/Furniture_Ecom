from ..models import Order,OrderItem
from rest_framework import serializers
from .shipping_address_serializer import ShippingAddressListSerializer
from .customer_serializer import CustomerListSerializer

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'total_price', 'status', 'shipping_address']

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['total_price', 'status']

class OrderListSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()  
    shipping_address = ShippingAddressListSerializer()  

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_price', 'status', 'shipping_address']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'furniture', 'quantity', 'price']

class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'price']

class OrderItemListSerializer(serializers.ModelSerializer):
    order = OrderListSerializer()  
    furniture = FurnitureListSerializer()  
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'furniture', 'quantity', 'price', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

