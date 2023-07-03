import uuid
from django.db import models
from django_apps.customer.models import Customer
from django_apps.loan.models import Loan
from payment.constants import Status
from django.core.validators import MinValueValidator

class Payment(models.Model):
    """
    This is the main table for storing all payments made by customers to loans in our system.
    Attributes:
        external_id: payment identifier given by the admin
        total_amount: corresponding amount of the given payment
        status: COMPLETED = 1 | REJECTED = 2 | PENDING = 3
        paid_at (optional field): date when a particular transaction was completed successfully
        customer_id : foreign key reference from Customers Table
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10, validators=[MinValueValidator(0)])
    status = models.SmallIntegerField(default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = "payment"

class PaymentDetail(models.Model):
    """
    A detail model that stores information about each individual installment or principal payable towards
    Attributes:
        amount: Processed amount for a expecific loan (one payment may modify more than one loan)
        loan_id: Foreign Key Reference from Loan Model
        payment_id: One-to-One relationship with Payments Table
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="loan")
    payment_id = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="payment")

    class Meta:
        db_table = "paymentdetail"
