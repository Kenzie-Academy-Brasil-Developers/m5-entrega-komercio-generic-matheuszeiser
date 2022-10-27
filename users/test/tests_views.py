from rest_framework.test import APITestCase, APIClient
from ..models import User
from rest_framework.authtoken.models import Token


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = APIClient()
        cls.user_data_superuser = {
            "username": "Matheus",
            "password": "1234",
            "first_name": "Matheus",
            "last_name": "Zeiser",
            "is_seller": True,
        }
        cls.user_data_seller = {
            "username": "Giovanna",
            "password": "1234",
            "first_name": "Giovanna",
            "last_name": "Zeiser",
            "is_seller": True,
        }
        cls.user_data_common = {
            "username": "Ricardo",
            "password": "1234",
            "first_name": "Ricardo",
            "last_name": "Zeiser",
            "is_seller": False,
        }

        cls.superuser = User.objects.create_superuser(**cls.user_data_superuser)
        cls.seller = User.objects.create_user(**cls.user_data_seller)
        cls.common = User.objects.create_user(**cls.user_data_common)

        cls.token_superuser = cls.client.post(
            "/api/login/",
            {
                "username": "Matheus",
                "password": "1234",
            },
        )
        cls.token_seller = cls.client.post(
            "/api/login/",
            {
                "username": "Giovanna",
                "password": "1234",
            },
        )
        cls.token_common = cls.client.post(
            "/api/login/",
            {
                "username": "Ricardo",
                "password": "1234",
            },
        )

    def test_login_success(self):
        """
        Verifica a rota de login com um usuário válido
        """
        response = self.client.post(
            "/api/login/",
            {
                "username": "Matheus",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_login_failed(self):
        """
        Verifica a rota de login com um usuário inválido
        """
        response = self.client.post(
            "/api/login/",
            {"username": "Não existe", "password": "2134"},
        )
        self.assertEqual(response.status_code, 403)

    def test_create_user_uuid(self):
        """
        Verifica a rota de criação de usuários com UUID
        """
        response = self.client.post(
            "/api/accounts/",
            {
                "username": "Ana",
                "password": "1234",
                "first_name": "Ana",
                "last_name": "Zeiser",
            },
        )
        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("is_seller", response.data)
        self.assertIn("date_joined", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("is_superuser", response.data)
        self.assertEqual(len(response.data["id"]), 36)
        self.assertEqual(response.status_code, 201)

    def test_list_all_users(self):
        """
        Verifica a rota de listagem de todos os usuários
        """
        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_list_newest_joined_users(self):
        """
        Verifica a rota de listagem de usuários com a classificação de mais recentes
        """
        response = self.client.get("/api/accounts/newest/1/")

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["username"], "Ricardo")

    def test_update_user(self):
        """
        Verifica a rota de atualização de usuário
        """
        # token = Token.objects.get(user__username="Giovanna")
        # self.client.login(username="Giovanna", password="1234")

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller.data["token"]
        )

        response = self.client.patch(
            f"/api/accounts/{self.seller.id.urn[9:]}/",
            {
                "last_name": "Clark",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual("Clark", response.data["last_name"])

    def test_soft_delete(self):
        """
        Verifica a rota de deleção do usuário
        """

        token = Token.objects.get(user__username="Matheus")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{self.common.id.urn[9:]}/management/",
            {
                "is_active": False,
            },
        )

        self.assertEqual(response.status_code, 200)
