from django.db import connection, reset_queries
from .models import Contract


def _contracts_as_dicts(contracts):
    return [
        {
            'contract_name': contract.name,
            'customer_name': contract.customer.name,
            'meters': [m.serial_number for m in contract.meters.all()],
        }
        for contract in contracts
    ]

# Bad: load contracts → each contract.meters.all() = extra query per contract.
# Good: prefetch_related('meters') — 2 queries total, not N+1.

# Don't use select_related on M2M — it doesn't work that way.


# Note: select_related('customer') on Contract FK — still good. prefetch_related('meters') for M2M.


def get_contracts_with_meters_slow():
    reset_queries()
    contracts = list(Contract.objects.select_related('customer').all())
    result = _contracts_as_dicts(contracts)
    query_count = len(connection.queries)
    return result, query_count


def get_contracts_with_meters_fast():
    reset_queries()
    contracts = Contract.objects.select_related('customer').prefetch_related('meters').all()
    result = _contracts_as_dicts(contracts)
    query_count = len(connection.queries)
    return result, query_count