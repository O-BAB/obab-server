# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.tokens import CustomJWTAuthentication
from accounts.models import User
from core.constants import SystemCodeManager


class RecipeImageCreateTest(APITestCase):
    create_image_url = reverse("recipes:recipe-images")

    email = "test@test.com"
    password = "password1234"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)
        cls.token = CustomJWTAuthentication.create_token(user=cls.user)
        cls.access_token = cls.token["access_token"]

    def setUp(self):
        self.image1_url = "recipes/tests/data/test_image1.png"

    def test_create_recipe_images_success(self):
        with open(self.image1_url, "rb") as img_file:
            response = self.client.post(
                self.create_image_url,
                HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
                data={"image": img_file},
                format="multipart",
            )
        self.assertEqual(
            response.data["code"],
            SystemCodeManager.get_message("base_code", "SUCCESS")[0],
        )
