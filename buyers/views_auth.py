from django.contrib import admin, messages
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

from .permissions import IsAdminOrManager

from .models import User
from .serializers import (
    SignupSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
)
import uuid
from datetime import datetime


#############################
# auth
#############################


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    # def perform_create(self, serializer):
    #     password=get_random_string(12)
    #     print(password)
    #     user=serializer.save()
    #     user.set_password(password)
    #     user.save()
    #     return Response({"password":password},status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = get_random_string(12)
        user = serializer.save()
        user.set_password(password)
        user.save()

        return Response(
            {
                "message": "User created successfully",
                "password": password,
            },
            status=status.HTTP_201_CREATED,
        )


class ResetView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        if not User.objects.filter(email=email).exists():
            return Response({"error": "Invaid user"}, status=status.HTTP_404_NOT_FOUND)

        try:
            resetHash = self.kwargs["hash"]
            newPassword = request.data["password"]
            user = User.objects.get(email=email)
            if len(newPassword) < 8:
                return Response(
                    {"error": "password should be atleast 8 character long"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif user.hash == resetHash and user.timestamp > int(
                datetime.now().timestamp()
            ):
                user.set_password(newPassword)
                user.save()
                return Response(
                    {"success": "password changed successully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "link expired"}, status=status.HTTP_400_BAD_REQUEST
                )
        except:
            resetHash = uuid.uuid4()
            timestamp = int(datetime.now().timestamp()) + 15 * 60
            user = User.objects.get(email=email)
            user.hash = resetHash
            user.timestamp = timestamp
            user.save()

            BASE_URL = os.getenv("FRONTEND_BASE_URL")
            reset_link = BASE_URL + "/reset/" + f"{resetHash}/"

            subject = "Origins Coffee Password Reset"
            message = f"Hello {user.full_name},\n\nYour reset link is: {reset_link}\n\n"
            recipient_list = [user.email]

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    recipient_list,
                    fail_silently=False,
                )

            except Exception as e:
                print(e)

            return Response(
                {"success": "email sent to your mail", "link": reset_link},
                status=status.HTTP_200_OK,
            )


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "Password updated successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
