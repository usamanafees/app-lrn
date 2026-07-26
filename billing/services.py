from .models import LineItem
from django.db import connection, reset_queries
from django.db.models import Sum, F

def calculate_customer_total(customer_id):
    items = LineItem.objects.filter(customer_id=customer_id)
    total = sum(item.total for item in items)
    return total

def _line_items_as_dicts(items):
    return [
        {
            'id': item.id,
            'customer_name': item.customer.name,
            'kwh': str(item.kwh),
        }
        for item in items
    ]

def get_line_items_with_customer_slow():
    reset_queries()
    items = list(LineItem.objects.all())
    result = _line_items_as_dicts(items)
    query_count = len(connection.queries)
    return result, query_count

def get_line_items_with_customer_fast():
    reset_queries()
    items = LineItem.objects.select_related('customer').all()
    result = _line_items_as_dicts(items)
    query_count = len(connection.queries)
    return result, query_count

def calculate_customer_total_slow(customer_id):
    reset_queries()
    items = LineItem.objects.filter(customer_id=customer_id)
    total = sum(item.total for item in items)
    query_count = len(connection.queries)
    return total, query_count

def calculate_customer_total_fast(customer_id):
    reset_queries()
    result = LineItem.objects.filter(customer_id=customer_id).aggregate(
        total=Sum(F('kwh') * F('rate'))
    )
    total = result['total'] or 0
    query_count = len(connection.queries)
    return total, query_count

def calculate_customer_total_raw_sql(customer_id):
    reset_queries()
    rows = LineItem.objects.raw(
        '''
        SELECT id, customer_id, kwh, rate, created_at
        FROM billing_lineitem
        WHERE customer_id = %s
        ''',
        [customer_id],
    )
    total = sum(row.kwh * row.rate for row in rows)
    query_count = len(connection.queries)
    return total, query_count

# Fixed	Yours
# .raw()
# Fixed Django method
# %s
# Fixed placeholder (safe)
# [customer_id]
# Yours — params list
# table name billing_lineitem
# Django default — yours to verify

#     Interview line
# "N+1 happens when you loop related objects without select_related. For FK/O2O I use select_related; for M2M/reverse FK I use prefetch_related."