from django import forms
from .models import Proveedor, Producto, Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'proveedor']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['producto', 'cantidad']

    # Opcional: Personalizar el widget para el campo de producto
    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0)  # Solo productos en stock
        
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user