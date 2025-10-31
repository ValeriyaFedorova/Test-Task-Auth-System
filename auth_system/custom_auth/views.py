from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import User, SessionToken, Role, Resource, Permission, UserRole
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer, 
    UserLoginSerializer, RoleSerializer, ResourceSerializer, PermissionSerializer
)
from .authentication import SessionTokenAuthentication
from .permissions import CustomPermission

class AuthViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            if user.check_password(password):
                # Создаем токен сессии
                token = SessionToken.generate_token(user)
                user.last_login = timezone.now()
                user.save()
                
                return Response({
                    "message": "Login successful",
                    "token": token.token,
                    "user": UserProfileSerializer(user).data
                })
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        # Получаем токен из заголовка
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token_key = auth_header[7:]
            try:
                token = SessionToken.objects.get(token=token_key, user=request.user)
                token.is_active = False
                token.save()
            except SessionToken.DoesNotExist:
                pass
        
        return Response({"message": "Logout successful"})
    
    @action(detail=False, methods=['get', 'put'])
    def profile(self, request):
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'])
    def delete_account(self, request):
        user = request.user
        user.is_active = False
        user.save()
        
        # Деактивируем все токены пользователя
        SessionToken.objects.filter(user=user).update(is_active=False)
        
        return Response({"message": "Account deleted successfully"})

# Административные view для управления правами доступа
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [CustomPermission]
    
    def get_resource_name(self, request):
        method = request.method
        if method == 'GET':
            return 'role_management'
        elif method == 'POST':
            return 'role_management'
        return 'role_management'

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [CustomPermission]
    resource_name = 'ResourceManagement'
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'is_superuser') or not self.request.user.is_superuser:
            return Resource.objects.none()
        return Resource.objects.all()

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [CustomPermission]
    resource_name = 'PermissionManagement'
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'is_superuser') or not self.request.user.is_superuser:
            return Permission.objects.none()
        return Permission.objects.select_related('role', 'resource')

# Mock views для бизнес-логики
class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [CustomPermission]
    
    def get_resource_name(self, request):
        # Динамически определяем имя ресурса в зависимости от метода
        method = request.method
        if method == 'GET' and not request.parser_context.get('kwargs'):
            return 'project_list'
        elif method == 'POST':
            return 'project_create'
        elif method == 'PUT':
            return 'project_update'
        elif method == 'DELETE':
            return 'project_delete'
        return 'project_list'
    
    def list(self, request):
        # Устанавливаем resource_name для проверки прав
        request.resource_name = 'project_list'
        return Response({
            "projects": [
                {"id": 1, "name": "Project Alpha", "status": "active"},
                {"id": 2, "name": "Project Beta", "status": "completed"}
            ]
        })
    
    def create(self, request):
        request.resource_name = 'project_create'
        return Response({
            "message": "Project created successfully",
            "project_id": 3
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        request.resource_name = 'project_delete'
        # Здесь должна быть логика удаления проекта
        # Но сначала проверяются права через CustomPermission
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskViewSet(viewsets.ViewSet):
    permission_classes = [CustomPermission]
    
    def get_resource_name(self, request):
        method = request.method
        if method == 'GET' and not request.parser_context.get('kwargs'):
            return 'task_list'
        elif method == 'POST':
            return 'task_create'
        elif method == 'PUT':
            return 'task_update'
        elif method == 'DELETE':
            return 'task_delete'
        return 'task_list'
    
    def list(self, request):
        request.resource_name = 'task_list'
        return Response({
            "tasks": [
                {"id": 1, "title": "Design database", "status": "done"},
                {"id": 2, "title": "Implement API", "status": "in_progress"}
            ]
        })
    
    def create(self, request):
        request.resource_name = 'task_create'
        return Response({
            "message": "Task created successfully",
            "task_id": 3
        }, status=status.HTTP_201_CREATED)