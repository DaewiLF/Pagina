from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from Sistemagestion.models import Producto, Boleta, DetalleBoleta
from Sistemagestion.forms import ProductoForm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

def venta(request):    
    productos = Producto.objects.all()
    return render(request,'Sistemagestion/venta.html', {'productos': productos});

@csrf_exempt
def generar_venta(request):
    if request.method == 'POST':
        #Obtén los datos enviados por el formulario (JSON)
        datos_venta = json.loads(request.body)

        #Crea una nueva boleta
        boleta = Boleta.objects.create(
            fecha=timezone.now(),
            total=datos_venta['total']
        )

        #Guarda los detalles de la boleta
        for producto_id, cantidad in datos_venta['productos'].items():
            producto = Producto.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            DetalleBoleta.objects.create(
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal,
                producto=producto,
                boleta=boleta
            )
            #Actualiza el stock del producto
            producto.stock -= cantidad
            producto.save()

        return HttpResponse("Venta generada con éxito", status=201)
    return HttpResponse("Método no permitido", status=405)

def productos(request):
    #guarda todo los productos de la base de datos
    productos = Producto.objects.all()
    #son guardados en una variable tipo diccionario
    data = {'productos':productos}
    #retornara donde esta la lista de producto con la data
    return render(request,'Sistemagestion/producto_crud.html',data);

def crear_producto(request):
    #verifica si es post
    if request.method == "POST":

        form = ProductoForm(request.POST,request.FILES)#pasamos el formulario a una instancia de producto
        #validamos los parametros del formulario
        if form.is_valid():
            #guardamos los datos
            form.save()
            #redirijimos a la lista de productos
            return redirect('/productos/')
    else:
        #si no valido mostrara nuevamente el formulario de producto
        form = ProductoForm()

    return render(request,'Sistemagestion/crear_producto.html',{'form':form})

#metodo que recibe el id de producto para cargarlos en el formulario
def cargar_editar_producto(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)#rescatamos el id del modelo de producto
    form = ProductoForm(instance=producto)# cargar el producto en el formulario
    data = {
        'form':form,
        'producto':producto,
    }

    #renderizamos el template y los datos
    return render(request,'Sistemagestion/producto_editar.html',data)

# funcion que rescata los valores del formulario y los actualiza en la base de datos
def editar_producto(request,producto_id):
    producto = get_object_or_404(Producto,id=producto_id)#rescatamos el id del modelo de producto

    if request.method == 'POST': #verificamos si la sulicitud llega por POST

        form = ProductoForm(request.POST,request.FILES,instance=producto)#pasamos el formulario a una instancia de producto

        if form.is_valid():#verificamos que cumpla con las validaciones
            form.save() #guardamos los cambios en el formulario
            return redirect('/productos/') #redireccionamos a la tabla producto
    
    else:
        #cargamos los datos de producto
        form = ProductoForm(instance=producto) 
    
    #redireccionamos a la tabla si no llego por post
    return render(request, "Sistemagestion/producto_crud.html",{'form':form})

def eliminar_producto(request, producto_id):
    #Rescatamos el producto que queremos eliminar
    producto = get_object_or_404(Producto, id=producto_id) 
    
    #Cambia este valor por el ID real de producto por defecto
    producto_por_defecto_id = 10000000 

    #Verificamos si la solicitud llega por POST
    if request.method == 'POST': 

        #Actualiza los DetalleBoleta relacionados para que apunten al producto por defecto
        DetalleBoleta.objects.filter(producto=producto).update(producto_id=producto_por_defecto_id)

        #eliminara el producto
        producto.delete()
        
        #Rediriga a la lista de productos
        return redirect('/productos/')

    return render(request, "Sistemagestion/productoDel.html", {"producto": producto})