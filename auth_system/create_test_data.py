import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_system.settings')
django.setup()

from custom_auth.models import User, Role, Resource, Permission, UserRole

def create_test_data():
    print("Creating test data...")
    
    # Очистка старых данных (опционально)
    User.objects.all().delete()
    Role.objects.all().delete()
    Resource.objects.all().delete()
    
    # Создаем суперпользователя
    admin_user, created = User.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'first_name': 'Admin',
            'last_name': 'User',
            'is_superuser': True,
            'is_active': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f'Created admin user: {admin_user.email}')

    # Создаем обычного пользователя
    regular_user, created = User.objects.get_or_create(
        email='user@example.com',
        defaults={
            'first_name': 'Regular',
            'last_name': 'User',
            'is_active': True
        }
    )
    if created:
        regular_user.set_password('user123')
        regular_user.save()
        print(f'Created regular user: {regular_user.email}')

    # Создаем роли
    roles_data = [
        ('admin', 'Administrator role'),
        ('manager', 'Project manager role'),
        ('user', 'Regular user role'),
        ('guest', 'Guest user role'),
    ]
    
    roles = {}
    for name, description in roles_data:
        role, created = Role.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        roles[name] = role
        if created:
            print(f'Created role: {name}')

    # Назначаем роли пользователям
    UserRole.objects.get_or_create(user=admin_user, role=roles['admin'])
    UserRole.objects.get_or_create(user=regular_user, role=roles['user'])

    # Создаем ресурсы - теперь с уникальными комбинациями name+method
    resources_data = [
        ('project_list', 'GET', 'View projects'),
        ('project_create', 'POST', 'Create project'),
        ('project_update', 'PUT', 'Update project'),
        ('project_delete', 'DELETE', 'Delete project'),
        ('task_list', 'GET', 'View tasks'),
        ('task_create', 'POST', 'Create task'),
        ('task_update', 'PUT', 'Update task'),
        ('task_delete', 'DELETE', 'Delete task'),
        ('role_management', 'GET', 'View roles'),
        ('role_management', 'POST', 'Create role'),
        ('resource_management', 'GET', 'View resources'),
        ('permission_management', 'GET', 'View permissions'),
    ]

    resources = {}
    for name, method, description in resources_data:
        resource, created = Resource.objects.get_or_create(
            name=name,
            method=method,
            defaults={'description': description}
        )
        resources[f"{name}_{method}"] = resource
        if created:
            print(f'Created resource: {name} {method}')

    # Создаем разрешения для админа (все права)
    for resource in Resource.objects.all():
        Permission.objects.get_or_create(
            role=roles['admin'],
            resource=resource,
            defaults={'can_access': True}
        )

    # Создаем разрешения для обычного пользователя
    user_permissions = [
        ('project_list', 'GET'),
        ('project_create', 'POST'),
        ('task_list', 'GET'),
        ('task_create', 'POST'),
    ]
    
    for resource_name, method in user_permissions:
        resource_key = f"{resource_name}_{method}"
        if resource_key in resources:
            Permission.objects.get_or_create(
                role=roles['user'],
                resource=resources[resource_key],
                defaults={'can_access': True}
            )

    print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data()