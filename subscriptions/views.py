from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Subscription, Payment
from .serializers import SubscriptionSerializer, PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SubscriptionView(generics.RetrieveUpdateAPIView):

    serializer_class = SubscriptionSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        subscription, created = Subscription.objects.get_or_create(
            user=self.request.user
        )

        return subscription
    

class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        amount = request.data.get("amount")

        payment = Payment.objects.create(

            user=request.user,

            amount=amount,

            payment_id=f"PAY-{request.user.id}-{Payment.objects.count()+1}",

            status="completed"
        )

        subscription, created = Subscription.objects.get_or_create(
            user=request.user
        )

        subscription.activate_premium(days=30)

        serializer = PaymentSerializer(payment)

        return Response({

            "payment": serializer.data,

            "subscription": {

                "plan": subscription.plan,

                "active": subscription.active,

                "start_date": subscription.start_date,

                "end_date": subscription.end_date,
            }
        })
    



class PaymentHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        payments = Payment.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(serializer.data)
    



class SubscriptionStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        subscription, created = Subscription.objects.get_or_create(
            user=request.user
        )

        return Response({

            "plan": subscription.plan,

            "active": subscription.active,

            "start_date": subscription.start_date,

            "end_date": subscription.end_date,
        })