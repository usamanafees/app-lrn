import django_filters
from .models import LineItem
from django.db.models import Q


class LineItemFilter(django_filters.FilterSet):
    customer_id = django_filters.NumberFilter(field_name='customer_id')
    min_kwh = django_filters.NumberFilter(field_name='kwh', lookup_expr='gte')
    max_kwh = django_filters.NumberFilter(field_name='kwh', lookup_expr='lte')

    class Meta:
        model = LineItem
        fields = ['customer_id']
    
def filter_line_items_or(queryset, query_params):
    q = Q()
    customer_id = query_params.get('customer_id')
    min_kwh = query_params.get('min_kwh')
    max_kwh = query_params.get('max_kwh')
    if customer_id is not None:
        q |= Q(customer_id=customer_id)
    if min_kwh is not None:
        q |= Q(kwh__gte=min_kwh)
    if max_kwh is not None:
        q |= Q(kwh__lte=max_kwh)
    if q:
        return queryset.filter(q)
    return queryset