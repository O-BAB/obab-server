from django.conf import settings


class Constants:
    BASE_URL = getattr(settings, "BASE_URL")

    GOOGLE_CALLBACK_URI = f"http://localhost:3000/google"
    GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    GOOGLE_SCOPE = " ".join(
        [
            "https://www.googleapis.com/auth/userinfo.email",
        ]
    )

    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_CALLBACK_URI = f"http://localhost:3000/kakao"
