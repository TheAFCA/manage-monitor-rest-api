import uuid
from django.db import models
from customer.models import Customer

class Payment(models.Model):
    """Payment model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=12, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.SmallIntegerField()
    paid_at = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

class PaymentDetail(models.Model):
    """PaymentDetail model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_id = models.UUIDField()
    payment_id = models.OneToOneField(Payment, on_delete=models.CASCADE)
