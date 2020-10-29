from django.contrib import admin
from django.urls import path, include
from config.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
# from sanction.views import SanctionLV
from sanction.models import SanctionList


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('sanction/', include('sanction.urls')),
    path('document_inspection/', include('document_inspection.urls')),
    # path('sanction/', SanctionLV.as_view(model=SanctionList), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)