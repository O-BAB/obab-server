from django.conf import settings


class Constants:
    BASE_URL = getattr(settings, "BASE_URL")

    # kakao
    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_CALLBACK_URI = "http://localhost:3000/kakao"

    # google
    GOOGLE_CALLBACK_URI = "http://localhost:3000/google"
    GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    GOOGLE_SCOPE = " ".join(["https://www.googleapis.com/auth/userinfo.email"])
    # naver
    NAVER_CALLBACK_URI = "http://localhost:3000/naver"
    NAVER_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_NAVER_SECRET")
