from ..models import Cart,CartItem
from rest_framework import serializers
from .customer_serializer import CustomerListSerializer

class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['customer', 'total_amount']

class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['total_amount']

class CartListSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()  

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'total_amount']


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'furniture', 'quantity', 'price']

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', 'price']

class CartItemListSerializer(serializers.ModelSerializer):
    cart = CartListSerializer()  
    furniture = FurnitureListSerializer()  
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'furniture', 'quantity', 'price', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


