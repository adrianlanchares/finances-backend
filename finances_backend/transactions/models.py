from django.db import models
from django.utils import timezone


# Create your models here.
class Transaction(models.Model):
    """Represents a financial transaction.

    Args:
        models (Model): Django model base class.
    """

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transaction {self.id}: {self.description} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
