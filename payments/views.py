from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serailizers import *
from rest_framework.permissions import IsAuthenticated


class BillView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            bills = Bill.objects.all()

        elif user.role == "regional_admin" and user.region_id:
            bills = Bill.objects.filter(book_loan__book__institution__region_id=user.region_id)
        elif user.role == "school_admin" and user.institution_id:
            bills = Bill.objects.filter(book_loan__book__institution_id=user.institution_id)
        else:
            return Response({"error": "Permission denied"}, status=403)

        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)
        


class BillDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            bill = Bill.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            bill = Bill.objects.filter(id=pk,book_loan__book__institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            bill = Bill.objects.filter(id=pk,book_loan__book__institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)

        if not bill:
            return Response({"error": "Bill not found"}, status=404)
        serializer = BillSerializer(bill)
        return Response(serializer.data)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            payments = Payment.objects.all()
        elif user.role == "regional_admin" and user.region_id:
            payments = Payment.objects.filter(bill__book_loan__book__institution__region_id=user.region_id)
        elif user.role == "school_admin" and user.institution_id:
            payments = Payment.objects.filter(bill__book_loan__book__institution_id=user.institution_id)

        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            bill = serializer.validated_data["bill"]
            amount = serializer.validated_data["amount"]

            if user.role == "super_admin" and user.is_superuser:
                pass
            elif user.role == "regional_admin" and user.region_id:
                if bill.book_loan.book.institution.region_id != user.region_id:
                    return Response({"error": "Permission denied"}, status=403)
            elif user.role == "school_admin" and user.institution_id:
                if bill.book_loan.book.institution_id != user.institution_id:
                    return Response({"error": "Permission denied"}, status=403)
            else:
                return Response({"error": "Permission denied"}, status=403)
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
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            payment = Payment.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            payment = Payment.objects.filter(id=pk,bill__book_loan__book__institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            payment = Payment.objects.filter(id=pk,bill__book_loan__book__institution_id=user.institution_id).first()

        else:
            return Response({"error": "Permission denied"}, status=403)
        if not payment:
            return Response({"error": "Payment not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)


