from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
User = get_user_model()

class EmailPhoneBackend(BaseBackend):
    def authenticate(self, request, email_phone=None, password=None, **kwargs):
        try:
            # Try to get user by email
            user = User.objects.get(email=email_phone)
        except User.DoesNotExist:
            try:
                # Try to get user by phone number
                user = User.objects.get(phone_number=email_phone)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
