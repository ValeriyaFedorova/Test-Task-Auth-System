from django.utils.deprecation import MiddlewareMixin
from .models import SessionToken
from datetime import datetime

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Пропускаем аутентификацию для admin и статических файлов
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return None
            
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header and auth_header.startswith('Bearer '):
            token_key = auth_header[7:]
            try:
                token = SessionToken.objects.select_related('user').get(
                    token=token_key,
                    is_active=True
                )
                
                if token.is_valid():
                    request.user = token.user
                else:
                    request.user = None
                    
            except SessionToken.DoesNotExist:
                request.user = None
        else:
            request.user = None