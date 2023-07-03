from decimal import Decimal
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import serializers
from django_apps.customer.models import Customer
from django_apps.loan.models import Loan
from django_apps.payment.models import PaymentDetail
from customer.constants import Status as customer_status
from loan.constants import Status as loan_status
from payment.constants import Status as payment_status

from . import models

class AddPaymentView(APIView):
    """
    This view allows adding new payments for customers' loans in our system
    """

    class InputSerializer(serializers.Serializer):
        external_id = serializers.CharField(max_length=60)
        total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
        customer_id = serializers.UUIDField()

    class OutputSerializer(serializers.Serializer):
        external_id = serializers.CharField(max_length=60)
        customer_id = serializers.UUIDField()

    def post(self, request):
    
        current_date = timezone.now()

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        customer = Customer.objects.get(id=input_serializer.data['customer_id'])
        loans = Loan.objects.filter(customer_id=customer.id).order_by('created_at')

        if customer is not None and len(loans) == 0:
            raise Exception("There is not a customer or a loan associated to the given paymnet.")

        if customer.status != customer_status.ACTIVE:
            raise Exception("The customer has not being activated.")
        
        payment = models.Payment(
            external_id = input_serializer.data['external_id'],
            total_amount = input_serializer.data['total_amount'],
            status = payment_status.PENDING,
            paid_at = current_date,
            customer_id = customer,
        )

        payment.save()


        total_amount = input_serializer.data['total_amount']

        remaining_amount = Decimal(total_amount)

        for i in range(len(loans)):
            loan = loans[i]
            outstanding_result = loan.outstanding - remaining_amount
            
            if loan.status != loan_status.ACTIVE:
                break
            elif outstanding_result <= 0:
                loan.outstanding = 0
                loan.status = loan_status.PAID
                remaining_amount = abs(outstanding_result)
                loan.save()
                payment_details = models.PaymentDetail(
                    amount = remaining_amount,
                    loan_id = loan,
                    payment_id = payment,
                )
                payment_details.save()
            else:
                loan.outstanding = outstanding_result
                loan.save()
                payment_details = models.PaymentDetail(
                    amount = remaining_amount,
                    loan_id = loan,
                    payment_id = payment,
                )
                payment_details.save()
                break   
        
        payment.status = payment_status.COMPLETED
        payment.save()

        output_data = self.OutputSerializer(payment).data

        return Response(output_data, status=status.HTTP_201_CREATED)
    
class ListPaymentView(generics.ListAPIView):
    """
    This view returns a list of all payments made by the user for their loans
    """

    class OutputSerializer(serializers.Serializer):
        external_id = serializers.CharField(max_length=60)
        customer_external_id = serializers.CharField()
        loan_external_id = serializers.CharField()
        payment_date = serializers.DateTimeField(),
        status = serializers.IntegerField(),
        total_amount = serializers.DecimalField(max_digits=12, decimal_places=2),
        payment_amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    serializer_class = OutputSerializer
    
    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')

        queryset = PaymentDetail.objects.filter(payment_id__customer_id=customer_id).select_related(
        'payment_id', 'loan_id', 'payment_id__customer_id'
        ).annotate(
            external_id=F('payment_id__external_id'),
            customer_external_id=F('payment_id__customer_id__external_id'),
            loan_external_id=F('loan_id__external_id'),
            payment_date=F('payment_id__created_at'),
            status=F('payment_id__status'),
            total_amount=F('payment_id__total_amount'),
            payment_amount=F('payment_id__total_amount'),
        ).values(
            'external_id',
            'customer_external_id',
            'loan_external_id',
            'payment_date',
            'status',
            'amount',
            'total_amount',
            'payment_amount',
        )

        return queryset
