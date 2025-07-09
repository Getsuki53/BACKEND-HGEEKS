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
            # Si ya es una URL completa, devolverla tal como está
            if obj.FotoProd.url.startswith('http'):
                return obj.FotoProd.url
            # Si no, agregar el dominio de Cloudinary
            return f"https://res.cloudinary.com/devfncp85/{obj.FotoProd.url}"
        return None

class ProductoMainSerializer(serializers.ModelSerializer):
    FotoProd = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['Nomprod', 'Precio', 'FotoProd']
    
    def get_FotoProd(self, obj):
        if obj.FotoProd:
            if obj.FotoProd.url.startswith('http'):
                return obj.FotoProd.url
            return f"https://res.cloudinary.com/devfncp85/{obj.FotoProd.url}"
        return None

# Hacer lo mismo para UsuarioSerializer y TiendaSerializer
class UsuarioSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = '__all__'
    
    def get_foto(self, obj):
        if obj.foto:
            if obj.foto.url.startswith('http'):
                return obj.foto.url
            return f"https://res.cloudinary.com/devfncp85/{obj.foto.url}"
        return None

class TiendaSerializer(serializers.ModelSerializer):
    Logo = serializers.SerializerMethodField()
    
    class Meta:
        model = Tienda
        fields = '__all__'
    
    def get_Logo(self, obj):
        if obj.Logo:
            if obj.Logo.url.startswith('http'):
                return obj.Logo.url
            return f"https://res.cloudinary.com/devfncp85/{obj.Logo.url}"
        return None

# Resto de tus serializers...
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

class SeguimientoTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientoTienda
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'groups', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
