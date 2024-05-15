# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.tokens import CustomJWTAuthentication
from accounts.models import User


class BasicRecipeUpdateTest(APITestCase):
    create_recipe_url = reverse("recipes:basic-recipes-create")
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
            0,
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
            "categoryCD": "food_recipe",
            "title": "Spaghetti Carbonara",
            "thumnail_url": thumbnail_url,
            "video": "https://example.com/video/carbonara.mp4",
            "intro": "Classic Italian pasta dish with eggs, cheese, pancetta, and black pepper",
            "time": "03:11",
            "people_num": 4,
            "difficulty": "easy",
            "recipe_ingredients": [
                {
                    "type": "pasta",
                    "name": "spaghetti",
                    "count": 400,
                    "unit": "grams",
                    "etc": "preferably thick spaghetti",
                },
                {
                    "type": "meat",
                    "name": "pancetta",
                    "count": 150,
                    "unit": "grams",
                    "etc": "diced",
                },
                {
                    "type": "dairy",
                    "name": "Parmesan cheese",
                    "count": 100,
                    "unit": "grams",
                    "etc": "grated",
                },
                {
                    "type": "dairy",
                    "name": "eggs",
                    "count": 4,
                    "unit": "units",
                    "etc": "large eggs",
                },
                {
                    "type": "spice",
                    "name": "black pepper",
                    "count": 1,
                    "unit": "teaspoon",
                    "etc": "freshly ground",
                },
            ],
            "recipe_image": [{"image_url": image1_url}, {"image_url": image2_url}],
            "recipe_process": [
                {
                    "content": "Boil the spaghetti in salted water according to package instructions until al dente."
                },
                {
                    "content": "While the pasta cooks, sauté the pancetta in a skillet over medium heat until crisp."
                },
                {
                    "content": "In a bowl, whisk together eggs and grated Parmesan until well combined."
                },
                {
                    "content": "Drain the pasta and add it to the skillet with the pancetta. Remove from heat."
                },
                {
                    "content": "Quickly pour in the egg and cheese mixture, stirring vigorously to coat the spaghetti and to prevent the eggs from scrambling."
                },
                {
                    "content": "Serve immediately with additional Parmesan and a generous sprinkle of black pepper."
                },
            ],
        }
        response = self.client.post(
            path=self.create_recipe_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.data,
            format="json",
        )

        self.assertEqual(
            response.data["code"],
            0,
        )
        self.recipe_id = response.data["data"]["id"]

        self.update_data = {
            "title": "Updated Spaghetti Carbonara",
            "thumnail_url": test_update_image3,
            "video": "https://example.com/video/carbonara_updated.mp4",
            "intro": "Updated classic Italian pasta dish with eggs, cheese, pancetta, and black pepper",
            "time": "03:30:00",
            "people_num": 2,
            "difficulty": "medium",
            "recipe_ingredients": [
                {
                    "type": "pasta",
                    "name": "spaghetti",
                    "count": 200,
                    "unit": "grams",
                    "etc": "preferably thick spaghetti",
                },
                {
                    "type": "meat",
                    "name": "pancetta",
                    "count": 100,
                    "unit": "grams",
                    "etc": "diced",
                },
                {
                    "type": "dairy",
                    "name": "Parmesan cheese",
                    "count": 50,
                    "unit": "grams",
                    "etc": "grated",
                },
                {
                    "type": "dairy",
                    "name": "eggs",
                    "count": 2,
                    "unit": "units",
                    "etc": "large eggs",
                },
                {
                    "type": "spice",
                    "name": "black pepper",
                    "count": 1,
                    "unit": "teaspoon",
                    "etc": "freshly ground",
                },
            ],
            "recipe_image": [
                {"image_url": test_update_image1},
                {"image_url": test_update_image2},
            ],
            "recipe_process": [
                {"content": "Boil the spaghetti in salted water until al dente."},
                {
                    "content": "Sauté the pancetta in a skillet over medium heat until crisp."
                },
                {"content": "Whisk eggs and Parmesan together."},
                {
                    "content": "Drain the pasta and add to the skillet with pancetta. Remove from heat."
                },
                {"content": "Pour in the egg mixture, stirring vigorously."},
                {"content": "Serve immediately with Parmesan and black pepper."},
            ],
        }

    def test_update_basic_recipe_success(self):
        update_url = reverse(
            "recipes:basic-recipes-update", kwargs={"id": self.recipe_id}
        )
        response = self.client.put(
            path=update_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.update_data,
            format="json",
        )

        self.assertEqual(
            response.data["code"],
            0,
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
