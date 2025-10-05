from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_productos),
    path('reporte_stock/', views.reporte_stock),
]
