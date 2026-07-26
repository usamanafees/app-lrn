from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_contracts_with_meters_slow, get_contracts_with_meters_fast


class ContractsWithMetersSlowView(APIView):
    def get(self, request):
        items, query_count = get_contracts_with_meters_slow()
        return Response({'query_count': query_count, 'items': items})


class ContractsWithMetersFastView(APIView):
    def get(self, request):
        items, query_count = get_contracts_with_meters_fast()
        return Response({'query_count': query_count, 'items': items})