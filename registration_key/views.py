import hashlib
import random
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response 
from rest_framework import status 

from properties.models import (
    CondoUnit, 
    ParkingUnit, 
    StorageUnit
)
from user_profile.models import (
    User,
    PublicProfile, 
    CompanyProfile
)
from .models import (
    CondoRegistrationKey, 
    StorageRegistrationKey, 
    ParkingRegistrationKey,
    RegistrationKey
)
from .serializers import (
    CondoRegistrationKeySerializer, 
    ParkingRegistrationKeySerializer, 
    StorageRegistrationKeySerializer
)

class CondoRegistrationKeyView(ModelViewSet):
    """
    Viewset for managing condo registration keys.
    """
    queryset = CondoRegistrationKey.objects.all()
    serializer_class = CondoRegistrationKeySerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new condo registration key.
        
        Parameters:
        - request: The HTTP request object.
        
        Returns:
        - Response: The HTTP response object.
        """
        try:
            unit = CondoUnit.objects.get(id=self.request.data.get('unit', None))
            company = CompanyProfile.objects.get(user_id=self.request.data.get('company', None))
            user = User.objects.get(email=self.request.data.get('user', None))
            
            if unit.public_profile is not None:
                raise Exception("this unit is already in use.")
            if user.role != 'PUBLIC':
                return Response({"details": "The user associated with this email is not a public user"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer_data = {
                'key': CondoRegistrationKey.generate_key(user, unit),
                'user': user.id,
                'unit': unit.id
            }
            
            is_owner = self.request.data.get('is_owner', None)
            
            if is_owner is not None: 
                serializer_data['is_owner'] = is_owner
                
            serializer = CondoRegistrationKeySerializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            company.send_registration_key(serializer.data['key'], user)
            return Response(serializer.data)
        
        except User.DoesNotExist:
            return Response({"details": "There is no user with the given email"}, status=status.HTTP_400_BAD_REQUEST)
        except CondoUnit.DoesNotExist:
            return Response({"details": "There is no condo unit associated with the given id"}, status=status.HTTP_400_BAD_REQUEST)
        except CompanyProfile.DoesNotExist:
            return Response({"details": "There is no Company Profile associated with the given id"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ParkingRegistrationKeyView(ModelViewSet):
    """
    Viewset for managing parking registration keys.
    """
    queryset = ParkingRegistrationKey.objects.all()
    serializer_class = ParkingRegistrationKeySerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new parking registration key.
        
        Parameters:
        - request: The HTTP request object.
        
        Returns:
        - Response: The HTTP response object.
        """
        try:
            unit = ParkingUnit.objects.get(id=self.request.data.get('unit', None))
            company = CompanyProfile.objects.get(user_id=self.request.data.get('company', None))
            user = User.objects.get(email=self.request.data.get('user', None))
            
            if unit.public_profile is not None:
                raise Exception("this unit is already in use.")
            if user.role != 'PUBLIC':
                return Response({"details": "The user associated with this email is not a public user"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer_data = {
                'key': ParkingRegistrationKey.generate_key(user, unit),
                'user': user.id,
                'unit': unit.id
            }
            
            is_owner = self.request.data.get('is_owner', None)
            
            if is_owner is not None: 
                serializer_data['is_owner'] = is_owner
                
            serializer = ParkingRegistrationKeySerializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            company.send_registration_key(serializer.data['key'], user)
            return Response(serializer.data)
        
        except User.DoesNotExist:
            return Response({"details": "There is no user with the given email"}, status=status.HTTP_400_BAD_REQUEST)
        except ParkingUnit.DoesNotExist:
            return Response({"details": "There is no parking unit associated with the given id"}, status=status.HTTP_400_BAD_REQUEST)
        except CompanyProfile.DoesNotExist:
            return Response({"details": "There is no Company Profile associated with the given id"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StorageRegistrationKeyView(ModelViewSet):
    """
    Viewset for managing storage registration keys.
    """
    queryset = StorageRegistrationKey.objects.all()
    serializer_class = StorageRegistrationKeySerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new storage registration key.
        
        Parameters:
        - request: The HTTP request object.
        
        Returns:
        - Response: The HTTP response object.
        """
        try:
            unit = StorageUnit.objects.get(id=self.request.data.get('unit', None))
            company = CompanyProfile.objects.get(user_id=self.request.data.get('company', None))
            user = User.objects.get(email=self.request.data.get('user', None))
            
            if unit.public_profile is not None:
                raise Exception("this unit is already in use.")
            if user.role != 'PUBLIC':
                return Response({"details": "The user associated with this email is not a public user"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer_data = {
                'key': StorageRegistrationKey.generate_key(user, unit),
                'user': user.id,
                'unit': unit.id
            }
            
            is_owner = self.request.data.get('is_owner', None)
            
            if is_owner is not None: 
                serializer_data['is_owner'] = is_owner
                
            serializer = StorageRegistrationKeySerializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            company.send_registration_key(serializer.data['key'], user)
            return Response(serializer.data)
        
        except User.DoesNotExist:
            return Response({"details": "There is no user with the given email"}, status=status.HTTP_400_BAD_REQUEST)
        except StorageUnit.DoesNotExist:
            return Response({"details": "There is no storage unit associated with the given id"}, status=status.HTTP_400_BAD_REQUEST)
        except CompanyProfile.DoesNotExist:
            return Response({"details": "There is no Company Profile associated with the given id"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
