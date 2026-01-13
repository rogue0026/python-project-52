from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView


class BaseCreate(SuccessMessageMixin, CreateView):
    template_name = "common/create.html"


class BaseUpdate(SuccessMessageMixin, UpdateView):
    template_name = "common/update.html"


class BaseDelete(SuccessMessageMixin, DeleteView):
    template_name = "common/delete.html"