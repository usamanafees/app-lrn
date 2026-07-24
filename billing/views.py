from rest_framework import viewsets          # fixed — DRF import
from .models import LineItem                 # fixed pattern — your model name
from .serializers import LineItemSerializer  # fixed pattern — your serializer name
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action


class LineItemViewSet(viewsets.ModelViewSet): # LineItemViewSet = yours | ModelViewSet = fixed DRF base
    queryset = LineItem.objects.all()         # queryset = fixed attr name | LineItem = yours
    serializer_class = LineItemSerializer     # serializer_class = fixed | LineItemSerializer = yours
    
    def get_queryset(self):                   # get_queryset = fixed DRF hook name
        queryset = super().get_queryset()
        customer_id = self.request.query_params.get('customer_id')
        # self = fixed
        # request = fixed (HTTP request)
        # query_params = fixed (DRF, reads ?key=value)
        # 'customer_id' = yours (query param name)
        # customer_id = yours (local variable)
        if self.action == 'list' and customer_id is not None:
            queryset = queryset.filter(customer_id=customer_id)
            # filter = fixed Django ORM method
            # customer_id=customer_id → left = model field (yours) | right = value (yours)
        return queryset  

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
    
    @action(detail=False, methods=['get'], url_path='total-by-custmer')
    def total_by_customer(self, request):
        customer_id = request.query_params.get('customer_id')
        if customer_id is None:
            raise ValidationError({'customer_id': 'customer_id is required'})

        items = LineItem.objects.filter(customer_id=customer_id)
        total = sum(item.total for item in items)
        return Response({'customer_id': int(customer_id), 'total': total})