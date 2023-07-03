import uuid
from django.db import models
from django.core.validators import MinValueValidator

from loan.constants import Status
from django_apps.customer.models import Customer

class Loan(models.Model):
    """
    Model to represent a loan 
    Attributes:
        external_id: loan identifier given by the admin
        amount: quantity of money that was lend to the customer
        status: PENDING = 1 |ACTIVE = 2 | REJECTED = 3 | PAID = 4
        outstanding: Pending amount for being paid
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.SmallIntegerField(default=Status.PENDING)
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField(null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        db_table = "loan"
