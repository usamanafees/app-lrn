from django.contrib import admin
from .models import Meter, Contract, ContractMeter



admin.site.register(Meter)
admin.site.register(Contract)
admin.site.register(ContractMeter)