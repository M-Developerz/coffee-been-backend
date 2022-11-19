from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authentication.exception import ValidationException
from authentication.serializers import UserSerializer, CreateUserSerializer


class UsersViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    # serializer_class = UserSerializer
    # queryset = User.objects.all().order_by('-date_joined')

    def get(self, request, format=None):
        users = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationException as exception:
                return Response({"errors": [{
                    exception.field: exception.message
                }]}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
