from .base_settings import *
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))
SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# env
KAKAO_REST_API_KEY = env("kakao_rest_api_key")
SOCIAL_AUTH_GOOGLE_CLIENT_ID = env("google_client_api")
SOCIAL_AUTH_GOOGLE_SECRET = env("google_api_secret")
SOCIAL_AUTH_NAVER_CLIENT_ID = env("naver_api_key")
SOCIAL_AUTH_NAVER_SECRET = env("naver_api_secret")
STATE = env("state")
BASE_URL = env("base_url")

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

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
