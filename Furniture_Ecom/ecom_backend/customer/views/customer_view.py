from ..models import Customer
from ..serializer.customer_serializer import (
    CustomerListSerializer,
    CustomerCreateSerializer,
    CustomerUpdateSerializer
)
from ..serializer.none_serializer import NoneSerializer
from ..base_mixins import BaseMixins
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout,login


class CustomerViewSet(BaseMixins):
    queryset = Customer.objects.all()
    serializer_dict = {
        'list': CustomerListSerializer,
        'create': CustomerCreateSerializer,
        'update': CustomerUpdateSerializer,
        'retrieve': CustomerListSerializer
    }

    def get_serializer_class(self):
        """
        Determines which serializer to use based on the action (list, create, update, etc.).
        Falls back to NoneSerializer if the action is not recognized.
        """
        return self.serializer_dict.get(self.action, NoneSerializer)
    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()
    
    def get_queryset(self):
        """
        Overrides the default queryset to allow customers to see only their own customers.
        Admins can see all customers.
        """
        if self.request.user.is_staff:
            return Customer.objects.all()  
        return Customer.objects.filter(id=self.request.user.id) 
    
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
            # If prefetching was done for the instance, invalidate the prefetch cache
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
        Handles listing all customer instances.
        The list is paginated and uses the list serializer to return the data.
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
    
    @action(detail=False, methods=['post'], url_path='login', authentication_classes=[], permission_classes=[])
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'], url_path='logout')
    def logout_view(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
