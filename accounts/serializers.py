from rest_framework import serializers
from .models import CustomUser


class RegisterSerailizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerailizer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ["id","username","email","first_name","last_name","role","groups"]
        read_only_fields = ["role", "groups"]



# access
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzk0OTczMjc4LCJpYXQiOjE3OTQ5NzIzNzgsImp0aSI6IjA1YTVhMmU3YjYyNzQ1YTViN2Y2M2NlNzA1Mjk5ZjNhIiwidXNlcl9pZCI6IjEifQ.axxm_Ljd-KJCmZZ0dSnwJSIS4GnYYA0oJGGM30sU5Bs

# refresh
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc5NTU3NzE3OCwiaWF0IjoxNzk0OTcyMzc4LCJqdGkiOiI1MTNmZGIxYWI0MTA0MDA4YWE3MmM3N2U1N2I4MmJiYiIsInVzZXJfaWQiOiIxIn0.aPAfe0DiTTMNaL2PTxSMyD09j9Ymx15_OdKW1tDH8ws