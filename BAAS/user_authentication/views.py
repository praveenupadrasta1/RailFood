# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from BAAS.config import HTTP_API_VERSION_KEY, BETA_VERSION_KEY, INVALID_API_VERSION, DETAILS_KEY, STATUS_CODE_KEY, \
    EMAIL_KEY, USER_KEY, ROLE_KEY
from utilities.UserUtilities import UserUtilities
from utilities.OTPUtilities import OTPUtilities
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, ForgotPasswordSerializer, OTPVerificationSerializer, OTPRegenerateSerializer
)

# Create your views here.


class RegistrationAPIView(generics.GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return RegistrationSerializer
        raise Exception(INVALID_API_VERSION)

    def post(self, request):
        user = request.data.get(USER_KEY,{})

        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return LoginSerializer
        raise Exception(INVALID_API_VERSION)

    def post(self, request):
        user = request.data.get(USER_KEY, {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return UserSerializer
        raise Exception(INVALID_API_VERSION)

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.get_serializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get(USER_KEY,{})

        serializer = self.get_serializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return ForgotPasswordSerializer
        raise Exception(INVALID_API_VERSION)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = UserUtilities.forgot_password(request.data.get(EMAIL_KEY))
            return Response({DETAILS_KEY: response.get(DETAILS_KEY)}, status=response.get(STATUS_CODE_KEY))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return OTPVerificationSerializer
        raise Exception(INVALID_API_VERSION)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = OTPUtilities.verify_otp(request)
            return Response({DETAILS_KEY:response.get(DETAILS_KEY)}, status=response.get(STATUS_CODE_KEY))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPRegenerateView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return OTPRegenerateSerializer
        raise Exception(INVALID_API_VERSION)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = OTPUtilities.regenerate_otp(request=request)
            return Response({DETAILS_KEY:response.get(DETAILS_KEY)}, status=response.get(STATUS_CODE_KEY))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPResendView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return OTPRegenerateSerializer
        raise Exception(INVALID_API_VERSION)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = OTPUtilities.resend_otp(request=request)
            return Response({DETAILS_KEY:response.get(DETAILS_KEY)}, status=response.get(STATUS_CODE_KEY))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)