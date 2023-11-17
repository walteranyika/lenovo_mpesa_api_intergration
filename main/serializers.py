from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20) # 254723456789 # 254 11
    amount = serializers.IntegerField()