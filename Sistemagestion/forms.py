from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nombre del producto'
        })
    )
    precio = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese precio'
        })
    )
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese cantidad en stock'
        })
    )
    estado = forms.ChoiceField(
        choices=[('Disponible', 'Disponible'), ('No Disponible', 'No Disponible')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    descuento = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese descuento'
        })
    )

    class Meta:
        model = Producto
        fields = '__all__'

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento is not None and (descuento < 0 or descuento > 100):
            raise forms.ValidationError("El descuento debe estar entre 0 y 100.")
        return descuento