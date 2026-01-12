
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class BaseUsersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 11):
            usr = User.objects.create_user(
                username=f"user_{i}",
                password="12345",
            )
            usr.save()


class UserListViewTest(BaseUsersTest):
    def test_user_list(self):
        response = self.client.get(
            reverse("users_list_view"),
        )
        users_expected = response.context.get("object_list")
        self.assertTemplateUsed(
            response,
            "users/index.html",
        )
        self.assertQuerySetEqual(
            User.objects.all().order_by("id"),
            users_expected.order_by("id"),
        )


class UserRegistrationViewTest(BaseUsersTest):
    def test_uses_correct_template(self):
        response = self.client.get(
            reverse("registration_view")
        )
        self.assertTemplateUsed(
            response,
            "common/create.html"
        )

    def test_create_user_normal_scenario(self):
        form_data = {
            "first_name": "user_firstname",
            "last_name": "user_lastname",
            "username": "test_username",
            "password1": "super_secret_password",
            "password2": "super_secret_password",
        }
        response = self.client.post(
            reverse("registration_view"),
            data=form_data,
            follow=True,
        )
        self.assertTrue(
            User.objects.filter(username="test_username").exists(),
        )
        self.assertRedirects(
            response, reverse("login_view"),
        )
        self.assertContains(
            response,
            "Пользователь успешно зарегистрирован",
        )

    def test_create_with_validation_errors(self):
        form_data = {
            "first_name": "user_firstname",
            "last_name": "user_lastname",
            "username": "invalid_usr()_#",
            "password1": "super_secret_password",
            "password2": "super_secret_password123",
        }
        response = self.client.post(
            reverse("registration_view"),
            data=form_data,
        )
        self.assertContains(
            response,
            "Введите правильное имя пользователя",
        )
        self.assertContains(
            response,
            "Введенные пароли не совпадают."
        )


class UpdateUserViewTest(BaseUsersTest):
    def test_redirects_if_not_logged_in(self):
        first_user = User.objects.first()
        response = self.client.get(
            reverse("users_update_view", kwargs={"pk": first_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse("login_view"))
        self.assertContains(
            response,
            "Для выполнения этой операции необходимо авторизоваться",
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="user_1", password="12345")
        first_user = User.objects.first()
        response = self.client.get(
            reverse(
                "users_update_view",
                kwargs={"pk": first_user.id}),
        )
        self.assertTemplateUsed(response, "common/update.html")

    def test_update_user_normal_scenario(self):
        self.client.login(username="user_1", password="12345")
        first_user = User.objects.first()
        form_data = {
            "first_name": "updated first name",
            "last_name": "updated last name",
            "username": "updated_user_1_username",
            "password1": "123456",
            "password2": "123456",
        }
        response = self.client.post(
            reverse(
                "users_update_view",
                kwargs={"pk": first_user.id},
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("users_list_view"),
        )
        self.assertContains(
            response,
            "Пользователь успешно изменен",
        )
        first_user.refresh_from_db()
        self.assertEqual(
            first_user.first_name, "updated first name",
        )
        self.assertEqual(
            first_user.last_name, "updated last name",
        )
        self.assertEqual(
            first_user.username, "updated_user_1_username",
        )

    def test_update_user_with_validation_errors(self):
        self.client.login(username="user_1", password="12345")
        first_user = User.objects.first()
        invalid_form_data = {
            "first_name": "updated first name",
            "last_name": "updated last name",
            "username": "(@)invalid#username(@)",
            "password1": "123456###",
            "password2": "123456",
        }
        response = self.client.post(
            reverse("users_update_view", kwargs={"pk": first_user.id}),
            data=invalid_form_data,
        )
        self.assertContains(
            response,
            "Введите правильное имя пользователя",
        )
        self.assertContains(
            response,
            "Введенные пароли не совпадают",
        )

    def test_update_error_user(self):
        self.client.login(username="user_1", password="12345")
        second_user = User.objects.get(username="user_2")
        form_data = {
            "first_name": "user_2",
            "last_name": "user_2",
            "username": "user_2_updated",
            "password1": "12345",
            "password2": "12345",
        }
        response = self.client.post(
            reverse(
                "users_update_view",
                kwargs={"pk": second_user.id},
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("users_list_view"),
        )
        self.assertContains(
            response,
            "У вас нет прав для изменения",
        )


class DeleteUserViewTest(BaseUsersTest):
    def test_redirects_if_not_logged_in(self):
        first_user = User.objects.first()
        response = self.client.get(
            reverse("users_delete_view", kwargs={"pk": first_user.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse("login_view"))
        self.assertContains(
            response,
            "Для выполнения этой операции необходимо авторизоваться",
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="user_1", password="12345")
        first_user = User.objects.get(username="user_1")
        response = self.client.get(
            reverse("users_delete_view", kwargs={"pk": first_user.id})
        )
        self.assertTemplateUsed(
            response,
            "common/delete.html",
        )

    def test_contains_user_full_name(self):
        self.client.login(username="user_1", password="12345")
        first_user = User.objects.get(username="user_1")
        response = self.client.get(
            reverse("users_delete_view", kwargs={"pk": first_user.id})
        )
        self.assertContains(
            response,
            f"{first_user.first_name} {first_user.last_name}",
        )

    def test_delete_user(self):
        self.client.login(username="user_1", password="12345")
        first_user = User.objects.get(username="user_1")
        response = self.client.post(
            reverse("users_delete_view", kwargs={"pk": first_user.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("users_list_view"),
        )
        self.assertContains(
            response,
            "Пользователь успешно удален",
        )
        user_exists = User.objects.filter(id=first_user.id).exists()
        self.assertFalse(user_exists)

    def test_delete_user_error(self):
        self.client.login(username="user_1", password="12345")
        second_user = User.objects.get(username="user_2")
        response = self.client.post(
            reverse("users_delete_view", kwargs={"pk": second_user.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("users_list_view"),
        )
        self.assertContains(
            response,
            "У вас нет прав для изменения",
        )
