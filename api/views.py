from rest_framework import viewsets, permissions
from api.models import Producto, Usuario, Administrador, Venta, ProductoDeseado, tipoCategoria, Carrito, Tienda, SeguimientoTienda
from api.serializers import ProductoSerializer, UsuarioSerializer, UserSerializer, AdministradorSerializer, VentaSerializer, ProductoDeseadoSerializer, tipoCategoriaSerializer, CarritoSerializer, TiendaSerializer, SeguimientoTiendaSerializer
from rest_framework import status,views, response
from rest_framework import authentication
from django.contrib.auth.models import User
from django.contrib.auth import logout ,authenticate, login 
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

class UsuarioLogoutView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Si se usa autenticación basada en tokens propios, aquí se puede invalidar el token.
        return Response({'message': 'Logout exitoso'}, status=200)

class UsuarioLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        correo = request.data.get('correo')
        contrasena = request.data.get('contrasena')
        if not correo or not contrasena:
            return Response({'error': 'Debes enviar correo y contraseña'}, status=400)
        try:
            usuario = Usuario.objects.get(correo=correo)
            # Si guardas contraseñas en texto plano (no recomendado):
            if usuario.contrasena == contrasena:
                # Aquí puedes devolver un token propio, el id, o lo que necesites
                return Response({'message': 'Login exitoso', 'usuario_id': usuario.id}, status=200)
            else:
                return Response({'error': 'Contraseña incorrecta'}, status=401)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)

class ProductoAdminViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(Estado=False)
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [authentication.BasicAuthentication]

    #Obtiene solo Nombre, precio e imagen del producto
    @action(detail=False, methods=['get'])
    def ObtenerProductoMain(self, request):
        producto_id = request.query_params.get('producto_id')
        if not producto_id:
            return Response({'error': 'Debes enviar producto_id'}, status=400)
        try:
            producto = Producto.objects.get(pk=producto_id)
            serializer = ProductoMainSerializer(producto)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
    

    #Actualiza el estado del producto a 1
    @action(detail=True, methods=['patch'])
    def ActualizarEstadoProducto(self, request, pk=None):
        try:
            producto = Producto.objects.get(pk=pk)
            producto.Estado = True
            producto.save()
            tienda = producto.tienda
            tienda.Cant_productos = Producto.objects.filter(tienda=tienda, Estado=True).count()
            tienda.save()
            return Response({'message': 'Estado del producto actualizado exitosamente y cantidad de productos actualizada'}, status=200)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
        
    @action(detail=False, methods=['delete'])
    def EliminarProducto(self, request):
        producto_id = request.data.get('producto_id')
        if not producto_id:
            return Response({'error': 'Debes enviar producto_id'}, status=400)
        try:
            producto = Producto.objects.get(pk=producto_id)
            producto.delete()
            return Response({'message': 'Producto eliminado exitosamente'}, status=200)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(Estado=True)
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [authentication.BasicAuthentication]

    #Obtiene solo Nombre, precio e imagen del producto
    @action(detail=False, methods=['get'])
    def ObtenerProductoMain(self, request):
        producto_id = request.query_params.get('producto_id')
        if not producto_id:
            return Response({'error': 'Debes enviar producto_id'}, status=400)
        try:
            producto = Producto.objects.get(pk=producto_id)
            serializer = ProductoMainSerializer(producto)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
    
    @action(detail=False, methods=['get'])
    def ObtenerProductosPorTienda(self, request):
        tienda_id = request.query_params.get('tienda_id')
        if not tienda_id:
            return Response({'error': 'Debes enviar tienda_id'}, status=400)
        try:
            tienda = Tienda.objects.get(pk=tienda_id)
            productos = Producto.objects.filter(tienda=tienda)
            serializer = self.get_serializer(productos, many=True)
            return Response(serializer.data)
        except Tienda.DoesNotExist:
            return Response({'error': 'Tienda no encontrada'}, status=404)

    @action(detail=False, methods=['get'])
    def ObtenerProductosCarrito(self, request):
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Debes enviar usuario_id'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            carrito = Carrito.objects.filter(usuario=usuario)
            serializer = CarritoSerializer(carrito, many=True)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
    
    #Actualiza el estado del producto a 1
    @action(detail=False, methods=['patch'])
    def ActualizarEstadoProducto(self, request):
        producto_id = request.data.get('producto_id')
        if not producto_id:
            return Response({'error': 'Debes enviar producto_id'}, status=400)
        try:
            producto = Producto.objects.get(pk=producto_id)
            producto.Estado = True
            producto.save()
            return Response({'message': 'Estado del producto actualizado exitosamente'}, status=200)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
            

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.BasicAuthentication,]

    @action(detail=False, methods=['get'])
    def ListaUsuarios(self, request):
        usuarios = Usuario.objects.all()
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def CambiarContrasena(self, request):
        usuario_id = request.data.get('usuario_id')
        nueva_contrasena = request.data.get('nueva_contrasena')
        if not usuario_id or not nueva_contrasena:
            return Response({'error': 'Debes enviar usuario_id y nueva_contrasena'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            usuario.contrasena = nueva_contrasena
            usuario.save()
            return Response({'message': 'Contraseña actualizada exitosamente'}, status=200)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        
    @action(detail=False, methods=['post'])
    def CrearUsuario(self, request):  
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido', '')
        foto = request.FILES.get('foto', None)
        correo = request.data.get('correo')
        contrasena = request.data.get('contrasena')
        if not nombre or not correo or not contrasena:
            return Response({'error': 'Debes enviar nombre, correo y contraseña'}, status=400)
        try:
            usuario, created = Usuario.objects.get_or_create(correo=correo)
            if created:
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.foto = foto
                usuario.contrasena = contrasena
                usuario.save()  # <-- GUARDAR EL USUARIO PRIMERO
                
                # Crear un carrito asignado al usuario
                Carrito.objects.create(usuario=usuario)  # <-- CREAR CARRITO ANTES DEL RETURN
                
                return Response({'success': 'Usuario creado correctamente'}, status=201)  # <-- AHORA SÍ RETURN
            else:
                return Response({'error': 'El usuario ya existe'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    @action(detail=False, methods=['post'])

# Si quieres editar un usuario existente, puedes usar este método
# Si no se ingresa foto, nombre o apellido, se mantendrá lo actual
    def EditarUsuario(self, request):
        usuario_id = request.data.get('usuario_id')
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido', '')
        foto = request.FILES.get('foto', None)

        if not usuario_id or not nombre:
            return Response({'error': 'Debes enviar usuario_id y nombre'}, status=400)

        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            usuario.nombre = nombre if nombre else usuario.foto
            usuario.apellido = apellido if apellido else usuario.apellido
            usuario.foto = foto if foto else usuario.foto  # Mantener la foto actual si no se proporciona una nueva
            usuario.save()
            return Response({'message': 'Usuario actualizado exitosamente'}, status=200)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        
    

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.BasicAuthentication,]

    @action(detail=False, methods=['post'])
    def AutenticacionarAdministrador(self, request):
        correo = request.data.get('correo')
        contrasena = request.data.get('contrasena')
        if not correo or not contrasena:
            return Response({'error': 'Debes enviar correo y contrasena'}, status=400)
        try:
            administrador = Administrador.objects.get(correo=correo, contrasena=contrasena)
            return Response({'message': 'Administrador autenticado exitosamente'}, status=200)
        except Administrador.DoesNotExist:
            return Response({'error': 'Administrador no encontrado o credenciales incorrectas'}, status=404)

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.BasicAuthentication,]

class ProductoDeseadoViewSet(viewsets.ModelViewSet):
    queryset = ProductoDeseado.objects.all()
    serializer_class = ProductoDeseadoSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.BasicAuthentication,]

    @action(detail=False, methods=['get'])
    def ObtenerListaDeseadosPorUsuario(self, request):
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Debes enviar usuario_id'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            productos_deseados = ProductoDeseado.objects.filter(usuario=usuario)
            serializer = self.get_serializer(productos_deseados, many=True)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
    
    @action(detail=False, methods=['get'])
    def ObtenerListaUsuariosQueDeseanProducto(self, request, pk=None):
        producto_id = request.query_params.get('producto_id')
        if not producto_id:
            return Response({'error': 'Debes enviar producto_id'}, status=400)
        try:
            producto = Producto.objects.get(pk=producto_id)
            usuarios_desean = ProductoDeseado.objects.filter(producto=producto)
            serializer = self.get_serializer(usuarios_desean, many=True)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def AgregarProductoDeseado(self, request):
        usuario_id = request.data.get('usuario_id')
        producto_id = request.data.get('producto_id')
        if not usuario_id or not producto_id:
            return Response({'error': 'Debes enviar usuario_id y producto_id'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            producto = Producto.objects.get(pk=producto_id)
            deseado, created = ProductoDeseado.objects.get_or_create(usuario=usuario, producto=producto)
            if created:
                return Response({'message': 'Producto agregado a deseos exitosamente'}, status=201)
            else:
                return Response({'message': 'El producto ya está en la lista de deseos'}, status=200)
        except (Usuario.DoesNotExist, Producto.DoesNotExist):
            return Response({'error': 'Usuario o Producto no encontrado'}, status=404)
    
    @action(detail=False, methods=['DELETE'])
    def EliminarProductoDeseado(self, request):
        usuario_id = request.data.get('usuario_id')
        producto_id = request.data.get('producto_id')
        if not usuario_id or not producto_id:
            return Response({'error': 'Debes enviar usuario_id y producto_id'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            producto = Producto.objects.get(pk=producto_id)
            deseado = ProductoDeseado.objects.filter(usuario=usuario, producto=producto).first()
            if deseado:
                deseado.delete()
                return Response({'message': 'Producto eliminado de deseos exitosamente'}, status=200)
            else:
                return Response({'message': 'El producto no está en la lista de deseos'}, status=404)
        except (Usuario.DoesNotExist, Producto.DoesNotExist):
            return Response({'error': 'Usuario o Producto no encontrado'}, status=404)

class tipoCategoriaViewSet(viewsets.ModelViewSet):
    queryset = tipoCategoria.objects.all()
    serializer_class = tipoCategoriaSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.BasicAuthentication,]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser,]
    authentication_classes = [authentication.BasicAuthentication,]

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()  # Assuming you want to list products in the cart
    serializer_class = ProductoSerializer
    #permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [authentication.BasicAuthentication,]

    @action(detail=False, methods=['post'])
    def AgAlCarrito(self, request):
        if request.method == 'POST':
            usuario_id = request.data.get('usuario_id')
            producto_id = request.data.get('producto_id')
            unidades = request.data.get('unidades', 1)
            if not usuario_id or not producto_id:
                return Response({'error': 'Debes enviar usuario_id y producto_id'}, status=400)
            try:
                usuario = Usuario.objects.get(pk=usuario_id)
                producto = Producto.objects.get(pk=producto_id)
                carrito, created = Carrito.objects.get_or_create(usuario=usuario, producto=producto)
                if created:
                    carrito.unidades = unidades
                    carrito.valortotal = producto.Precio * unidades
                    carrito.save()
                    return Response({'message': 'Producto agregado al carrito exitosamente'}, status=201)
                else:
                    carrito.unidades += unidades
                    carrito.valortotal += producto.Precio * unidades
                    carrito.save()
                    return Response({'message': 'Producto actualizado en el carrito'}, status=200)
            except (Usuario.DoesNotExist, Producto.DoesNotExist):
                return Response({'error': 'Usuario o Producto no encontrado'}, status=404)
        return Response({'error': 'Método no permitido'}, status=405)

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()  # Assuming you want to list products in the store
    serializer_class = TiendaSerializer 
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.BasicAuthentication,]

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        nombre = request.query_params.get('nombre', None)
        if nombre:
            tiendas = Tienda.objects.filter(nombre__icontains=nombre)
        else:
            tiendas = Tienda.objects.all()
        serializer = self.get_serializer(tiendas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ObtenerImgNomTiendaPorProducto(self, request):
        producto_id = request.query_params.get('producto_id')
        if not producto_id:
            return Response({'error': 'Debes enviar producto_id'}, status=400)
        try:
            producto = Producto.objects.get(pk=producto_id)
            tienda = producto.tienda
            data = {
                'nombre': tienda.NomTienda,
                'imagen': tienda.Logo.url if tienda.Logo else None
            }
            return Response(data)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
        except AttributeError:
            return Response({'error': 'El modelo Tienda debe tener un campo imagen'}, status=500)
        
    @action(detail=False, methods=['get'])
    def ObtenerTiendaPorPropietario(self, request):
        propietario_id = request.query_params.get('propietario_id')
        if not propietario_id:
            return Response({'error': 'Debes enviar propietario_id'}, status=400)
        try:
            tienda = Tienda.objects.get(Propietario=propietario_id)
            serializer = self.get_serializer(tienda)
            return Response(serializer.data)
        except Tienda.DoesNotExist:
            return Response({'error': 'Tienda no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def CrearTienda(self, request):
        propietario_id = request.data.get('propietario_id')
        nombre_tienda = request.data.get('nombre_tienda')
        descripcion_tienda = request.data.get('descripcion_tienda', '')
        logo = request.FILES.get('logo', None)

        if not propietario_id or not nombre_tienda:
            return Response({'error': 'Debes enviar propietario_id y nombre_tienda'}, status=400)

        try:
            propietario = Usuario.objects.get(pk=propietario_id)
            tienda, created = Tienda.objects.get_or_create(Propietario=propietario, NomTienda=nombre_tienda)
            if created:
                tienda.DescripcionTienda = descripcion_tienda
                tienda.Logo = logo
                tienda.save()
                return Response({'message': 'Tienda creada exitosamente'}, status=201)
            else:
                return Response({'message': 'La tienda ya existe'}, status=200)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
    
    @action(detail=False, methods=['get'])
    def ObtenerDetallesTienda(self, request):
        tienda_id = request.query_params.get('tienda_id')
        if not tienda_id:
            return Response({'error': 'Debes enviar tienda_id'}, status=400)
        try:
            tienda = Tienda.objects.get(pk=tienda_id)
            serializer = self.get_serializer(tienda)
            return Response(serializer.data)
        except Tienda.DoesNotExist:
            return Response({'error': 'Tienda no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'])
    def EditarTienda(self, request):
        tienda_id = request.data.get('tienda_id')
        nombre_tienda = request.data.get('nombre_tienda')
        descripcion_tienda = request.data.get('descripcion_tienda', '')
        logo = request.FILES.get('logo', None)

        if not tienda_id or not nombre_tienda:
            return Response({'error': 'Debes enviar tienda_id y nombre_tienda'}, status=400)

        try:
            tienda = Tienda.objects.get(pk=tienda_id)
            tienda.NomTienda = nombre_tienda if nombre_tienda else tienda.NomTienda
            tienda.DescripcionTienda = descripcion_tienda if descripcion_tienda else tienda.DescripcionTienda
            if logo:
                tienda.Logo = logo
            else:
                tienda.Logo = tienda.Logo
            tienda.save()
            return Response({'message': 'Tienda actualizada exitosamente'}, status=200)
        except Tienda.DoesNotExist:
            return Response({'error': 'Tienda no encontrada'}, status=404)
        
class SeguimientoTiendaViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoTienda.objects.all()  # Assuming you want to track products in the store
    serializer_class = SeguimientoTiendaSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.BasicAuthentication,]

    @action(detail=False, methods=['get'])
    def ObtenerListaTiendasSeguidasPorUsuario(self, request):
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({'error': 'Debes enviar usuario_id'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            tiendas_seguidas = SeguimientoTienda.objects.filter(usuario=usuario)
            serializer = self.get_serializer(tiendas_seguidas, many=True)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        
    @action(detail=False, methods=['get'])
    def ObtenerListaUsuarioQueSiguenTienda(self, request, pk=None):
        tienda_id = request.query_params.get('tienda_id')
        if not tienda_id:
            return Response({'error': 'Debes enviar tienda_id'}, status=400)    
        try:
            tienda = Tienda.objects.get(pk=tienda_id)
            seguidores = SeguimientoTienda.objects.filter(tienda=tienda)
            serializer = self.get_serializer(seguidores, many=True)
            return Response(serializer.data)
        except Tienda.DoesNotExist:
            return Response({'error': 'Tienda no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])   
    def AgregarSeguimientoTienda(self, request):
        usuario_id = request.data.get('usuario_id')
        tienda_id = request.data.get('tienda_id')
        if not usuario_id or not tienda_id:
            return Response({'error': 'Debes enviar usuario_id y tienda_id'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            tienda = Tienda.objects.get(pk=tienda_id)
            seguimiento, created = SeguimientoTienda.objects.get_or_create(usuario=usuario, tienda=tienda)
            #Subir la cantidad de seguidores de la tienda
            if seguimiento.tienda:
                seguimiento.tienda.CantidadSeguidores += 1
                seguimiento.tienda.save()
            if created:
                return Response({'message': 'Ahora sigues la tienda exitosamente'}, status=201)
            else:
                return Response({'message': 'Ya sigues esta tienda'}, status=200)
        except (Usuario.DoesNotExist, Tienda.DoesNotExist):
            return Response({'error': 'Usuario o Tienda no encontrado'}, status=404)

    @action(detail=False, methods=['DELETE'])
    def DejarDeSeguirTienda(self, request):
        usuario_id = request.data.get('usuario_id')
        tienda_id = request.data.get('tienda_id')
        if not usuario_id or not tienda_id:
            return Response({'error': 'Debes enviar usuario_id y tienda_id'}, status=400)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            tienda = Tienda.objects.get(pk=tienda_id)
            seguimiento = SeguimientoTienda.objects.filter(usuario=usuario, tienda=tienda).first()
            if seguimiento:
                seguimiento.delete()
                return Response({'message': 'Has dejado de seguir la tienda exitosamente'}, status=200)
            else:
                return Response({'message': 'No estabas siguiendo esta tienda'}, status=404)
        except (Usuario.DoesNotExist, Tienda.DoesNotExist):
            return Response({'error': 'Usuario o Tienda no encontrado'}, status=404)

            

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # Recuperamos las credenciales y autenticamos al usuario
        username2= request.data.get('username', None)
        password2 = request.data.get('password', None)
        if username2 is None or password2 is None:
            return response.Response({'message': 'Please provide both username and password'},status=status.HTTP_400_BAD_REQUEST)
        user2 = authenticate(username=username2, password=password2)
        if not user2:
            return response.Response({'message': 'Usuario o Contraseña incorrecto !!!! '},status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user2)
        # Si es correcto añadimos a la request la información de sesión
        if user2:
            # para loguearse una sola vez
            # login(request, user)
            return response.Response({'message':'usuario y contraseña correctos!!!!'},status=status.HTTP_200_OK)
            #return response.Response({'token': token.key}, status=status.HTTP_200_OK)

        # Si no es correcto devolvemos un error en la petición
        return response.Response(status=status.HTTP_404_NOT_FOUND)        

class LogoutView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    def post(self, request):        
        request.user.auth_token.delete()
        # Borramos de la request la información de sesión
        logout(request)
        # Devolvemos la respuesta al cliente
        return response.Response({'message':'Sessión Cerrada y Token Eliminado !!!!'},status=status.HTTP_200_OK)

