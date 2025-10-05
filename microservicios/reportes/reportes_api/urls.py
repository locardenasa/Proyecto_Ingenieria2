from django.urls import path
from . import views

urlpatterns = [
    path('reportes/', views.ReporteListCreate.as_view(), name='reportes'),
    path('reportes/pdf/', views.ReportePDF.as_view(), name='reporte_pdf'),
    path('reportes/excel/', views.ReporteExcel.as_view(), name='reporte_excel'),
]
