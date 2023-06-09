from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, role, password=None):
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have a Email")
        if role is None:
            raise TypeError("User should have role")

        user = self.model(username=username, email=self.normalize_email(email))
        user.role = role
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        username,
        email,
        password=None,
    ):
        if password is None:
            raise TypeError("Password should not be none")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.role = 1
        user.is_verified = True
        user.save()
        return user
