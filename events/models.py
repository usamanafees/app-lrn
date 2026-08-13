from django.db import models

from customers.models import Customer
# Create your models here.

class UsageEvent(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='usage_events'
    )
    kwh = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'timestamp'],
                name = 'unique_usage_event_customer_timestamp',

            ),
            models.CheckConstraint(
                condition=models.Q(kwh__gte=0),
                name= 'usage_event_kwh_non_negative'
            )
        ]
        indexes = [
        models.Index(fields=['timestamp'], name='idx_usage_event_timestamp'),
        models.Index(fields=['customer'], name='idx_usage_event_customer'),
        ]
    def __str__(self):
        return f'{self.customer_id} - {self.kwh} kwh at {self.timestamp}'