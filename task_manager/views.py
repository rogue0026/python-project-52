from django.contrib import messages
from django.contrib.auth import views
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class Login(views.LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        messages.success(self.request,"Вы залогинены")
        return super().form_valid(form)


class Logout(views.LogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().post(request, *args, **kwargs)
    template_name = "logout.html"
