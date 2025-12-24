from django.test import TestCase
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse


class BaseLabelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        usr = User.objects.create_user(
            username="test",
            password="12345",
        )
        usr.save()

    def setUp(self):
        self.client.login(username="test", password="12345")


class LabelListViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/labels/")
        redirect_to = response.headers.get("Location")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_to, "/login/")

    def test_logged_in_uses_correct_template(self):
        response = self.client.get("/labels/")
        self.assertTemplateUsed(response, "labels/index.html")

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("labels_list_view"))
        self.assertEqual(response.status_code, 200)

    def test_lists_all_labels(self):
        for i in range(1, 4):
            label = Label(name=f"label_{i}")
            label.save()

        response = self.client.get("/labels/")
        self.assertEqual(response.status_code, 200)

        labels = response.context.get("object_list")
        self.assertEqual(
            list(labels.values_list("name", flat=True)),
            ["label_1", "label_2", "label_3"],
        )


class CreateLabelViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/labels/create/")
        redirect_to = response.headers.get("Location")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(redirect_to == "/login/")

    def test_logged_in_uses_correct_template(self):
        response = self.client.get("/labels/create/")
        self.assertTemplateUsed(response, "labels/create.html")

    def test_create_new_label(self):
        response = self.client.post(
            "/labels/create/",
            data=({
                "name": "test_label"
            }),
        )
        self.assertEqual(response.status_code, 302)
        labels = Label.objects.filter(name="test_label")

        self.assertEqual(
            list(labels.values_list("name", flat=True)),
            ["test_label"],
        )

    def test_contains_flash_message_after_create(self):
        response = self.client.post(
            "/labels/create/",
            data=({
                "name": "test_label"
            }),
            follow=True,
        )
        self.assertContains(response, "Метка успешно создана")


class UpdateLabelViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/labels/2/update/")
        redirect_to = response.headers.get("Location")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_to, "/login/")

    def test_logged_in_uses_correct_template(self):
        label = Label.objects.create(name="test_label_name")
        response = self.client.get(f"/labels/{label.id}/update/")
        self.assertTemplateUsed(response, "labels/update.html")

    def test_update_label(self):
        label = Label.objects.create(name="test_label")
        response = self.client.post(
            f"/labels/{label.id}/update/",
            data=({"name": "new_label_name"}),
        )
        label.refresh_from_db()
        redirect_to = response.headers.get("Location")
        self.assertEqual("/labels/", redirect_to)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(label.name, "new_label_name")

    def test_contains_flash_message_after_update(self):
        label = Label.objects.create(name="test_label")
        response = self.client.post(
            f"/labels/{label.id}/update/",
            data=({"name": "new_label_name"}),
            follow=True,
        )
        self.assertContains(response, "Метка успешно изменена")


class DeleteLabelViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        label = Label.objects.create(name="label_for_delete")
        self.client.logout()
        response = self.client.get(f"/labels/{label.id}/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get("Location"), "/login/")

    def test_contains_label_name(self):
        label = Label.objects.create(name="label_for_delete")
        response = self.client.get(f"/labels/{label.id}/delete/")
        self.assertContains(response, "label_for_delete")

    def test_label_delete(self):
        label = Label.objects.create(name="label_for_delete")
        response = self.client.post(f"/labels/{label.id}/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers.get("Location"), "/labels/")
        label_exists = Label.objects.filter(name="label_for_delete").exists()
        self.assertFalse(label_exists)

    def test_contains_flash_message_after_delete(self):
        label = Label.objects.create(name="label_for_delete")
        response = self.client.post(
            f"/labels/{label.id}/delete/",
            follow=True,
        )
        self.assertContains(response, "Метка успешно удалена")

    def test_label_delete_constraint(self):
        label = Label.objects.create(name="label_1")
        status = Status.objects.create(name="status_1")
        task = Task.objects.create(
            name="test_task",
            description="test_description",
            status=status,
            author=User.objects.get(username="test"),
            executor=User.objects.get(username="test"),
        )
        task.labels.set(Label.objects.all())
        response = self.client.post(
            f"/labels/{label.id}/delete/",
            follow=True,
        )
        self.assertContains(
            response,
            "Невозможно удалить метку, потому что она используется",
        )
