from django.contrib import admin
from django.urls import path, include
from config.views import HomeView, AboutTV
from django.conf import settings
from django.conf.urls.static import static
from config.views import UserCreateView, UserCreateDoneTV
# from sanction.views import SanctionLV
from sanction.models import SanctionList


urlpatterns = [
    path('sanction/', include('sanction.urls')),
    path('document_inspection/', include('document_inspection.urls')),
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    # path('user/', include('user.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('user/register/', UserCreateView.as_view(), name='register'),
    path('user/register/done/', UserCreateDoneTV.as_view(), name='register_done'),
    path('about/', AboutTV.as_view(), name='about'),
    # path('sanction/', SanctionLV.as_view(model=SanctionList), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)