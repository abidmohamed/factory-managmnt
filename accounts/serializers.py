from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # knox fields
        # fields = ('id', 'username', 'email')
        # simple jwt fields
        fields = ('first_name', 'last_name', 'username',)
