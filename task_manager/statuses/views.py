from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.views import View

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.users.middleware import AuthRequiredMixin


class StatusesListView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_statuses = Status.objects.all()
        formatted_statuses = []
        for status in all_statuses:
            formatted_statuses.append({
                "id": status.id,
                "name": status.name,
                "created_at": status.created_at.strftime("%d.%m.%Y %H:%M"),
            })

        return render(
            request,
            "statuses/index.html",
            context={
                "statuses": formatted_statuses,
            },
        )


class CreateStatusView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(
            request,
            "statuses/create.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        f = StatusForm(request.POST)
        if not f.is_valid():
            return render(
                request,
                "statuses/create.html",
                context={
                    "form": f,
                },
                status=422,
            )

        s = Status.objects.create(name=f.cleaned_data["name"])
        s.save()
        messages.success(
            request,
            "Статус успешно создан",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("statuses_list_view"))


class UpdateStatusView(View):
    def get(self, request, *args, **kwargs):
        status_id = int(kwargs.get("pk"))
        status = Status.objects.get(id=status_id)
        form = StatusForm(
            {
                "name": status.name,
            },
        )
        return render(
            request,
            "statuses/update.html",
            context={
                "form": form,
                "status_id": status_id,
            }
        )

    def post(self, request, *args, **kwargs):
        status_id = int(kwargs.get("pk"))
        status = Status.objects.get(id=status_id)
        form = StatusForm(request.POST)
        if not form.is_valid():
            render(
                request,
                "statuses/update.html",
                context={
                    "form": form,
                    "status_id": status_id,
                }
            )
        status.name = form.cleaned_data["name"]
        status.save()
        messages.success(
            request,
            "Статус успешно изменен",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("statuses_list_view"))


class DeleteStatusView(View):
    def get(self, request, *args, **kwargs):
        status_id = int(kwargs.get("pk"))
        status = Status.objects.get(id=status_id)
        return render(
            request,
            "statuses/delete.html",
            context={
                "status_name": status.name,
            },
        )

    def post(self, request, *args, **kwargs):
        # todo добавить проверку на наличие связей с имеющимися задачами
        status_id = int(kwargs.get("pk"))
        status = Status.objects.get(id=status_id)
        status.delete()
        messages.success(
            request,
            "Статус успешно удален",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("statuses_list_view"))