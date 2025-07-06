from rest_framework import serializers
from api.models import Producto, Persona, Usuario, Administrador, Venta, ProductoDeseado, tipoCategoria, Carrito, Tienda, SeguimientoTienda
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ProductoSerializer(serializers.ModelSerializer):
    FotoProd = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def get_FotoProd(self, obj):
        if obj.FotoProd:
            return obj.FotoProd.url
        return '/media/images/default-product.jpg'  # URL por defecto

class ProductoMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['Nomprod', 'Precio', 'FotoProd']

class ProductoCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [ Producto.Nomprod, Producto.Precio, Producto.FotoProd, Producto.Stock]


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class ProductoDeseadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoDeseado
        fields = '__all__'

class tipoCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = tipoCategoria
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'

class SeguimientoTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientoTienda
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'groups', 'email']
         #esconder password
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
