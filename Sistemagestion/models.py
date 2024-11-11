from django.db import models

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    edad = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'administrador'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    edad = models.PositiveSmallIntegerField()
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'trabajador'
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'

class Producto(models.Model):
    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('No Disponible', 'No Disponible')
    ]
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES)
    descuento = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Boleta(models.Model):
    fecha = models.DateTimeField()
    trabajador = models.ForeignKey(Trabajador, on_delete=models.SET_NULL, null=True)
    total = models.IntegerField()

    def __str__(self):
        return f"Boleta {self.id} - {self.fecha}"

    class Meta:
        db_table = 'boleta'
        verbose_name = 'Boleta'
        verbose_name_plural = 'Boletas'

class DetalleBoleta(models.Model):
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.IntegerField()
    subtotal = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True,blank=True)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Detalle de Boleta {self.boleta.id} - Producto: {self.producto.nombre}"

    class Meta:
        db_table = 'detalleboleta'
        verbose_name = 'Detalle de Boleta'
        verbose_name_plural = 'Detalles de Boletas'

class InformeCierre(models.Model):
    fecha = models.DateTimeField()
    ventas_total = models.IntegerField()
    stock_actual = models.PositiveIntegerField()
    boletas_emitidas = models.PositiveIntegerField()
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return f"Informe de Cierre {self.fecha}"

    class Meta:
        db_table = 'informecierre'
        verbose_name = 'Informe de Cierre'
        verbose_name_plural = 'Informes de Cierre'

class LogVenta(models.Model):
    TIPO_ACCION_CHOICES = [
        ('Creación', 'Creación'),
        ('Modificación', 'Modificación'),
        ('Eliminación', 'Eliminación')
    ]
    fecha_hora = models.DateTimeField()
    tipo_accion = models.CharField(max_length=15, choices=TIPO_ACCION_CHOICES)
    descripcion = models.TextField()
    informe = models.ForeignKey(InformeCierre, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

    def __str__(self):
        return f"Log de Venta {self.id} - {self.tipo_accion}"

    class Meta:
        db_table = 'logventa'
        verbose_name = 'Log de Venta'
        verbose_name_plural = 'Logs de Venta'