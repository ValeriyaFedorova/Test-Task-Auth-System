from django.contrib import admin
from .models import User, Role, UserRole, Resource, Permission, SessionToken

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'created_at']
    list_filter = ['is_active', 'is_superuser', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'method', 'description']
    list_filter = ['method']
    search_fields = ['name']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'resource', 'can_access', 'created_at']
    list_filter = ['role', 'can_access', 'created_at']

@admin.register(SessionToken)
class SessionTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_active', 'created_at', 'expires_at']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['token']