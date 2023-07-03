# Generated by Django 4.2.2 on 2023-07-03 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_alter_loan_amount_alter_loan_outstanding'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetail',
            name='loan_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan', to='loan.loan'),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='payment_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='payment.payment'),
        ),
    ]