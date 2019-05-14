from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from common.forms import CommonLoginForm, RegistrationForm
from django.urls import reverse_lazy


class CommonLoginView(LoginView):
    form_class = CommonLoginForm
    template_name = 'common/login.html'
    redirect_authenticated_user = True


class CommonLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class CommonRegisterView(CreateView):
    template_name = 'common/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')
