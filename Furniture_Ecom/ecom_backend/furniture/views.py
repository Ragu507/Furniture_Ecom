from django.shortcuts import render
from customer.base_mixins import BaseMixins
from .models import Furniture,FurnitureAttribute,FurnitureVariant,Discount,Category
from .serializer import (
    FurnitureListSerializer,
    FurnitureCreateUpdateSerializer,
    DiscountSerializer,
    CategorySerializer
)
from customer.serializer.none_serializer import NoneSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action

class FurnitureView(BaseMixins):
    queryset = Furniture.objects.prefetch_related('discounts').all()
    serializer_dict = {
        'list': FurnitureListSerializer,
        'create': FurnitureCreateUpdateSerializer,
        'update': FurnitureCreateUpdateSerializer,
        'retrieve': FurnitureListSerializer
    }

    def get_serializer_class(self):
        """
        Determines which serializer to use based on the action (list, create, update, etc.).
        Falls back to NoneSerializer if the action is not recognized.
        """
        return self.serializer_dict.get(self.action, NoneSerializer)
    
    def get_permissions(self):
        """
        Restricts 'create', 'update', and 'destroy' actions to admin users only.
        """
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        """
        Handles the create logic with CSRF exempt.
        After creating the customer, it returns the serialized data in the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handles the update logic.
        Fetches the customer object by primary key and applies the update using the UpdateSerializer.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Handles retrieving a single customer instance based on the primary key.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Handles listing all furniture instances with infinite scrolling.
        This method does not use pagination and returns the data as per the client scrolling.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))

        queryset = queryset[offset:offset+limit]
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "results": serializer.data,
            "next_offset": offset + limit,
            "has_more": queryset.count() > limit  
        })

    def destroy(self, request, *args, **kwargs):
        """
        Handles deleting a customer instance based on the primary key.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='create-discount', permission_classes=[IsAdminUser])
    def create_discount(self, request, pk=None):
        """
        Handles the creation of a discount for a specific furniture item.
        Only admin users are allowed to create discounts.
        """
        furniture = self.get_object()  
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(furniture=furniture)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryView(BaseMixins):
    queryset = Category.objects.all()
    serializer_dict = {
        'list': CategorySerializer,
        'create': CategorySerializer,
        'update': CategorySerializer,
        'retrieve': CategorySerializer
    }

    def get_serializer_class(self):
        """
        Determines which serializer to use based on the action (list, create, update, etc.).
        Falls back to NoneSerializer if the action is not recognized.
        """
        return self.serializer_dict.get(self.action, NoneSerializer)
    
    def get_permissions(self):
        """
        Restricts 'create', 'update', and 'destroy' actions to admin users only.
        """
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        """
        Handles the create logic with CSRF exempt.
        After creating the customer, it returns the serialized data in the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handles the update logic.
        Fetches the customer object by primary key and applies the update using the UpdateSerializer.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Handles retrieving a single customer instance based on the primary key.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Lists all shipping addresses for the current user, with pagination.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Handles deleting a customer instance based on the primary key.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)





