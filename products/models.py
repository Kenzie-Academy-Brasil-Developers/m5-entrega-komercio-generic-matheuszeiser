import uuid
from django.db import models
import uuid


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="products",
    )
