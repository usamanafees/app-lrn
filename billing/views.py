from rest_framework import viewsets          # fixed — DRF import
from .models import LineItem                 # fixed pattern — your model name
from .serializers import (  
    LineItemSerializer, 
    CustomerTotalInputSerializer, 
    CustomerTotalOutputSerializer
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.views import APIView
from .services import calculate_customer_total, calculate_customer_total_fast, calculate_customer_total_raw_sql, calculate_customer_total_slow, get_line_items_with_customer_fast, get_line_items_with_customer_slow
from .filters import LineItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import LineItemFilter, filter_line_items_or
from rest_framework.permissions import AllowAny

class LineItemViewSet(viewsets.ModelViewSet): # LineItemViewSet = yours | ModelViewSet = fixed DRF base
    queryset = LineItem.objects.all()         # queryset = fixed attr name | LineItem = yours
    serializer_class = LineItemSerializer     # serializer_class = fixed | LineItemSerializer = yours
    filterset_class = LineItemFilter
    filter_backends = [DjangoFilterBackend]
    # django-filter handles that now. No need for self.action == 'list' guard — django-filter only 
    # runs on list by default via filter_queryset.
   
   
    # def get_queryset(self):                   # get_queryset = fixed DRF hook name
    #     queryset = super().get_queryset()
    #     customer_id = self.request.query_params.get('customer_id')
    #     # self = fixed
    #     # request = fixed (HTTP request)
    #     # query_params = fixed (DRF, reads ?key=value)
    #     # 'customer_id' = yours (query param name)
    #     # customer_id = yours (local variable)
    #     if self.action == 'list' and customer_id is not None:
    #         queryset = queryset.filter(customer_id=customer_id)
    #         # filter = fixed Django ORM method
    #         # customer_id=customer_id → left = model field (yours) | right = value (yours)
    #     return queryset  

    def retrieve(self, request, *args, **kwargs): # why is it not self.action == 'retrieve' in get_queryset
        # customer_id = kwargs['pk']   # fixed: kwargs, 'pk' | 1 from URL
        # item = LineItem.objects.filter(id=customer_id).first()
        id_ = kwargs['pk']
        item = LineItem.objects.filter(id=id_).first()
        if item is None:
            raise NotFound()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # kwh = serializer.validated_data['kwh']
        # if kwh < 0:
        #     raise ValidationError({'kwh': 'kwh cannot be negative'})
        serializer.save()

    def perform_update(self, serializer):
        serializer.save(customer_id=serializer.instance.customer_id)

    def perform_destroy(self, instance):
        if instance.kwh > 1000:
            raise ValidationError('Cannot delete large line items')
        instance.delete()
    
    @action(detail=False, methods=['get'], url_path='total-by-customer')
    def total_by_customer(self, request):
        # customer_id = request.query_params.get('customer_id')
        # if customer_id is None:
        #     raise ValidationError({'customer_id': 'customer_id is required'})

        # total = calculate_customer_total(customer_id)
        # return Response({'customer_id': int(customer_id), 'total': total})
        input_serializer = CustomerTotalInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        customer_id = input_serializer.validated_data['customer_id']
        total = calculate_customer_total(customer_id)

        output_serializer = CustomerTotalOutputSerializer({
            'customer_id': customer_id,
            'total': total,
        })            
        return Response(output_serializer.data)

    @action(detail=False, methods=['get'], url_path='search-or')
    def search_or(self, request):
        queryset = filter_line_items_or(LineItem.objects.all(), request.query_params)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='with-customer-slow')
    def with_customer_slow(self, request):
        items, query_count = get_line_items_with_customer_slow()
        return Response({'query_count': query_count, 'items': items})

    @action(detail=False, methods=['get'], url_path='with-customer-fast')
    def with_customer_fast(self, request):
        items, query_count = get_line_items_with_customer_fast()
        return Response({'query_count': query_count, 'items': items})
    
    @action(detail=False, methods=['get'], url_path='total-by-customer-slow')
    def total_by_customer_slow(self, request):
        input_serializer = CustomerTotalInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        customer_id = input_serializer.validated_data['customer_id']
        total, query_count = calculate_customer_total_slow(customer_id)
        return Response({'customer_id': customer_id, 'total': total, 'query_count': query_count})

    @action(detail=False, methods=['get'], url_path='total-by-customer-fast')
    def total_by_customer_fast(self, request):
        input_serializer = CustomerTotalInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        customer_id = input_serializer.validated_data['customer_id']
        total, query_count = calculate_customer_total_fast(customer_id)
        return Response({'customer_id': customer_id, 'total': total, 'query_count': query_count})
    
    @action(detail=False, methods=['get'], url_path='total-by-customer-raw')
    def total_by_customer_raw(self, request):
        input_serializer = CustomerTotalInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        customer_id = input_serializer.validated_data['customer_id']
        total, query_count = calculate_customer_total_raw_sql(customer_id)
        return Response({'customer_id': customer_id, 'total': total, 'query_count': query_count})

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()
# from django.db import connection
# with connection.cursor() as cursor:
#     cursor.execute("SELECT SUM(kwh * rate) FROM billing_lineitem WHERE customer_id = %s", [customer_id])
#     total = cursor.fetchone()[0]

class LineItemCalculateView(APIView):   
    def post(self, request):
        customer_id = request.data.get('customer_id')
        if customer_id is None:
            raise ValidationError({'customer_id': 'customer_id is required'})
        total = calculate_customer_total(customer_id)
        return Response({'customer_id': int(customer_id), 'total': total})
