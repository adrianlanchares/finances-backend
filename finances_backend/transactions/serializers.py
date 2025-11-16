from rest_framework import serializers
from . import models


# Create or update transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    cashflow = serializers.ChoiceField(
        choices=["income", "expense"], write_only=True, required=True
    )

    class Meta:
        model = models.Transaction
        fields = [
            "id",
            "amount",
            "description",
            "category",
            "account",
            "datetime",
            "cashflow",
        ]

    def validate(self, attrs):
        amount = attrs["amount"]
        cashflow = attrs["cashflow"]

        if cashflow == "expense":
            attrs["amount"] = -abs(amount)
        else:
            attrs["amount"] = abs(amount)

        # remove the field before saving
        attrs.pop("cashflow")
        return attrs

    def create(self, validated_data):
        original = models.Transaction.objects.create(**validated_data)  # type: ignore

        if original.account == "ahorros":
            models.Transaction.objects.create(  # type: ignore
                amount=-original.amount,  # reversed sign
                description=original.description,
                category=original.category,
                account="tarjeta",
                datetime=original.datetime,
            )

        return original

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
