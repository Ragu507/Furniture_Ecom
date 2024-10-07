from ..base_mixins import BaseMixins
from ..models import ShippingAddress
from ..serializer.shipping_address_serializer import (
    ShippingAddressCreateSerializer,
    ShippingAddressUpdateSerializer,
    ShippingAddressListSerializer
)
from ..serializer.none_serializer import NoneSerializer
from rest_framework.response import Response
from rest_framework import status

class ShippingAddressView(BaseMixins):
    queryset = ShippingAddress.objects.all()
    serializer_dict = {
        'list': ShippingAddressListSerializer,
        'create': ShippingAddressCreateSerializer,
        'update': ShippingAddressUpdateSerializer,
        'retrieve': ShippingAddressListSerializer
    }
    
    def get_serializer_class(self):
        """
        Determines which serializer to use based on the action (list, create, update, etc.).
        Falls back to NoneSerializer if the action is not recognized.
        """
        return self.serializer_dict.get(self.action, NoneSerializer)
    
    def get_queryset(self):
        """
        Overrides the default queryset to allow customers to see only their own shipping address.
        Admins can see all shipping address.
        """
        if self.request.user.is_staff:
            return ShippingAddress.objects.all()  
        return ShippingAddress.objects.filter(customer=self.request.user) 
    
    def perform_create(self, serializer):
        """
        Sets the customer as the currently authenticated user before saving.
        """
        serializer.save(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Handles the create logic. 
        This method doesn't need the csrf_exempt decorator if you're using Token or JWT authentication.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handles update logic for the shipping address.
        DRF automatically handles full and partial updates based on the HTTP method (PUT/PATCH).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single shipping address instance.
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
        Deletes a shipping address.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
