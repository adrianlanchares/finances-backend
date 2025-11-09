from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListTransactionsView.as_view(), name="transactions"),
    path("create/", views.CreateTransactionView.as_view(), name="create-transaction"),
    path("<int:pk>/", views.TransactionView.as_view(), name="transaction-details"),
    path("balance/", views.AccountBalancesView.as_view(), name="account-balances"),
]
