#from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from rest_framework import serializers, viewsets, generics, status
from django.contrib.auth import get_user_model

from .models import User
# # Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from backend import settings
#from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .serializers import ChangePasswordSerializer
from django.contrib.sites.shortcuts import get_current_site
from django import template


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'firstname', 'lastname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        user.is_active = True 

        user.save()

        return user


# @permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        raise PermissionDenied()


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)




# ==================================================
            #CHANGE PASSWORD
# ==================================================

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()
