from rest_framework import permissions
from .models import Permission, Resource, UserRole

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Суперпользователь имеет все права
        if hasattr(request.user, 'is_superuser') and request.user.is_superuser:
            return True
        
        # Получаем имя ресурса
        resource_name = getattr(request, 'resource_name', None)
        if not resource_name and hasattr(view, 'get_resource_name'):
            resource_name = view.get_resource_name(request)
        
        if not resource_name:
            # Если ресурс не указан, используем имя view + метод
            resource_name = f"{view.__class__.__name__.lower()}_{request.method.lower()}"
        
        method = request.method
        
        try:
            # Ищем ресурс в базе данных
            resource = Resource.objects.get(name=resource_name, method=method)
        except Resource.DoesNotExist:
            # Если ресурс не найден, запрещаем доступ
            return False
        
        # Получаем все роли пользователя
        user_roles = UserRole.objects.filter(user=request.user).values_list('role_id', flat=True)
        
        # Проверяем, есть ли у любой из ролей пользователя доступ к ресурсу
        has_access = Permission.objects.filter(
            role_id__in=user_roles,
            resource=resource,
            can_access=True
        ).exists()
        
        return has_access