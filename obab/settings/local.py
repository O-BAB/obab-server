from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

BASE_URL = env("BASE_URL")

SOCIAL_AUTH_GOOGLE_CLIENT_ID = env("GOOGLE_OAUTH2_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_SECRET = env("GOOGLE_OAUTH2_CLIENT_SECRET")
STATE = env("STATE")

KAKAO_REST_API_KEY = env("KAKAO_REST_API_KEY")
