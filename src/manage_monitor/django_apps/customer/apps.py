from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    #name = 'customer'
    name = 'django_apps.customer'
    verbose_name = 'Customer'
