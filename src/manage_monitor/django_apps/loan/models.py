import uuid
from django.db import models

from loan.constants import Status
from customer.models import Customer

class Loan(models.Model):
    """Loan model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=12, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(default=Status.PENDING)
    maximum_payment = models.DateTimeField()
    taken_at = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
