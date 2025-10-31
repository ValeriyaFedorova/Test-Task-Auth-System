from rest_framework import authentication
from rest_framework import exceptions
from .models import SessionToken, User
from datetime import datetime

class SessionTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token_key = request.META.get('HTTP_AUTHORIZATION')
        
        if not token_key:
            return None
        
        # Убираем префикс "Bearer " если есть
        if token_key.startswith('Bearer '):
            token_key = token_key[7:]
        
        try:
            token = SessionToken.objects.select_related('user').get(
                token=token_key,
                is_active=True
            )
            
            if not token.is_valid():
                raise exceptions.AuthenticationFailed('Token expired')
            
            if not token.user.is_active:
                raise exceptions.AuthenticationFailed('User inactive')
            
            return (token.user, token)
            
        except SessionToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')