from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class BaseStatusesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="test", password="12345")
        user.save()

    def setUp(self):
        self.client.login(username="test", password="12345")
        for i in range(1, 10):
            Status.objects.create(name=f"status_{i}")
        Label.objects.create(name="test_label")
        task = Task.objects.create(
            name="test_task",
            description="test_description",
            status=Status.objects.first(),
            author=User.objects.get(username="test"),
            executor=User.objects.get(username="test"),
        )
        task.labels.set(Label.objects.all())


class StatusesListViewTest(BaseStatusesTest):
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse("statuses_list_view"),
            follow=True,
        )
        self.assertRedirects(response, reverse("login_view"))
        self.assertContains(
            response,
            "Для выполнения этой операции необходимо авторизоваться",
        )

    def test_logged_in_uses_correct_template(self):
        response = self.client.get(reverse("statuses_list_view"))
        self.assertTemplateUsed(response, "statuses/index.html")

    def test_list_all_statuses(self):
        response = self.client.get(reverse("statuses_list_view"))
        statuses = response.context.get("object_list")
        self.assertQuerySetEqual(
            statuses.order_by("name"),
            Status.objects.all().order_by("name"),
        )


class CreateStatusViewTest(BaseStatusesTest):
    def test_uses_correct_template(self):
        response = self.client.get(reverse("statuses_create_view"))
        self.assertTemplateUsed(response, "statuses/create.html")

    def test_create_new_status(self):
        response = self.client.post(
            reverse("statuses_create_view"),
            data=({"name": "new_status"}),
            follow=True,
        )
        status_exists = Status.objects.filter(name="new_status").exists()
        self.assertTrue(status_exists)
        self.assertRedirects(response, reverse("statuses_list_view"))
        self.assertContains(response, "Статус успешно создан")


class UpdateStatusViewTest(BaseStatusesTest):
    def test_uses_correct_template(self):
        first_status = Status.objects.first()
        response = self.client.get(
            reverse(
                "statuses_update_view",
                kwargs={"pk": first_status.id},
            ),
        )
        self.assertTemplateUsed(
            response,
            "statuses/update.html",
        )

    def test_update_status(self):
        first_status = Status.objects.first()
        response = self.client.post(
            reverse(
                "statuses_update_view",
                kwargs={"pk": first_status.id},
            ),
            data={"name": "first_status_updated"},
            follow=True,
        )
        first_status.refresh_from_db()
        self.assertRedirects(response, reverse("statuses_list_view"))
        self.assertContains(response, "Статус успешно изменен")
        self.assertEqual(first_status.name, "first_status_updated")


class DeleteStatusViewTest(BaseStatusesTest):
    def test_uses_correct_template(self):
        first_status = Status.objects.first()
        response = self.client.get(
            reverse(
                "statuses_delete_view",
                kwargs={"pk": first_status.id})
        )
        self.assertTemplateUsed(
            response,
            "statuses/delete.html",
        )

    def test_show_status_name_on_page(self):
        last_status = Status.objects.last()
        response = self.client.get(
            reverse(
                "statuses_delete_view",
                kwargs={"pk": last_status.id},
            )
        )
        self.assertContains(response, last_status.name)

    def test_delete_status(self):
        last_status = Status.objects.last()
        response = self.client.post(
            reverse(
                "statuses_delete_view",
                kwargs={"pk": last_status.id},
            ),
            follow=True,
        )
        status_exists = Status.objects.filter(name=last_status.name).exists()
        self.assertRedirects(response, reverse("statuses_list_view"))
        self.assertContains(response, "Статус успешно удален")
        self.assertFalse(status_exists)

    def test_constraint_delete_status(self):
        first_status = Status.objects.first()
        response = self.client.post(
            reverse(
                "statuses_delete_view",
                kwargs={"pk": first_status.id},
            ),
            follow=True,
        )
        self.assertRedirects(response, reverse("statuses_list_view"))
        self.assertContains(
            response,
            "Невозможно удалить статус, потому что он используется",
        )
