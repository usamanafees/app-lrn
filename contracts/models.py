from django.db import models
from customers.models import Customer


class Meter(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.serial_number


class Contract(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contracts')
    name = models.CharField(max_length=255)
    meters = models.ManyToManyField(
        Meter,
        through='ContractMeter',
        related_name='contracts',
    )

    def __str__(self):
        return self.name


class ContractMeter(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    start_date = models.DateField()
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = [['contract', 'meter']]

    def __str__(self):
        return f"{self.contract.name} — {self.meter.serial_number}"