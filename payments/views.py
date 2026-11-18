from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serailizers import *


class BillView(APIView):
    def get(self, request):
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)


class BillDetailView(APIView):
    def get(self, request, pk):
        bill = Bill.objects.filter(id=pk).first()
        if not bill:
            return Response({"error": "bill not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = BillSerializer(bill)
        return Response(serializer.data)


class PaymentView(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            bill = serializer.validated_data["bill"]
            amount = serializer.validated_data["amount"]

            if amount <= 0:
                return Response({"error": "Payment amount must be greater than zero"},status=status.HTTP_400_BAD_REQUEST)

            payments = Payment.objects.filter(bill=bill)
            total_paid = sum(payment.amount for payment in payments)
            remaining = bill.total_amount - total_paid

            if amount > remaining:
                return Response({"error": "Payment exceeds remaining amount"},status=status.HTTP_400_BAD_REQUEST)

            payment = serializer.save()
            total_paid += amount

            if total_paid >= bill.total_amount:
                bill.status = "paid"
            else:
                bill.status = "partial"

            bill.save()

            return Response(PaymentSerializer(payment).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailView(APIView):
    def get(self, request, pk):
        payment = Payment.objects.filter(id=pk).first()
        if not payment:
            return Response({"error": "Payment not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
