from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
from web_project import TemplateLayout
from apps.authentication.models import Usuarios, Rol
from django.views.decorators.csrf import csrf_exempt
import json
from apps.biblioteca.models import Biblioteca_Usuario, PolyaBiblioteca
from apps.authentication.models import Auditoria_Usuario


class GestionUsuariosView(TemplateView):
    template_name = 'gestion_usuarios.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Get search parameters
        search_query = self.request.GET.get('buscar', '')
        rol_filter = self.request.GET.get('rol', '')
        estado_filter = self.request.GET.get('estado')

        # Get all users with role information
        usuarios = Usuarios.objects.select_related('rol').all()

        # Apply filters
        if search_query:
            usuarios = usuarios.filter(
                Q(nombre_usuario__icontains=search_query) |
                Q(usuario_id__icontains=search_query)
            )

        if rol_filter:
            usuarios = usuarios.filter(rol_id=rol_filter)

        # Apply estado filter
        if estado_filter:
            usuarios = usuarios.filter(estado=estado_filter == '1')

        # Get all roles for the filter
        roles = Rol.objects.all()

        # Prepare user data with role information
        usuarios_data = []
        for usuario in usuarios:
            usuarios_data.append({
                'id': usuario.usuario_id,
                'username': usuario.nombre_usuario,
                'rol': usuario.rol.tipo if usuario.rol else 'Sin rol',
                'rol_id': usuario.rol_id,
                'estado': usuario.estado
            })

        # Add data to context
        context.update({
            'usuarios': usuarios_data,
            'roles': [{'rol_id': str(rol.id), 'nombre': rol.tipo} for rol in roles],
            'search_query': search_query,
            'selected_rol': rol_filter,
            'selected_estado': estado_filter if estado_filter is not None else ''
        })

        return context


@require_http_methods(["POST"])
def editar_usuario(request):
    try:
        data = request.POST
        user_id = data.get('user_id')

        if not user_id:
            return JsonResponse({'success': False, 'error': 'ID de usuario no proporcionado'}, status=400)

        try:
            usuario = Usuarios.objects.get(usuario_id=user_id)
        except Usuarios.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)

        # Update user data
        username = data.get('username')
        if username:
            # Check if username exists for other users
            if Usuarios.objects.filter(nombre_usuario=username).exclude(usuario_id=user_id).exists():
                return JsonResponse({'success': False, 'error': 'El nombre de usuario ya está en uso'}, status=400)
            usuario.nombre_usuario = username

        # Update role if provided
        rol_id = data.get('rol')
        if rol_id:
            usuario.rol_id = rol_id

        # Update status
        usuario.estado = data.get('estado') == 'on'

        usuario.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def eliminar_usuario(request):
    try:
        data = request.POST
        user_id = data.get('user_id')

        if not user_id:
            return JsonResponse({'success': False, 'error': 'ID de usuario no proporcionado'}, status=400)

        try:
            usuario = Usuarios.objects.get(usuario_id=user_id)

            # Manual cascade deletion wrapped in try-except to handle missing tables
            try:
                Biblioteca_Usuario.objects.filter(usuario=usuario).delete()
            except Exception:
                pass

            try:
                PolyaBiblioteca.objects.filter(usuario=usuario).delete()
            except Exception:
                pass

            try:
                Auditoria_Usuario.objects.filter(usuario_id=usuario).delete()
            except Exception:
                pass

            usuario.delete()
            return JsonResponse({'success': True})

        except Usuarios.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
