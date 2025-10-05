import io
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from .serializers import ProductoSerializer
from reportlab.pdfgen import canvas

# CRUD básico
class ReporteListCreate(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Reporte creado"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PDF dinámico
class ReportePDF(APIView):
    def get(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        productos = Producto.objects.all()
        y = 800
        p.drawString(100, y, "Reporte de Productos")
        y -= 30
        for producto in productos:
            line = f"{producto.nombre} - Cantidad: {producto.cantidad_vendida} - Fecha: {producto.fecha}"
            p.drawString(100, y, line)
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='reporte.pdf')

# Excel dinámico
class ReporteExcel(APIView):
    def get(self, request):
        # Import pandas lazily so Django can start even if pandas/numpy aren't installed.
        try:
            import pandas as pd
        except Exception as e:
            # Return a clear error response instead of crashing the server at import-time.
            return Response({
                "error": "pandas (and its dependencies) are required for Excel export.",
                "details": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        productos = Producto.objects.all().values()
        df = pd.DataFrame(productos)
        buffer = io.BytesIO()
        # Use xlsxwriter (installed) as engine; pandas will require it for Excel output.
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Productos')
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='reporte.xlsx')