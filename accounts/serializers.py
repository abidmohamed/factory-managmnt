from django.contrib.auth.password_validation import validate_password
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

#
# class ChangePasswordSerializer(serializers):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('old_password', 'password', 'password2')
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#
#         return attrs
#
#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})
#         return value
#
#     def update(self, instance, validated_data):
#
#         instance.set_password(validated_data['password'])
#         instance.save()
#
#         return instance