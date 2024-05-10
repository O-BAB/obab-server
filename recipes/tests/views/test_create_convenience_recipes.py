# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.tokens import CustomJWTAuthentication
from accounts.models import User
from core.constants import SystemCodeManager


class ConvenienceCreateTest(APITestCase):
    create_recipe_url = reverse("recipes:convenience-recipes")
    create_image_url = reverse("recipes:recipe-images")

    email = "test@test.com"
    password = "password1234"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)
        cls.token = CustomJWTAuthentication.create_token(user=cls.user)
        cls.access_token = cls.token["access_token"]

    def upload_image(self, file_path):
        """
        Helper method to upload an image and return the URL.
        """
        with open(file_path, "rb") as img_file:
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
        return response.data["data"]["image"]

    def setUp(self):
        image1_url = self.upload_image("recipes/tests/data/test_image1.png")
        image2_url = self.upload_image("recipes/tests/data/test_image2.png")
        thumbnail_url = self.upload_image("recipes/tests/data/test_thumnail.png")

        self.data = {
            "categoryCD": "convenience_store_combination",
            "title": "create_test",
            "thumnail_url": thumbnail_url,
            "video": "http://127.0.0.1:8000/swagger/",
            "intro": "string",
            "time": "09:00",
            "people_num": 3,
            "difficulty": "easy",
            "recipe_image": [{"image_url": image1_url}, {"image_url": image2_url}],
            "recipe_process": [{"content": "string"}],
            "convenience_items": [{"name": "string", "price": 3000}],
        }

    def test_create_convenience_recipes_success(self):
        response = self.client.post(
            path=self.create_recipe_url,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
            data=self.data,
            format="json",
        )

        self.assertEqual(
            response.data["code"],
            SystemCodeManager.get_message("base_code", "SUCCESS")[0],
        )
