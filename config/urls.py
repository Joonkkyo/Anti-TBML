from django.contrib import admin
from django.urls import path, include

from config import views
from config.views import HomeView, AboutTV
from django.conf import settings
from django.conf.urls.static import static
# from sanction.views import SanctionLV
from sanction.models import SanctionList


urlpatterns = [
    path('sanction/', include('sanction.urls')),
    path('document_inspection/', include('document_inspection.urls')),
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('about/', AboutTV.as_view(), name='about'),
    # path('sanction/', SanctionLV.as_view(model=SanctionList), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)