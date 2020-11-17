from django.conf.urls.static import static
from django.urls import path
from document_inspection import views
from django.conf.urls import include
from config import settings

app_name = 'document_inspection'

urlpatterns = [
    # path('', views.SanctionLV.as_view(), name='index'),
    # path('',views.showfile, name='file_upload'),
    path('upload/', views.upload, name='upload')
    # path('scan/', views.ScanLV.as_view(), name='scan'),
    # path('sanction', views.TableView.as_view(), name='sanction_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
