from django.urls import path
from .views import SubscriptionView, CreatePaymentView, PaymentHistoryView, SubscriptionStatusView


urlpatterns = [

    path('',SubscriptionView.as_view(),name='subscription'),

    path("create-payment/",CreatePaymentView.as_view()),

    path("payment-history/",PaymentHistoryView.as_view()),

    path("status/",SubscriptionStatusView.as_view()),
]