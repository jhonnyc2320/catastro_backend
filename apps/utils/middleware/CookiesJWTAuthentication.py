from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        
        if access_token is None:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except InvalidToken as e:
            raise AuthenticationFailed('Token inválido o expirado')
            