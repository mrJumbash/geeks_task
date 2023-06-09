from django.contrib.auth import authenticate
from accounts.models import User
from core.settings.env_reader import env
from accounts.services import UserService
import random
from rest_framework.exceptions import AuthenticationFailed
from core.settings.env_reader import env


def generate_username(name):
    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(
                email=email, password=env("GOOGLE_CLIENT_SECRET")
            )

            return {
                "username": registered_user.username,
                "email": registered_user.email,
                "tokens": UserService.tokens(user=registered_user),
            }

        else:
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user_by_email[0].auth_provider
            )

    else:
        user = {
            "username": generate_username(name),
            "email": email,
            "password": env("GOOGLE_CLIENT_SECRET"),
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.role = 2
        user.save()

        new_user = authenticate(email=email, password=env("GOOGLE_CLIENT_SECRET"))
        return {
            "email": new_user.email,
            "username": new_user.username,
            "tokens": UserService.tokens(user=new_user),
        }
