from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import serializers
from django_apps.customer.models import Customer
from django_apps.loan.models import Loan
from customer.constants import Status as customer_status
from loan.constants import Status as loan_status

from . import models

class AddLoanView(APIView):
    """
    This view is used to add a new loan for the given user and return back all details of
    """

    class InputSerializer(serializers.Serializer):
        external_id = serializers.CharField(max_length=60)
        customer_id = serializers.UUIDField()
        amount = serializers.DecimalField(max_digits=12, decimal_places=2)
        outstanding = serializers.DecimalField(max_digits=12, decimal_places=2)

    class OutputSerializer(serializers.Serializer):
        external_id = serializers.CharField(max_length=60)
        customer_id = serializers.UUIDField()
        amount = serializers.DecimalField(max_digits=12, decimal_places=2)
        outstanding = serializers.DecimalField(max_digits=12, decimal_places=2)
        status = serializers.IntegerField()

    def post(self, request):
    
        current_date = timezone.now()
        tentative_maximum_payment_date = current_date + timedelta(days=2)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        customer = Customer.objects.get(id=input_serializer.data['customer_id'])

        amount = input_serializer.data['amount']

        if Decimal(amount) > customer.score:
            raise Exception("The amount of the loan can not be greater than the customer score.")

        if customer is not None and customer.status != customer_status.INACTIVE:
            loan = models.Loan(
                external_id = input_serializer.data['external_id'],
                customer_id = customer,
                amount = input_serializer.data['amount'],
                outstanding = input_serializer.data['outstanding'],
                maximum_payment_date = tentative_maximum_payment_date,
            )

            loan.save()
        else:
            raise Exception(f"The loan with id {input_serializer.data['customer_id']} does not exist or is Inactive")

        output_data = self.OutputSerializer(loan).data

        return Response(output_data, status=status.HTTP_201_CREATED)
    
    
class ActivateLoanView(APIView):
    """
    This view will activate a Loan by setting its `status` to active
    """

    current_date = timezone.now()

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        external_id = serializers.CharField()
        status = serializers.IntegerField()
        taken_at = serializers.DateTimeField()

    def patch(self, request, external_id):
        loan = get_object_or_404(Loan, external_id=external_id)
        loan.status = loan_status.ACTIVE
        loan.taken_at = self.current_date
        loan.save()

        output_data = self.OutputSerializer(loan).data

        return Response(output_data, status=status.HTTP_200_OK)
        

class ListLoanView(generics.ListAPIView):
    """
    This view returns a list of loans for the given user or all users
    """

    class OutputSerializer(serializers.Serializer):
        external_id = serializers.CharField(max_length=60)
        customer_id = serializers.UUIDField()
        amount = serializers.DecimalField(max_digits=12, decimal_places=2)
        outstanding = serializers.DecimalField(max_digits=12, decimal_places=2)
        status = serializers.IntegerField()

    serializer_class = OutputSerializer
    
    def get_queryset(self):

        customer_id = self.kwargs.get('customer_id')
        customer = Customer.objects.get(id=customer_id)

        if customer is not None:
            queryset = Loan.objects.filter(customer_id=customer_id)
        return queryset
        

