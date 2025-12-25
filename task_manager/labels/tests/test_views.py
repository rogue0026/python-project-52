from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse


class BaseLabelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name="test_status")
        usr = User.objects.create_user(
            username="test",
            password="12345",
        )
        usr.save()

    def setUp(self):
        for i in range(1, 4):
            Label.objects.create(name=f"label_{i}")

        task = Task.objects.create(
            name="test_task",
            description="test_description",
            status=Status.objects.first(),
            author=User.objects.get(username="test"),
            executor=User.objects.get(username="test"),
        )
        task.labels.set(Label.objects.all())

        self.client.login(username="test", password="12345")


class LabelListViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("labels_list_view"))
        self.assertRedirects(response, reverse("login_view"))

    def test_logged_in_uses_correct_template(self):
        response = self.client.get(reverse("labels_list_view"))
        self.assertTemplateUsed(response, "labels/index.html")

    def test_lists_all_labels(self):
        response = self.client.get(reverse("labels_list_view"))
        self.assertEqual(response.status_code, 200)

        labels_from_template = response.context.get("object_list")
        self.assertQuerySetEqual(
            labels_from_template.order_by("name"),
            Label.objects.all().order_by("name"))


class CreateLabelViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("labels_create_view"))
        self.assertRedirects(response, reverse("login_view"))

    def test_logged_in_uses_correct_template(self):
        response = self.client.get(reverse("labels_create_view"))
        self.assertTemplateUsed(response, "labels/create.html")

    def test_create_new_label(self):
        response = self.client.post(
            reverse("labels_create_view"),
            data=({
                "name": "test_label",
            }),
            follow=True,
        )
        self.assertRedirects(response, reverse("labels_list_view"))
        self.assertContains(response, "Метка успешно создана")
        labels = response.context["object_list"]

        self.assertQuerySetEqual(
            labels.order_by("name"),
            Label.objects.all().order_by("name"),
        )


class UpdateLabelViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        label = Label.objects.create(name="test_label")
        response = self.client.get(
            reverse(
                "labels_update_view",
                kwargs={"pk": label.id}),
        )
        self.assertRedirects(response, reverse("login_view"))

    def test_logged_in_uses_correct_template(self):
        label = Label.objects.create(name="test_label_name")
        response = self.client.get(
            reverse("labels_update_view", kwargs={"pk": label.id}),
        )
        self.assertTemplateUsed(response, "labels/update.html")

    def test_update_label(self):
        label = Label.objects.create(name="test_label")
        response = self.client.post(
            reverse("labels_update_view", kwargs={"pk": label.id}),
            data=({"name": "test_label_updated"}),
            follow=True,
        )
        label.refresh_from_db()
        self.assertRedirects(response, reverse("labels_list_view"))
        self.assertEqual(label.name, "test_label_updated")
        self.assertContains(response, "Метка успешно изменена")


class DeleteLabelViewTest(BaseLabelTest):

    def test_redirect_if_not_logged_in(self):
        label = Label.objects.create(name="label_for_delete")
        self.client.logout()
        response = self.client.get(
            reverse("labels_delete_view", kwargs={"pk": label.id}),
        )
        self.assertRedirects(response, reverse("login_view"))

    def test_template_contains_label_name(self):
        label = Label.objects.first()
        response = self.client.get(
            reverse("labels_delete_view", kwargs={"pk": label.id}),
        )
        self.assertContains(response, label.name)

    def test_label_delete(self):
        label = Label.objects.create(name="label_for_deletion")
        response = self.client.post(
            reverse("labels_delete_view", kwargs={"pk": label.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse("labels_list_view"))
        self.assertContains(response, "Метка успешно удалена")
        self.assertFalse(Label.objects.filter(name=label.name).exists())

    def test_label_delete_constraint(self):
        response = self.client.post(
            reverse(
                "labels_delete_view",
                kwargs={"pk": Label.objects.first().id},
            ),
            follow=True,
        )
        self.assertRedirects(response, reverse("labels_list_view"))
        self.assertContains(
            response,
            "Невозможно удалить метку, потому что она используется",
        )
