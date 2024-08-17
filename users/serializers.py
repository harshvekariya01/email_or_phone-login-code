from rest_framework import serializers
from users.backends import EmailPhoneBackend
from knox.models import AuthToken
from django.contrib.auth import get_user_model
User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    email_phone = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email_phone = data.get('email_phone')
        password = data.get('password')
        user = EmailPhoneBackend().authenticate(request=None, email_phone=email_phone, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        return AuthToken.objects.create(user=user)