from rest_framework import serializers

from . import models

class HelloSerializers(serializers.Serializer):
    """Serializes a name field for testing our APIView"""

    name = serializers.CharField(max_length=10)

class CustomerSerializers(serializers.ModelSerializer):
    """A serializers for customer object."""

    class Meta:
        model = models.Customer
        fields = ('id','created_at','updated_at','external_id','status','score','preapproved_at')
    
    def create(self, validated_data):
        """Create and return a new customer."""

        customer = models.Customer(
            external_id=validated_data['external_id'],
            status=validated_data['status'],
            score=validated_data['score'],
            preapproved_at=validated_data['preapproved_at']
        )

        customer.save()

        return customer

