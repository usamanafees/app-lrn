from django.db import models
from customers.models import Customer
# Create your models here.


class LineItem(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='line_items',
    )    
    kwh = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
            return f"{self.customer_id} - {self.kwh} kWh at {self.rate} cents/kWh"
    @property
    def total(self):
        return self.kwh * self.rate
