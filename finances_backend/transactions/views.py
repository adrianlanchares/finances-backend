from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Case, When, F
from . import serializers


class CreateTransactionView(generics.CreateAPIView):
    queryset = serializers.TransactionSerializer.Meta.model.objects.all()  # type: ignore
    serializer_class = serializers.TransactionSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TransactionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = serializers.TransactionSerializer.Meta.model.objects.all()  # type: ignore

    serializer_class = serializers.TransactionSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListTransactionsView(generics.ListCreateAPIView):
    queryset = serializers.TransactionSerializer.Meta.model.objects.all()  # type: ignore

    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        queryset = self.queryset.all().order_by("-datetime")

        minAmount = self.request.query_params.get("minAmount", None)
        maxAmount = self.request.query_params.get("maxAmount", None)
        description = self.request.query_params.get("description", None)
        category = self.request.query_params.get("category", None)
        account = self.request.query_params.get("account", None)
        date = self.request.query_params.get("date", None)
        beforeDatetime = self.request.query_params.get("beforeDatetime", None)
        afterDatetime = self.request.query_params.get("afterDatetime", None)
        skip = self.request.query_params.get("skip", None)
        limit = self.request.query_params.get("limit", None)

        if minAmount:
            queryset = queryset.filter(amount__gte=minAmount)
        if maxAmount:
            queryset = queryset.filter(amount__lte=maxAmount)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if account:
            queryset = queryset.filter(account__icontains=account)
        if date:
            if date == "all":
                pass
            elif date == "year":
                queryset = queryset.filter(
                    datetime__gte=timezone.now() - timedelta(days=365)
                )
            elif date == "month":
                queryset = queryset.filter(
                    datetime__gte=timezone.now() - timedelta(days=30)
                )
            elif date == "week":
                queryset = queryset.filter(
                    datetime__gte=timezone.now() - timedelta(days=7)
                )
        if beforeDatetime:
            queryset = queryset.filter(datetime__lt=beforeDatetime)
        if afterDatetime:
            queryset = queryset.filter(datetime__gt=afterDatetime)
        if skip:
            queryset = queryset[int(skip) :]  # type: ignore

        if limit:
            queryset = queryset[: int(limit)]  # type: ignore

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.queryset.all().delete()
        return Response(
            {"detail": "All transactions deleted."}, status=status.HTTP_204_NO_CONTENT
        )


class AccountBalancesView(APIView):
    queryset = serializers.TransactionSerializer.Meta.model.objects.all()  # type: ignore

    serializer_class = serializers.TransactionSerializer

    def get(self, request):
        Model = self.serializer_class.Meta.model
        balances = Model.objects.values("account").annotate(  # type: ignore
            balance=Sum(F("amount"))
        )

        return Response({b["account"]: b["balance"] for b in balances})


class DeleteAllTransactionsView(APIView):
    """
    Deletes all transactions from the database.
    """

    serializer_class = serializers.TransactionSerializer

    def delete(self, request, *args, **kwargs):
        Model = self.serializer_class.Meta.model
        deleted_count, _ = Model.objects.all().delete()  # type: ignore
        return Response(
            {"detail": f"Deleted {deleted_count} transactions."},
            status=status.HTTP_204_NO_CONTENT,
        )
