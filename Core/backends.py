from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class UserIdOrEmailBackend(ModelBackend):
    """Authenticate with either user_id or email address"""

    def authenticate(self, request, username=None, password=None, email=None, user_id=None, **kwargs):
        UserModel = get_user_model()
        identifier = user_id or email or username or kwargs.get(UserModel.USERNAME_FIELD)
        if not identifier:
            return None

        try:
            user = UserModel.objects.filter(
                Q(user_id__iexact=identifier) | Q(email__iexact=identifier)
            ).first()
            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None
        return None
