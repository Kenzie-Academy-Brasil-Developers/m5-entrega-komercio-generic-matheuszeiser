from django.test import TestCase
from ..models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
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

    def test_user_attr(self):
        id_primary_key = self.common._meta.get_field("id").primary_key
        username_max_length = self.common._meta.get_field("username").max_length
        username_unique = self.common._meta.get_field("username").unique
        first_name_max_length = self.common._meta.get_field("first_name").max_length
        last_name_max_length = self.common._meta.get_field("last_name").max_length

        self.assertTrue(id_primary_key)
        self.assertTrue(username_unique)
        self.assertEqual(username_max_length, 20)
        self.assertEqual(first_name_max_length, 50)
        self.assertEqual(last_name_max_length, 50)
