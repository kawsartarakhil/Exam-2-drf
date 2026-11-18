from rest_framework import serializers
from .models import *


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"
        read_only_fields = ["book_loan","total_amount","department_amount","school_amount","status","created_at"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["payment_date"]
