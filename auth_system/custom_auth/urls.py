from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'auth', views.AuthViewSet, basename='auth')
router.register(r'admin/roles', views.RoleViewSet, basename='role')
router.register(r'admin/resources', views.ResourceViewSet, basename='resource')
router.register(r'admin/permissions', views.PermissionViewSet, basename='permission')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]