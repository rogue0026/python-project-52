from mmap import PROT_EXEC

from django.db.models import ProtectedError
from django.shortcuts import (
    render,
    reverse,
    redirect
)
from django.contrib import messages
from django.views import View
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from task_manager.users.middleware import (
    AuthRequiredMixin,
)


class LabelListView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_labels = Label.objects.all()
        return render(
            request,
            "labels/index.html",
            context={
                "labels": all_labels,
            },
        )


class CreateLabelView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(
            request,
            "labels/create.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "labels/create.html",
                context={
                    "form": form,
                },
                status=422,
            )
        label = Label.objects.create(name=form.cleaned_data["name"])
        label.save()
        messages.success(
            request,
            "Метка успешно создана",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("labels_list_view"))


class UpdateLabelView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = int(kwargs.get("pk"))
        label = Label.objects.get(id=label_id)
        form = LabelForm({
            "name": label.name,
        })
        return render(
            request,
            "labels/update.html",
            context={
                "form": form,
                "label_id": label_id,
            },
        )

    def post(self, request, *args, **kwargs):
        label_id = int(kwargs.get("pk"))
        form = LabelForm({
            "name": request.POST.get("name"),
        })
        if not form.is_valid():
            return render(
                request,
                "labels/update.html",
                context={
                    "form": form,
                    "label_id": label_id,
                },
                status=422,
            )
        label = Label.objects.get(id=label_id)
        label.name = form.cleaned_data["name"]
        label.save()
        messages.success(
            request,
            "Метка успешно изменена",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("labels_list_view"))


class DeleteLabelView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = int(kwargs.get("pk"))
        label = Label.objects.get(id=label_id)
        return render(
            request,
            "labels/delete.html",
            context={
                "label_name": label.name,
            },
        )

    def post(self, request, *args, **kwargs):
        label_id = int(kwargs.get("pk"))
        label = Label.objects.get(id=label_id)
        try:
            label.delete()
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется",
                extra_tags="alert alert-danger",
            )
            return redirect(reverse("labels_list_view"))

        messages.success(
            request,
            "Метка успешно удалена",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("labels_list_view"))
