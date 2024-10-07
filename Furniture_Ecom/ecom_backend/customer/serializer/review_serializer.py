from ..models import Review
from rest_framework import serializers

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['customer', 'furniture', 'rating', 'comment']

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class ReviewListSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()  
    furniture = FurnitureListSerializer()  
    class Meta:
        model = Review
        fields = ['id', 'customer', 'furniture', 'rating', 'comment']


