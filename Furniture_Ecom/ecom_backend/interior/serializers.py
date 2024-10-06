from rest_framework import serializers
from .models import (
    DesignCategory, 
    InteriorDesignProject, 
    DesignImage, 
    RoomType, 
    InteriorRoom, 
    ServicePackage, 
    Booking
)
from customer.serializer.customer_serializer import CustomerListSerializer

class DesignCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignCategory
        fields = ['id', 'name', 'description', 'slug']

class DesignCategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignCategory
        fields = ['name', 'description', 'slug']

class DesignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignImage
        fields = ['id', 'image', 'description']

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'description']

class InteriorRoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer()

    class Meta:
        model = InteriorRoom
        fields = ['id', 'room_type', 'dimensions', 'design_description']

class InteriorRoomCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteriorRoom
        fields = ['room_type', 'dimensions', 'design_description']

class DesignImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignImage
        fields = ['image', 'description']

class InteriorDesignProjectSerializer(serializers.ModelSerializer):
    category = DesignCategorySerializer()
    rooms = InteriorRoomSerializer(many=True)
    images = DesignImageSerializer(many=True)

    class Meta:
        model = InteriorDesignProject
        fields = ['id', 'name', 'description', 'category', 'budget', 'rooms', 'images']

class InteriorDesignProjectCreateUpdateSerializer(serializers.ModelSerializer):
    rooms = InteriorRoomCreateUpdateSerializer(many=True)
    images = DesignImageCreateUpdateSerializer(many=True)

    class Meta:
        model = InteriorDesignProject
        fields = ['name', 'description', 'category', 'budget', 'rooms', 'images']

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms')
        images_data = validated_data.pop('images')

        project = InteriorDesignProject.objects.create(**validated_data)

        for room_data in rooms_data:
            InteriorRoom.objects.create(project=project, **room_data)

        for image_data in images_data:
            DesignImage.objects.create(project=project, **image_data)

        return project

    def update(self, instance, validated_data):
        rooms_data = validated_data.pop('rooms', None)
        images_data = validated_data.pop('images', None)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.budget = validated_data.get('budget', instance.budget)
        instance.save()

        if rooms_data:
            instance.rooms.all().delete()  
            for room_data in rooms_data:
                InteriorRoom.objects.create(project=instance, **room_data)

        if images_data:
            instance.images.all().delete()  
            for image_data in images_data:
                DesignImage.objects.create(project=instance, **image_data)

        return instance

class ServicePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePackage
        fields = ['id', 'name', 'description', 'price', 'features']

class ServicePackageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePackage
        fields = ['id', 'name', 'description', 'price', 'features']

class BookingSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()
    service_package = ServicePackageSerializer()
    project = InteriorDesignProjectSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'service_package', 'project', 'booking_date', 'status']

class BookingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer', 'service_package', 'project', 'booking_date', 'status']
        

