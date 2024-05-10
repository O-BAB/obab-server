# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.tokens import CustomJWTAuthentication
from accounts.models import User
from core.constants import SystemCodeManager


class ConvenienceUpdateTest(APITestCase):
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
        test_update_image1 = self.upload_image(
            "recipes/tests/data/test_update_image1.png"
        )
        test_update_image2 = self.upload_image(
            "recipes/tests/data/test_update_image2.png"
        )
        test_update_image3 = self.upload_image(
            "recipes/tests/data/test_update_image.png"
        )

        self.data = {
            "categoryCD": "convenience_store_combination",
            "title": "create_test",
            "thumnail_url": thumbnail_url,
            "video": "http://127.0.0.1:8000/swagger/",
            "intro": "string",
            "time": "09:00:00",
            "people_num": 3,
            "difficulty": "easy",
            "recipe_image": [{"image_url": image1_url}, {"image_url": image2_url}],
            "recipe_process": [{"content": "string"}],
            "convenience_items": [{"name": "string", "price": 3000}],
        }

        response = self.client.post(
            path=self.create_recipe_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.data,
            format="json",
        )

        self.assertEqual(
            response.data["code"],
            SystemCodeManager.get_message("base_code", "SUCCESS")[0],
        )
        self.recipe_id = response.data["data"]["id"]

        self.update_data = {
            "categoryCD": "convenience_store_combination",
            "title": "update_test",
            "thumnail_url": test_update_image3,
            "video": "http://127.0.0.1:8000/swagger/update",
            "intro": "update_intro",
            "time": "09:10:11",
            "people_num": 5,
            "difficulty": "easy",
            "recipe_image": [
                {"image_url": test_update_image2},
                {"image_url": test_update_image1},
            ],
            "recipe_process": [{"content": "convenience_update test"}],
            "convenience_items": [
                {"name": "불닭", "price": 3000},
                {"name": "치즈", "price": 2000},
            ],
        }

    def test_update_convenience_recipe_success(self):
        update_url = f"{self.create_recipe_url}?id={self.recipe_id}"
        response = self.client.put(
            path=update_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.update_data,
            format="json",
        )

        self.assertEqual(
            response.data["code"],
            SystemCodeManager.get_message("base_code", "SUCCESS")[0],
        )

        self.assertEqual(response.data["data"]["title"], self.update_data["title"])
        self.assertEqual(response.data["data"]["video"], self.update_data["video"])
        self.assertEqual(response.data["data"]["intro"], self.update_data["intro"])
        self.assertEqual(response.data["data"]["time"], self.update_data["time"])
        self.assertEqual(
            response.data["data"]["people_num"], self.update_data["people_num"]
        )
        self.assertEqual(
            response.data["data"]["difficulty"], self.update_data["difficulty"]
        )
