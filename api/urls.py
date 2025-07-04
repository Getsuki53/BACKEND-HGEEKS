from rest_framework import routers
from api.views import ProductoViewSet, UsuarioViewSet, UserViewSet, LogoutView , LoginView, AdministradorViewSet, VentaViewSet, ProductoDeseadoViewSet, tipoCategoriaViewSet, CarritoViewSet, TiendaViewSet, SeguimientoTiendaViewSet, ProductoAdminViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
router  = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet)
router.register('administrador', AdministradorViewSet)
router.register('Venta', VentaViewSet)
router.register('productodeseado', ProductoDeseadoViewSet)
router.register('tipocategoria', tipoCategoriaViewSet)
router.register('user', UserViewSet)
router.register('carrito', CarritoViewSet)
router.register('tienda', TiendaViewSet)
router.register('seguimientotienda', SeguimientoTiendaViewSet)
router.register('producto', ProductoViewSet, basename='producto')
router.register('productoadmin', ProductoAdminViewSet, basename='productoadmin')



urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('login-usuario/', UsuarioLoginView.as_view()),
    path('logout-usuario/', UsuarioLogoutView.as_view()),
] + router.urls
