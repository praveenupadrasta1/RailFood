from datetime import datetime
from django.utils import timezone

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, OTP
from BAAS.config import PASSWORD_MIN_LENGTH, INVALID_CREDENTIALS, USER_DEACTIVATED, INVALID_EMAIL_ADDRESS, EMAIL_KEY, \
    OTP_IS_REQUIRED, CATEGORY_IS_REQUIRED, PASSWORD_KEY, OTP_KEY, TOKEN_KEY, CATEGORY_KEY, IS_EMAIL_VERIFIED, \
    CONSUMER, RESTAURANT, DELIVERY_BOY


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user"""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.

    # The first option is the way it stored in DB and second option is the Human readable format
    ROLES_CHOICE = (('0', CONSUMER),
                    ('1', RESTAURANT),
                    ('2', DELIVERY_BOY),)

    password = serializers.CharField(
            max_length=128,
            min_length=PASSWORD_MIN_LENGTH,
            write_only=True
        )

    role = serializers.ChoiceField(choices=ROLES_CHOICE, allow_blank=False)

    # mobile_num = serializers.CharField(required=True)

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'password', 'token', 'role']

    def create(self, validated_data):
        # Use the `create_user` method we write earlier to create a new user.
        user = User.objects.create_user(**validated_data)
        if user is not None:
            otp_row = OTP.otp_objects.create_otp(user, 'EMAIL')

            # subject = "TrainApp Account verification"
            # message_text = "Please enter the following verification code to verify your TrainApp account \n\n" + \
            #        str(otp_row.otp) + "\n\n This code is valid for next 7 minutes"
            # recipient = [user.email]
            # # recipient.append(user.email)
            # # mail = EmailUtility.CreateMessage(settings.EMAIL_HOST_USER, recipient, subject, message)
            # EmailUtility.send_mail(recipient, subject, message_text)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    # username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    is_email_verified = serializers.BooleanField(read_only=True)
    # mobile_num = serializers.CharField(max_length=12, required=False)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.

        user = None
        password = data.get(PASSWORD_KEY, None)

        # # Raise an exception if an
        # # email is not provided
        # if email is None and mobile_num is None:
        #     raise serializers.ValidationError(
        #         'An email address or mobile number is required to log in.'
        #     )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(INVALID_CREDENTIALS)

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we ser `USERNAME_FIELD` as `email`.
        if data.has_key(EMAIL_KEY):
            email = data.get(EMAIL_KEY, None)
            user = authenticate(username=email, password=password)
        # elif data.has_key('mobile_num'):
        #     mobile_num = data.get('mobile_num', None)
        #     try:
        #         user = User.objects.get(mobile_num=mobile_num)
        #         user.check_password(password)
        #     except User.DoesNotExist:
        #         raise serializers.ValidationError('Invalid Credentials!')
        # else:
        #     raise serializers.ValidationError('Invalid Credentials!')

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                INVALID_CREDENTIALS
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                USER_DEACTIVATED
            )

        user.last_login = datetime.now(timezone.get_current_timezone())
        user.save()

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            EMAIL_KEY: user.email,
            # 'mobile_num': user.mobile_num,
            IS_EMAIL_VERIFIED: user.is_email_verified,
            # USERNAME_KEY: user.username,
            TOKEN_KEY: user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objjects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'token',)

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is that
        # we don't need to specify anything else about the field. The
        # password field needed the `min_length` and
        # `max_length` properties, but that isn't the case for the token
        # field.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        # Passwords should not be handled with `setattr`, unline other fields.
        # Django provides a funciton that handles hashing and
        # salting passwords. That means
        # we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop(PASSWORD_KEY, None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` handles all
            # of the security stuff that we shouldn;t be concerned with.
            instance.set_password(password)

        # After everything has been updadted we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    """
    This serializer is responsible to check if the user email provided is correct or not
    """

    email = serializers.EmailField(required=True)

    def validate(self, data):
        try:
            User.objects.get(email=data.get(EMAIL_KEY))
            return data
        except Exception as e:
            raise serializers.ValidationError(INVALID_EMAIL_ADDRESS)


class OTPVerificationSerializer(serializers.Serializer):
    """
    This serializer is responsible to check if the OTP are correct for given Category (Email or Mobile)
    """
    OTP_CATEGORIES = (('EMAIL', 'email'),)
    otp = serializers.IntegerField(required=True)
    category = serializers.ChoiceField(choices=OTP_CATEGORIES, required=True, allow_blank=False)

    def validate(self, data):
        otp = data.get(OTP_KEY, None)
        category = data.get(CATEGORY_KEY, None)

        if otp is None:
            raise serializers.ValidationError(OTP_IS_REQUIRED)

        if category is None:
            raise serializers.ValidationError(CATEGORY_IS_REQUIRED)

        return data


class OTPRegenerateSerializer(serializers.Serializer):
    """
        This serializer is responsible to check if Category (Email or Mobile) is correct
        """
    OTP_CATEGORIES = (('EMAIL', 'email'),)
    category = serializers.ChoiceField(choices=OTP_CATEGORIES, required=True, allow_blank=False)

    def validate(self, data):
        category = data.get(CATEGORY_KEY, None)

        if category is None:
            raise serializers.ValidationError(CATEGORY_IS_REQUIRED)

        return data
