from django.urls import path
from document_inspection import views
from django.conf.urls import include

app_name = 'document_inspection'

urlpatterns = [
    # path('', views.SanctionLV.as_view(), name='index'),
    path('',views.showfile, name='file_upload'),
    path('scan/', views.ScanLV.as_view(), name='scan'),
    # path('sanction', views.TableView.as_view(), name='sanction_list'),
]