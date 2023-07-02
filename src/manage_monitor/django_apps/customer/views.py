from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import models

class HelloApiView(APIView):
    """Test Api View."""

    serializer_class = serializers.HelloSerializers

    def get(self, request, format=None):
        """Returns a list of api view features"""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a tadicional Django',
            'Gives you the most control over your application logic'
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
    
    def post(self, request):
        """Create hello message with our name"""

        serializer = serializers.HelloSerializers(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CustomerViewSet(viewsets.ModelViewSet):
    """Handles creating, creating and active customer."""

    serializer_class = serializers.CustomerSerializers
    queryset = models.Customer.objects.all()