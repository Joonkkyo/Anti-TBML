from django.contrib import admin
from django.urls import path, include

from config import views
from config.views import HomeView, AboutTV, UserCreateView, UserCreateDoneTV
from django.conf import settings
from django.conf.urls.static import static
from sanction.models import SanctionList


urlpatterns = [
    path('sanction/', include('sanction.urls')),
    path('document_inspection/', include('document_inspection.urls')),
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    path('accounts/register/done', UserCreateDoneTV.as_view(), name='register_done'),
    path('about/', AboutTV.as_view(), name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)