from django.db import models 
import datetime

class tipoCategoria(models.Model):
    NomCat = models.CharField(max_length=100, primary_key= True, verbose_name='Nombre de Categoria')

    def __str__(self):
        return self.NomCat
# Create your models here.
class Persona(models.Model):
    correo = models.EmailField('Correo', blank=True)
    contrasena = models.CharField('Contraseña', max_length = 100)
    #class Meta:
    #    abstract = True

class Usuario(Persona):
    nombre = models.CharField('Nombre', max_length = 100)
    apellido = models.CharField('Apellido', default="vacio_", max_length = 100)
    foto = models.ImageField(null=True, blank=True, upload_to='fotos/')

    def __str__(self):  
        return '{0},{1}'.format(self.apellido,self.nombre)
    
class Administrador(Persona):

    def __str__(self):  
        return '{0}'.format(self.correo)
    
class Tienda(models.Model):
    Propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Propietario', null=False,unique=True)
    NomTienda = models.CharField(max_length=200)
    Logo = models.ImageField(null=True, blank=True, upload_to='logos/')
    DescripcionTienda = models.TextField(blank=True)
    Cant_productos = models.PositiveIntegerField(default=0)
    Cant_seguidores = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.NomTienda
    def ActualizarCantidadProductos(self):
        self.Cant_productos = Producto.objects.filter(tienda=self).count()
        self.save()
        

class Producto(models.Model):
    Nomprod = models.CharField(max_length=200)
    DescripcionProd = models.CharField(blank=True, max_length=200)
    Stock = models.PositiveIntegerField(default=0)
    FotoProd = models.ImageField(null=False, blank=False, upload_to='images/', default='images/default-product.jpg')
    Precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipoCategoria = models.ForeignKey('tipoCategoria', on_delete=models.CASCADE, verbose_name='Tipo de Categoria', null=False)   
    Estado = models.BooleanField(default=False)  
    FechaPub = models.DateTimeField(default=datetime.datetime.now)
    tienda= models.ForeignKey(Tienda, on_delete=models.CASCADE, verbose_name='Tienda', null=False)
    # create_at = models.DateTimeField(default=datetime.datetime.now)
    def __str__ (self):
        return self.Nomprod
    
    
    


class Venta(models.Model):
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario', null=False)
    productoComprado = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto', null=False)
    cantidad = models.PositiveIntegerField(default=0)
    fecha = models.DateTimeField(default=datetime.datetime.now)

    
    def __str__(self):
        return f'{self.comprador} compró {self.productoComprado}'

    class Meta:
        indexes = [
                models.Index(fields=['comprador', 'productoComprado',]),
            ]
        
class ProductoDeseado(models.Model): 
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario', null=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto', null=False)

    def __str__(self):
        return f'{self.usuario} desea {self.producto}'
    
    class Meta:
        indexes = [
                models.Index(fields=['usuario', 'producto',]),
            ]
    
class SeguimientoTienda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario', null=False)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, verbose_name='Tienda', null=False)

    def __str__(self):
        return f'{self.usuario} sigue a {self.tienda}'
    
    class Meta:
        indexes = [
                models.Index(fields=['usuario', 'tienda',]),
            ]
        
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario', null=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto', null=False)
    unidades = models.PositiveIntegerField(default=1)
    valortotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.usuario} tiene {self.unidades} de {self.producto} en el carrito'
    

    
    class Meta:
        indexes = [
                models.Index(fields=['usuario', 'producto',]),
            ]
        