from rest_framework import serializers

from .models import LineItem

class LineItemSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()

    class Meta:
        model = LineItem
        fields = ['id', 'customer_id', 'kwh', 'rate', 'total', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_kwh(self, value):          # validate_<field> = fixed DRF pattern
        if value < 0:                         # value = fixed param name
            raise serializers.ValidationError('kwh cannot be negative')
        return value                          # must return cleaned value