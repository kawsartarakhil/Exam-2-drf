from rest_framework import serializers
from .models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate(self, data):
        total = data.get("total_quantity")
        available = data.get("available_quantity")

        if total is not None and available is not None:
            if available > total:
                raise serializers.ValidationError("Available quantity is lesser than the total quantity")

        return data


class BookPriceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPriceFactor
        fields = "__all__"


class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = "__all__"
        read_only_fields = ["loan_date","return_date","status","calculated_price"]
