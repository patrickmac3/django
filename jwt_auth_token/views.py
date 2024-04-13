from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

class BlackListTokenView(APIView):
    """
        Black List Used JWT tokens 
        * Post Method
        * data: refresh_token 
        * anyone can access this view
        https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html
        
    """
    permission_classes = [AllowAny]
    
    def post(self, request:Request):
        try:
            refresh_token = request.data['refresh_token']
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Tokens successfully blacklisted"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)