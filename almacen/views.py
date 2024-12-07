from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, Producto, Pedido
from .forms import ProveedorForm, ProductoForm, PedidoForm, RegistroForm
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Componentes de Acceso y Autenticacion

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirigir al dashboard después del login
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirigir al login después del logout

@login_required
def dashboard(request):
    total_proveedores = Proveedor.objects.count()
    # total_productos = Producto.objects.aggregate(total_stock=Sum('stock'))['total_stock'] or 0
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()

    context = {
        'total_proveedores': total_proveedores,
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
    }

    return render(request, 'login/dashboard.html', context)

@login_required
def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirigir al login después del registro
    else:
        form = RegistroForm()
    
    return render(request, 'login/registro.html', {'form': form})

# Productos
@login_required
def editar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    
    form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

@login_required
def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'productos/confirmar_eliminacion.html', {'producto': producto})

# Proveedores

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    
    return render(request, 'proveedores/crear_proveedor.html', {'form': form})

@login_required
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/listar_proveedores.html', {'proveedores': proveedores})

@login_required
def editar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id=id_proveedor)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'proveedores/editar_proveedor.html', {'form': form, 'proveedor': proveedor})

@login_required
def eliminar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id=id_proveedor)
    
    if request.method == 'POST':
        proveedor.delete()
        return redirect('listar_proveedores')
    
    return render(request, 'proveedores/confirmar_eliminacion_proveedor.html', {'proveedor': proveedor})

# Pedidos
@login_required
def entregar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id=id_pedido)

    if request.method == 'POST':
        # Registrar la fecha de entrega
        pedido.fecha_entrega = timezone.now()  # Puedes cambiar esto si necesitas una fecha específica
        pedido.save()
        return redirect('listar_pedidos')  # Redirige a la lista de pedidos después de entregar

    return render(request, 'pedidos/entregar_pedido.html', {'pedido': pedido})

@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

@login_required
def editar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id=id_pedido)
    
    if request.method == 'POST':
        # Puedes cambiar el formulario según lo que necesites permitir editar
        cantidad = request.POST.get('cantidad')
        pedido.cantidad = cantidad
        pedido.save()
        return redirect('listar_pedidos')
    
    return render(request, 'pedidos/editar_pedido.html', {'pedido': pedido})

@login_required
def eliminar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id=id_pedido)
    
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    
    return render(request, 'pedidos/confirmar_eliminacion_pedido.html', {'pedido': pedido})

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            producto = pedido.producto
            
            # Verificar si hay suficiente stock
            if producto.stock >= pedido.cantidad:
                producto.stock -= pedido.cantidad  # Reducir el stock
                producto.save()  # Guardar el nuevo stock
                pedido.save()  # Guardar el pedido
                return redirect('listar_pedidos')  # Redirigir a la lista de pedidos
            else:
                form.add_error('cantidad', 'No hay suficiente stock disponible.')  # Mensaje de error si no hay stock suficiente

    else:
        form = PedidoForm()
    
    return render(request, 'pedidos/crear_pedido.html', {'form': form})
