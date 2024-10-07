from django.shortcuts import render
from customer.base_mixins import BaseMixins
from customer.serializer.none_serializer import NoneSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import action
from .serializers import (
    InteriorDesignProjectSerializer,
    InteriorDesignProjectCreateUpdateSerializer,
    DesignCategorySerializer,
    DesignImageSerializer,
    RoomTypeSerializer,
    InteriorRoomSerializer,
    ServicePackageSerializer,
    BookingSerializer,
    InteriorRoomCreateUpdateSerializer,
    DesignImageCreateUpdateSerializer,
    DesignCategoryCreateUpdateSerializer,
    ServicePackageCreateUpdateSerializer,
    BookingCreateUpdateSerializer   
)
from .models import (
    InteriorDesignProject,
    DesignCategory,
    DesignImage,
    RoomType,
    InteriorRoom,
    ServicePackage,
    Booking
)

class InteriorDesignProjectView(BaseMixins):
    queryset = InteriorDesignProject.objects.all()
    serializer_dict = {
        'list': InteriorDesignProjectSerializer,
        'create': InteriorDesignProjectCreateUpdateSerializer,
        'update': InteriorDesignProjectCreateUpdateSerializer,
        'retrieve': InteriorDesignProjectSerializer,
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
    
    def create(self, request, *args, **kwargs):
        """
        Handles the create logic.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handles the update logic.
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
        Handles retrieving a single project instance based on the primary key.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Handles listing all project instances with infinite scrolling.
        This method does not use pagination but returns the data as per the client scrolling.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))

        has_more = queryset[offset+limit:].exists()
        queryset = queryset[offset:offset + limit]

        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "results": serializer.data,
            "next_offset": offset + limit,
            "has_more": has_more
        })

    def destroy(self, request, *args, **kwargs):
        """
        Handles deleting a project instance based on the primary key.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DesignCategoryView(BaseMixins):
    queryset = DesignCategory.objects.all()
    serializer_dict = {
        'list': DesignCategorySerializer,
        'create': DesignCategoryCreateUpdateSerializer,
        'update': DesignCategoryCreateUpdateSerializer,
        'retrieve': DesignCategorySerializer,
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
    
    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a DesignCategory.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handles updating an existing DesignCategory.
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
        Handles retrieving a single DesignCategory by its ID.
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
        Handles deleting a DesignCategory.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ServicePackageView(BaseMixins):
    queryset = ServicePackage.objects.all()
    serializer_dict = {
        'list': ServicePackageSerializer,
        'create': ServicePackageCreateUpdateSerializer,
        'update': ServicePackageCreateUpdateSerializer,
        'retrieve': ServicePackageSerializer,
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

    def create(self, request, *args, **kwargs):
        """
        Handles creating a ServicePackage.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handles updating an existing ServicePackage.
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
        Handles retrieving a single ServicePackage by its ID.
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
        Handles deleting a ServicePackage.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BookingView(BaseMixins):
    queryset = Booking.objects.all()
    serializer_dict = {
        'list': BookingSerializer,
        'create': BookingCreateUpdateSerializer,
        'update': BookingCreateUpdateSerializer,
        'retrieve': BookingSerializer,
    }

    def get_serializer_class(self):
        """
        Determines which serializer to use based on the action (list, create, update, etc.).
        Falls back to NoneSerializer if the action is not recognized.
        """
        return self.serializer_dict.get(self.action, NoneSerializer)

    def get_permissions(self):
        """
        Grants access to authenticated users for creating, updating, and viewing their own bookings.
        Only admin users can list or delete all bookings.
        """
        if self.action in ['destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """
        Overrides the default queryset to allow customers to see only their own bookings.
        Admins can see all bookings.
        """
        if self.request.user.is_staff:
            return Booking.objects.all()  
        return Booking.objects.filter(customer=self.request.user)  

    def create(self, request, *args, **kwargs):
        """
        Handles creating a new Booking.
        Automatically assigns the authenticated user as the customer for the booking.
        """
        data = request.data.copy()
        data['customer'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handles updating a booking.
        Only the customer who created the booking or an admin can update it.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.customer != request.user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to edit this booking."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Handles retrieving a single booking instance.
        Customers can only retrieve their own bookings, while admins can retrieve any booking.
        """
        instance = self.get_object()
        if instance.customer != request.user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to view this booking."}, status=status.HTTP_403_FORBIDDEN)
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
        Handles deleting a booking.
        Only the customer who created the booking or an admin can delete it.
        """
        instance = self.get_object()

        if instance.customer != request.user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to delete this booking."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

