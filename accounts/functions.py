from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User


def get_user_id(request):
    auth_header = request.headers.get("Authorization")
    access_tokne = auth_header.split(" ")[1]
    decoded = AccessToken(access_tokne)
    user_id = decoded["user_id"]
    user_instance = User.objects.get(id=user_id)
    return user_instance
