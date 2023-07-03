import uuid
from django.db import models
from customer.constants import Status
from django.core.validators import MinValueValidator


class Customer(models.Model):
    """
    Model for storing customers data and their scores
    Attributes:
        external_id: costomer identifier given by the admin
        status: ACTIVE = 1 | INACTIVE = 2
        score: maximum amount available to be lended to the customer.
        preapproved_at : datetime when a request is approved automatically without human intervention
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField(default=Status.INACTIVE)
    score = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    preapproved_at = models.DateTimeField()

    class Meta:
        db_table = "customer"
