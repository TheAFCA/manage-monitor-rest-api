from django.urls import path

from django_apps.payment import views

urlpatterns = [
    path('payments/add', views.AddPaymentView.as_view()),
    path('payments/list/<uuid:customer_id>', views.ListPaymentView.as_view())
]