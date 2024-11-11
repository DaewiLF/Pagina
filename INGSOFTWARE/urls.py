
from django.contrib import admin
from django.urls import path
from Sistemagestion import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.venta, name='venta'),
    path('generar-venta/', views.generar_venta, name='generar_venta'), 
    path('productos/',views.productos,name='productos'),
    path('producto/',views.crear_producto,name='crear_producto'),
    path('productoedit/<int:producto_id>/',views.cargar_editar_producto,name='editarProducto'),
    path('productoEditado/<int:producto_id>/',views.editar_producto,name='productoEditado'),
    path('productoDel/<int:producto_id>/',views.eliminar_producto,name='productoDel'),

]
