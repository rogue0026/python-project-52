from django.contrib import messages
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(TemplateView):
    template_name = "index.html"


class Login(SuccessMessageMixin, views.LoginView):
    template_name = "login.html"
    success_message = "Вы залогинены"


class Logout(views.LogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().post(request, *args, **kwargs)
    template_name = "logout.html"
