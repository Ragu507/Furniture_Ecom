from rest_framework import serializers
from .models import Category,Furniture,FurnitureAttribute,FurnitureVariant,Discount

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug']

class FurnitureAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnitureAttribute
        fields = ['id', 'attribute_name', 'attribute_value']

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'discount_percentage', 'start_date', 'end_date']

class FurnitureVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnitureVariant
        fields = ['id', 'variant_name', 'variant_value']

class FurnitureCreateUpdateSerializer(serializers.ModelSerializer):
    attributes = FurnitureAttributeSerializer(many=True)
    variants = FurnitureVariantSerializer(many=True)

    class Meta:
        model = Furniture
        fields = ['id', 'name', 'description', 'price', 'category', 'stock', 'sku', 'image', 'available', 'attributes', 'variants']

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes')
        variants_data = validated_data.pop('variants')
        
        furniture = Furniture.objects.create(**validated_data)
        
        for attribute_data in attributes_data:
            FurnitureAttribute.objects.create(furniture=furniture, **attribute_data)

        for variant_data in variants_data:
            FurnitureVariant.objects.create(furniture=furniture, **variant_data)

        return furniture

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop('attributes', None)
        variants_data = validated_data.pop('variants', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if attributes_data is not None:
            instance.attributes.all().delete()  
            for attribute_data in attributes_data:
                FurnitureAttribute.objects.create(furniture=instance, **attribute_data)

        if variants_data is not None:
            instance.variants.all().delete()  
            for variant_data in variants_data:
                FurnitureVariant.objects.create(furniture=instance, **variant_data)

        return instance

class FurnitureListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    attributes = FurnitureAttributeSerializer(many=True, read_only=True)
    discounts = DiscountSerializer(many=True, read_only=True)
    variants = FurnitureVariantSerializer(many=True, read_only=True)
    effective_price = serializers.SerializerMethodField()

    class Meta:
        model = Furniture
        fields = ['id', 'name', 'description', 'price', 'effective_price', 'category', 'stock', 'sku', 'image', 'available', 'attributes', 'discounts', 'variants']

    def get_effective_price(self, obj):
        return obj.get_effective_price()
