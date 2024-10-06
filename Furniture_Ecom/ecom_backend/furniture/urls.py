from django.urls import path,include
from rest_framework import routers
from .views import FurnitureView,CategoryView

router = routers.DefaultRouter()
router.register(r'furniture', FurnitureView, basename='furniture')
router.register(r'categories', CategoryView, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]