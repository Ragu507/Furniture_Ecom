from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin
    )
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UtilGenericViewSet(GenericViewSet):
    
    model = None
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)
    
class BaseMixins(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    UtilGenericViewSet
):

    '''
    This common API mixin for CRUD Operation
    '''
    queryset = None
    serializer_class = None
    lookup_field = 'pk'
