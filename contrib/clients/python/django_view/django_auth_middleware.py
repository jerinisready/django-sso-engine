from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class SSOAuthBackend(BaseBackend):
    """
    Customized the structure of django.contrib.auth.backends.RemoteUserBackend
    """
    sso_agent = None
    create_unknown_user = True

    def clean_username(self, sso_agent):
        auth_details = sso_agent.get_user_details()
        if auth_details:
            return auth_details['features'].get('username')

    def configure_user(self, request, user, created=True):
        """
        Update user details in case of registration, or on the login after update happens on the remote server.
        """
        user_features = self.sso_agent.get_user_details()['features']
        commit = False
        for key in user_features:
            if key in self.sso_agent.get_registration_features():
                if getattr(user, key, None) != user_features[key]:
                    commit = True
                    setattr(user, key, user_features[key])
        if commit:
            user.save()
        return user

    def authenticate(self, request, sso_agent):
        if not sso_agent:
            return
        created = False
        user = None
        self.sso_agent = sso_agent
        username = self.clean_username(sso_agent)       # We trust the user backend from sso agent, if it exists
        if username is None:
            return

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = User._default_manager.get_or_create(
                **{User.USERNAME_FIELD: username},
            )
        else:
            try:
                user = User._default_manager.get_by_natural_key(username)
            except User.DoesNotExist:
                pass
        user = self.configure_user(request, user, created=created)
        return user if self.user_can_authenticate(user) else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)
