from django.db import models

# Create your models here.


class LineItem(models.Model):
    customer_id = models.IntegerField()
    kwh = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add = True)

    @property
    def total(self):
        return self.kwh * self.rate
