from django.urls import path
from sanction import views

app_name = 'sanction'

urlpatterns = [
    path('', views.sanction_list, name='sanction_list'),
    path('search/', views.result, name='result'),
    path('add/', views.sanction_add, name='sanction_add'),
    path('delete/<int:id>/', views.sanction_delete, name='sanction_delete')
]