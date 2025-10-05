from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoSerializer

@api_view(['GET'])
def listar_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reporte_stock(request):
    productos = Producto.objects.all()
    report = []
    for p in productos:
        report.append({
            'nombre': p.nombre,
            'cantidad': p.cantidad,
            'precio': p.precio,
            'valor_total': p.cantidad * p.precio
        })
    return Response(report)
