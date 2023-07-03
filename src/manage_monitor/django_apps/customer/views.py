from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import serializers
from django_apps.customer.models import Customer
from typing import Optional
from customer.constants import Status as customer_status


from . import models

class AddCustomerView(APIView):
    class InputSerializer(serializers.Serializer):
        external_id = serializers.CharField(max_length=60)
        score = serializers.DecimalField(max_digits=12, decimal_places=2)
        preapproved_at = serializers.DateTimeField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()

    def post(self, request):
    
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        import pdb
        pdb.set_trace()
    
        customer = models.Customer(
            external_id = input_serializer.data['external_id'],
            score = input_serializer.data['score'],
            preapproved_at = input_serializer.data['preapproved_at']
        )

        customer.save()

        output_data = self.OutputSerializer(customer).data

        return Response(output_data, status=status.HTTP_201_CREATED)
    
class ActivateCustomerView(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        external_id = serializers.CharField()
        status = serializers.IntegerField()

    def patch(self, request, external_id):
        customer = get_object_or_404(Customer, external_id=external_id)
        customer.status = customer_status.ACTIVE
        customer.save()

        output_data = self.OutputSerializer(customer).data

        return Response(output_data, status=status.HTTP_200_OK)
        

class ListCustomerView(generics.ListAPIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        external_id = serializers.CharField(max_length=60)
        status = serializers.IntegerField()
        score = serializers.DecimalField(max_digits=12, decimal_places=2)
        preapproved_at = serializers.DateTimeField()

    serializer_class = OutputSerializer
    def get_queryset(self, external_id: Optional[str] = None):
        queryset = Customer.objects.all()
        if self.kwargs.get('external_id') is not None:
            queryset = queryset.filter(external_id=self.kwargs['external_id'])
        return queryset
        
