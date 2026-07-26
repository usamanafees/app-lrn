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

class CustomerTotalInputSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(
        error_messages={
            'required': 'customer_id is required.',
            'invalid': 'customer_id must be a number ccc.',
        }
    )

class CustomerTotalOutputSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
