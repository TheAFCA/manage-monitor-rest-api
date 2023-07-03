from django.urls import path

from django_apps.customer import views

urlpatterns = [
    path('customers/add', views.AddCustomerView.as_view()),
    path('customers/enable/<str:external_id>', views.ActivateCustomerView.as_view()),
    path('customers/list', views.ListCustomerView.as_view()),
    path('customers/list/<str:external_id>', views.ListCustomerView.as_view()),
]