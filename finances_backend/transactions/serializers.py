import re
from rest_framework import serializers, exceptions
from . import models


# Create or update transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
