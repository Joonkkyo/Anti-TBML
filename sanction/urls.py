from django.urls import path
from sanction import views

app_name = 'sanction'

urlpatterns = [
    # path('', views.SanctionLV.as_view(), name='index'),
    # path('', views.SanctionLV.as_view(), name='sanction_list'),
    path('', views.post_list, name='sanction_list'),
    # path('sanction', views.TableView.as_view(), name='sanction_list'),
]