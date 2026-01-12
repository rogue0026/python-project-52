from django.test import TestCase
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from django.urls import reverse


class BaseTasksTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 10):
            Label.objects.create(name=f"label_{i}")
            Status.objects.create(name=f"status_{i}")
            u = User.objects.create_user(
                username=f"user_{i}",
                password="12345",
            )
            u.save()
            task = Task.objects.create(
                name=f"test_task_{i}",
                description=f"task_descirption_{i}",
                status=Status.objects.get(name=f"status_{i}"),
                author=User.objects.get(username=f"user_{i}"),
                executor=User.objects.get(username=f"user_{i}"),
            )
            task.labels.add(Label.objects.get(name=f"label_{i}"))
            task.save()


class TasksListViewTest(BaseTasksTest):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("tasks_list_view"), follow=True)
        self.assertRedirects(response, reverse("login_view"))
        self.assertContains(
            response,
            "Для выполнения этой операции необходимо авторизоваться",
        )

    def test_list_all_tasks(self):
        self.client.login(username="user_1", password="12345")
        response = self.client.get(reverse("tasks_list_view"))
        self.assertTemplateUsed(response, "tasks/index.html")
        tasks_expected = Task.objects.all().order_by("id")
        tasks_actual = response.context.get("tasks")
        self.assertQuerySetEqual(tasks_expected, tasks_actual.order_by("id"))

    def test_only_my_tasks_filter(self):
        self.client.login(username="user_1", password="12345")
        response = self.client.get(
            reverse("tasks_list_view"),
            data=({"self_tasks": "on"}),
        )
        tasks_actual = response.context.get("tasks")
        tasks_expected = Task.objects.filter(
            executor=User.objects.get(username="user_1"),
        )
        self.assertQuerySetEqual(
            tasks_actual.order_by("id"),
            tasks_expected.order_by("id"),
        )

    def test_label_filter(self):
        self.client.login(username="user_1", password="12345")
        label = Label.objects.get(name="label_1")
        response = self.client.get(
            reverse("tasks_list_view"),
            data={"label": label.id},
        )
        tasks_actual = response.context.get("tasks")
        tasks_expected = Task.objects.filter(labels__id=label.id)
        self.assertQuerySetEqual(
            tasks_actual.order_by("id"),
            tasks_expected.order_by("id"),
        )

    def test_executor_filter(self):
        self.client.login(username="user_1", password="12345")
        user = User.objects.get(username="user_4")
        response = self.client.get(
            reverse("tasks_list_view"),
            data={"executor": user.id},
        )
        tasks_actual = response.context.get("tasks")
        tasks_expected = Task.objects.filter(executor=user)
        self.assertQuerySetEqual(
            tasks_actual.order_by("id"),
            tasks_expected.order_by("id"),
        )

    def test_status_filter(self):
        self.client.login(username="user_1", password="12345")
        status = Status.objects.get(name="status_6")
        response = self.client.get(
            reverse("tasks_list_view"),
            data={"status": status.id},
        )
        tasks_actual = response.context.get("tasks")
        tasks_expected = Task.objects.filter(status=status)
        self.assertQuerySetEqual(
            tasks_actual.order_by("id"),
            tasks_expected.order_by("id"),
        )


class CreateTaskViewTest(BaseTasksTest):
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("tasks_create_view"), follow=True)
        self.assertRedirects(response, reverse("login_view"))
        self.assertContains(
            response,
            "Для выполнения этой операции необходимо авторизоваться",
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="user_1", password="12345")
        response = self.client.get(reverse("tasks_create_view"))
        self.assertTemplateUsed(response, "common/create.html")

    def test_create_task(self):
        self.client.login(username="user_1", password="12345")
        form_data = {
            "name": "task_123",
            "description": "test description",
            "status": Status.objects.get(name="status_2").id,
            "author": User.objects.get(username="user_1").id,
            "executor": User.objects.get(username="user_2").id,
            "labels": Label.objects.filter(
                name__in=["label_1", "label_2"]).values_list("id", flat=True),
            }
        response = self.client.post(
            reverse("tasks_create_view"),
            data=form_data,
            follow=True,
        )
        task = Task.objects.filter(
            name="task_123",
            description="test description",
        )
        self.assertTrue(task.exists())
        self.assertRedirects(response, reverse("tasks_list_view"))
        self.assertContains(response, "Задача успешно создана")


class UpdateTaskViewTest(BaseTasksTest):
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        first_task = Task.objects.first()
        response = self.client.get(
            reverse("tasks_update_view", kwargs={"pk": first_task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse("login_view"))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="user_1", password="12345")
        first_task = Task.objects.first()
        response = self.client.get(
            reverse("tasks_update_view", kwargs={"pk": first_task.id}))
        self.assertTemplateUsed(response, "common/update.html")

    def test_update_task(self):
        self.client.login(username="user_1", password="12345")
        first_task = Task.objects.first()
        form_data = {
            "name": "task_updated_name",
            "description": "updated_description",
            "status": Status.objects.get(name="status_8").id,
            "author": User.objects.get(username="user_7").id,
            "executor": User.objects.get(username="user_8").id,
            "labels": Label.objects.filter(
                name__in=[
                    "label_3",
                    "label_4",
                    "label_5",
                ]).values_list("id", flat=True),
        }
        response = self.client.post(
            reverse("tasks_update_view", kwargs={"pk": first_task.id}),
            data=form_data,
            follow=True,
        )
        first_task.refresh_from_db()
        status_expected = Status.objects.get(name="status_8")
        labels_expected = Label.objects.filter(name__in=[
            "label_3",
            "label_4",
            "label_5",
        ])
        self.assertRedirects(response, reverse("tasks_list_view"))
        self.assertEqual(first_task.name, "task_updated_name")
        self.assertEqual(first_task.description, "updated_description"),
        self.assertEqual(first_task.status, status_expected)
        self.assertEqual(
            first_task.executor,
            User.objects.get(username="user_8"))
        self.assertQuerySetEqual(
            first_task.labels.order_by("id"),
            labels_expected.order_by("id"),
        )


class DeleteTaskViewTest(BaseTasksTest):
    def test_redirect_if_not_logged_in(self):
        first_task = Task.objects.first()
        response = self.client.get(
            reverse("tasks_delete_view", kwargs={"pk": first_task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse("login_view"))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="user_1", password="12345")
        first_task = Task.objects.first()
        response = self.client.get(
            reverse("tasks_delete_view", kwargs={"pk": first_task.id}))
        self.assertTemplateUsed(response, "common/delete.html")

    def test_delete_task(self):
        self.client.login(username="user_2", password="12345")
        task = Task.objects.filter(
            author=User.objects.get(username="user_2")).first()
        id_for_deletion = task.id
        response = self.client.post(
            reverse("tasks_delete_view", kwargs={"pk": task.id}),
            follow=True,
        )
        self.assertFalse(Task.objects.filter(id=id_for_deletion).exists())
        self.assertRedirects(response, reverse("tasks_list_view"))
        self.assertContains(response, "Задача успешно удалена")

    def test_delete_permission(self):
        self.client.login(username="user_1", password="12345")
        task = Task.objects.filter(
            author=User.objects.get(username="user_2")).first()
        response = self.client.post(
            reverse("tasks_delete_view", kwargs={"pk": task.id}),
            follow=True,
        )
        self.assertRedirects(response, reverse("tasks_list_view"))
        self.assertContains(response, "Задачу может удалить только ее автор")
