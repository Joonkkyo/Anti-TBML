from django.urls import path
from sanction import views
from sanction.views import SanctionAddDoneTV

app_name = 'sanction'

urlpatterns = [
    path('', views.sanction_list, name='sanction_list'),
    path('search/', views.result, name='result'),
    path('add/', views.sanction_add, name='sanction_add'),
    path('add/done/', SanctionAddDoneTV.as_view(), name='sanction_add_done'),
    path('delete/<int:id>/', views.sanction_delete, name='sanction_delete'),
    path('update/<int:id>/', views.sanction_update, name='sanction_update'),
]