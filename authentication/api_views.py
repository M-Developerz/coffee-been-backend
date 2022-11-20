from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest

from authentication.exception import ValidationException
from authentication.serializers import UserSerializer, CreateUserSerializer, CheckEmailPasswordSerializer


@csrf_exempt
def check_email_username(request: HttpRequest):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data["email"]
        username = data["username"]

        users_with_email = User.objects.all().filter(email=email)
        users_with_username = User.objects.all().filter(username=username)

        if users_with_username.count() != 0:
            return JsonResponse({
                "messages": ["username already taken"],
                "isSuccess": False
            }, status=400)

        if users_with_email.count() != 0:
            return JsonResponse({
                "messages": ["email already taken"],
                "isSuccess": False
            }, status=400)

        return JsonResponse({
            "messages": ["Email and Password Valid"],
            "isSuccess": True
        }, status=200)

    return JsonResponse({
        "messages": ["Unkown Error"],
        "isSuccess": False}, status=404)


class UsersViewSet(APIView):
    # permission_classes = (IsAuthenticated,)

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
