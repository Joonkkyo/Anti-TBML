from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm


class HomeView(TemplateView):
    template_name = 'home.html'

class AboutTV(TemplateView):
    template_name = 'about.html'

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'