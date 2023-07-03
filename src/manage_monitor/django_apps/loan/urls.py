from django.urls import path

from django_apps.loan import views

urlpatterns = [
    path('loans/add', views.AddLoanView.as_view()),
    path('loans/enable/<str:external_id>', views.ActivateLoanView.as_view()),
    path('loans/list/<str:customer_id>', views.ListLoanView.as_view()),
]