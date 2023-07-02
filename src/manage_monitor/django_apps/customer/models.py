import uuid
from datetime import datetime
from django.db import models
from customer.constants import Status


class Customer(models.Model):
    """Customer model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=12, unique=True)
    status = models.SmallIntegerField(default=Status.INACTIVE)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField()
