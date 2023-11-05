from django.conf.urls import url

from user_authentication.views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, ForgotPasswordView, \
    OTPVerifyView, OTPRegenerateView, OTPResendView

urlpatterns = [
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^user/forgot_password/?$', ForgotPasswordView.as_view()),
    url(r'^verify_otp/?$', OTPVerifyView.as_view()),
    url(r'^regenerate_otp/?$', OTPRegenerateView.as_view()),
    url(r'^resend_otp/?$', OTPResendView.as_view()),
]