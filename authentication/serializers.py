from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.exception import ValidationException


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CreateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    email = serializers.CharField(required=True, allow_blank=False, max_length=100)
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    password = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        username = validated_data["username"]

        user_with_email = User.objects.all().filter(email=validated_data.get("email", None))

        if user_with_email.count() != 0:
            raise ValidationException(message="Email already used", field="email")

        users_with_username = User.objects.all().filter(username=username)
        if users_with_username.count() != 0:
            raise ValidationException(message="username already taken", field="username")

        user = User(**validated_data)
        if password is not None:
            user.set_password(password)

        user.is_active = True
        user.save()
        return user


class CheckEmailPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    email = serializers.CharField(required=True, allow_blank=False, max_length=100)