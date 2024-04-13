from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        Modification for Default Serializer to return tokens and user id   
        * Override the inherited .get_token(), .validate() methods
        * when generating/retrieving tokens, the user id will also be returned
        https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html 
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) # calling the base method
        token['id'] = user.id
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['id'] = self.user.id
        return data