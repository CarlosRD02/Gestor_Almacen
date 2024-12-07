from django.urls import path 
from .views import (
    crear_proveedor,
    listar_proveedores,
    crear_producto,
    listar_productos,
    eliminar_producto,
    entregar_pedido,
)

urlpatterns = [
    path('proveedores/crear/', crear_proveedor, name='crear_proveedor'),
    path('proveedores/', listar_proveedores, name='listar_proveedores'),
    
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/', listar_productos, name='listar_productos'),
    path('productos/eliminar/<int:id_producto>/', eliminar_producto, name='eliminar_producto'),
    
    path('pedidos/realizar/<int:id_producto>/', entregar_pedido, name='realizar_pedido'),
]