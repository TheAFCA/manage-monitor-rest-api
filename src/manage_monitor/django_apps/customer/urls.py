from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('customer', views.CustomerViewSet, basename='myCustomer')

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls))
]