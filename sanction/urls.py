from django.urls import path
from sanction import views

app_name = 'sanction'

urlpatterns = [
    path('', views.sanction_list, name='sanction_list'),
    path('search/', views.result, name='result'),
]