from rest_framework.test import APITestCase, APIClient
from users.models import User
from products.models import Product
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = APIClient()
        cls.user_data_seller = {
            "username": "Giovanna",
            "password": "1234",
            "first_name": "Giovanna",
            "last_name": "Zeiser",
            "is_seller": True,
        }

        cls.seller = User.objects.create_user(**cls.user_data_seller)

        cls.token_seller = cls.client.post(
            "/api/login/",
            {
                "username": "Giovanna",
                "password": "1234",
            },
        )

    def test_create_product(self):
        token = Token.objects.get(user__username="Giovanna")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.post(
            "/api/products/",
            {
                "description": "Smartband XYZ 3.0",
                "price": 100.99,
                "quantity": 15,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertIn("seller", response.data)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("quantity", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("id", response.data["seller"])
        self.assertEqual(len(response.data["id"]), 36)
        self.assertEqual("Smartband XYZ 3.0", response.data["description"])

    def test_update_product(self):

        token = Token.objects.get(user__username="Giovanna")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        product_id = self.client.post(
            "/api/products/",
            {
                "description": "Smartband XYZ 3.0",
                "price": 100.99,
                "quantity": 15,
            },
        ).data["id"]

        response = self.client.patch(
            f"/api/products/{product_id}/",
            {
                "description": "Televisão",
                "price": 200.00,
                "quantity": 10,
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("Televisão", response.data["description"])

    def test_list_products(self):

        token = Token.objects.get(user__username="Giovanna")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.client.post(
            "/api/products/",
            {
                "description": "Smartband XYZ 3.0",
                "price": 100.99,
                "quantity": 15,
            },
        )
        self.client.post(
            "/api/products/",
            {
                "description": "Televisão",
                "price": 200.00,
                "quantity": 5,
            },
        )
        response = self.client.get("/api/products/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            "Smartband XYZ 3.0", response.data["results"][0]["description"]
        )
        self.assertEqual("Televisão", response.data["results"][1]["description"])
        ...
