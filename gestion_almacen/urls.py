"""
URL configuration for gestion_almacen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from almacen.views import (
    crear_proveedor,
    listar_proveedores,
    crear_producto,
    listar_productos,
    eliminar_producto,
    entregar_pedido,
    editar_producto,
    dashboard,
    listar_pedidos,
    editar_proveedor,
    eliminar_proveedor,
    editar_pedido,
    eliminar_pedido,
    crear_pedido,
    user_login,
    user_logout,
    registrar,
)

urlpatterns = [
    path('admin/', admin.site.urls,),
    path('dashboard/registro/', registrar, name='registro'),
    
    path('login/', user_login, name='user_login'),  # URL para login
    path('logout/', user_logout, name='user_logout'),
    
    path('proveedores/', listar_proveedores, name='listar_proveedores'),
    path('proveedores/crear/', crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id_proveedor>/', editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id_proveedor>/', eliminar_proveedor, name='eliminar_proveedor'),
    
    path('productos/', listar_productos, name='listar_productos'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/eliminar/<int:id_producto>/', eliminar_producto, name='eliminar_producto'),
    path('productos/editar/<int:id_producto>/', editar_producto, name='editar_producto'),
    
    path('dashboard/', dashboard, name='dashboard'),
    
    path('pedidos/', listar_pedidos, name='listar_pedidos'),
    path('pedidos/entregar/<int:id_pedido>/', entregar_pedido, name='entregar_pedido'),
    path('pedidos/editar/<int:id_pedido>/', editar_pedido, name='editar_pedido'),
    path('pedidos/eliminar/<int:id_pedido>/', eliminar_pedido, name='eliminar_pedido'),
    path('pedidos/crear/', crear_pedido, name='crear_pedido'),
]
