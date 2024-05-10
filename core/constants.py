from django.conf import settings
import json


class Constants:
    BASE_URL = getattr(settings, "BASE_URL")

    # kakao
    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_CALLBACK_URI = f"http://localhost:3000/kakao"

    # google
    GOOGLE_CALLBACK_URI = f"http://localhost:3000/google"
    GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    GOOGLE_SCOPE = " ".join(
        [
            "https://www.googleapis.com/auth/userinfo.email",
        ]
    )
    # naver
    NAVER_CALLBACK_URI = f"http://localhost:3000/naver"
    NAVER_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_NAVER_SECRET")


class SystemCodeManager:
    """
    ex)
    status_code, message_ko = SystemCodeManager.get_message("auth_code", "SUCCESS")
    status_code, message_en = SystemCodeManager.get_message("auth_code", "SUCCESS", 'en')
    """

    @classmethod
    def get_message(cls, system_code_type, message, lang="ko"):
        filepath = f"core/system_codes/{system_code_type}.json"
        messages = cls.load_messages(filepath)

        if message in messages:
            data = messages[message]
            if lang in data:
                return data["code"], data[lang]
        else:
            return SystemCodeManager.get_message("base_code", "SYSTEM_CODE_ERROR")
        return None

    @staticmethod
    def load_messages(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)["SYSTEM_CODE"]
