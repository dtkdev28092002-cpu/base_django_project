from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from user.serializers import (
    UserDetailSerializer,
    UserSerializer,
    RegisterUserSerializer,
    RegisterAdminSerializer,
    LoginSerializer,
    SendEmailSerializer,
)
from user.email import send_template_email
from user.auth import IsAdmin
from .pagination import StandardizedAPIView


class UserLoginView(StandardizedAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(serializer.response(user), status=status.HTTP_200_OK)


class UserDetailView(StandardizedAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUserView(StandardizedAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class RegisterAdminView(StandardizedAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterAdminSerializer)
    def post(self, request):
        serializer = RegisterAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class SendEmailView(StandardizedAPIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(request_body=SendEmailSerializer)
    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        send_template_email(
            to=data["to"],
            subject=data["subject"],
            template_name="emails/base.html",
            context={**data["context"], "body": data["body"]},
        )

        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)