from django.urls import path,include
from rest_framework import routers
from .views import (
    InteriorDesignProjectView,DesignCategoryView,ServicePackageView,BookingView
)

router = routers.DefaultRouter()
router.register(r'projects', InteriorDesignProjectView, basename='projects')
router.register(r'categories', DesignCategoryView, basename='categories')
router.register(r'service-packages', ServicePackageView, basename='service-packages')
router.register(r'bookings', BookingView, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]