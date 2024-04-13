from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from registration_key.models import (
    CondoRegistrationKey,
    ParkingRegistrationKey,
    StorageRegistrationKey
)
from .models import (
    User, 
    Profile, 
    PublicProfile, 
    EmployeeProfile, 
    CompanyProfile
    )
from properties.serializers import (
    CondoUnitSerializer, 
    ParkingUnitSerializer, 
    StorageUnitSerializer
    )
from .serializers import (
    UserSerializer, 
    PublicProfileSerializer, 
    EmployeeProfileSerializer, 
    CompanyProfileSerializer
    )


"""
    ViewSets For CRUD Operations on the PublicProfile, CompanyProfile, EmployeeProfile and User models 
    
     * inherited methods: 
            .list(), .retrieve(), .create(), .update(),
            .partial_update(), and .destroy()
            
        https://www.django-rest-framework.org/api-guide/viewsets/ 
        
"""


class UserViewSet(ModelViewSet):
    """
        ViewSet for the User Model  
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
class PublicProfileViewSet(ModelViewSet):
    """
    A ViewSet for managing public profiles.
    """
    queryset = PublicProfile.objects.all()
    serializer_class = PublicProfileSerializer
    lookup_field = 'user'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    """  
    List the various units 
    """
    def get_condo_units(self, request, **kwargs):
        """
        Retrieve the condo units associated with a user.

        Args:
            request (HttpRequest): The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object containing the serialized condo units.

        Raises:
            Http404: If the user or condo units are not found.
        """
        user_id = self.kwargs.get('user_id', None)
        if not user_id:
            return Response({"error": "Missing user_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = PublicProfile.objects.get(user_id=user_id)
        except PublicProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if not profile.condo_units:
            return Response({"error": "No condo units found for this user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CondoUnitSerializer(profile.condo_units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_parking_units(self, request, **kwargs):
        """
        Retrieve the parking units associated with a user.

        Args:
            request (HttpRequest): The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object containing the serialized parking units.

        Raises:
            Http404: If the user or parking units are not found.
        """
        user_id = self.kwargs.get('user_id', None)
        if not user_id:
            return Response({"error": "Missing user_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = PublicProfile.objects.get(user_id=user_id)
        except PublicProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if not profile.parking_units:
            return Response({"error": "No parking units found for this user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ParkingUnitSerializer(profile.parking_units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_storage_units(self, request, **kwargs):
        """
        Retrieve the storage units associated with a user.

        Args:
            request (HttpRequest): The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object containing the serialized storage units.

        Raises:
            Http404: If the user or storage units are not found.
        """
        user_id = self.kwargs.get('user_id', None)
        if not user_id:
            return Response({"error": "Missing user_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = PublicProfile.objects.get(user_id=user_id)
        except PublicProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if not profile.storage_units:
            return Response({"error": "No storage units found for this user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StorageUnitSerializer(profile.storage_units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def register_condo(self, request, **kwargs):
        """
        Register a condo unit for a user.

        Args:
            request (HttpRequest): The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object indicating the success of the registration.

        Raises:
            Http404: If the registration key or user is not found.
        """
        key = request.data.get('key')
        user = request.data.get('user')
        key = CondoRegistrationKey.objects.get(key=key)
        user = User.objects.get(id=user)
        
        if key.user.user_id is not user.id:
            return Response({"details":"This registration key is not valid for you"}, status=status.HTTP_400_BAD_REQUEST)
        unit = key.unit
        unit.public_profile = PublicProfile.objects.get(user=user)
        unit.save()
        return Response(status=status.HTTP_200_OK)
    
    def register_parking(self, request, **kwargs):
        """
        Register a parking unit for a user.

        Args:
            request (HttpRequest): The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object indicating the success of the registration.

        Raises:
            Http404: If the registration key or user is not found.
        """
        key = request.data.get('key')
        user = request.data.get('user')
        key = ParkingRegistrationKey.objects.get(key=key)
        user = User.objects.get(id=user)
        
        if key.user.user_id is not user.id:
            return Response({"details":"This registration key is not valid for you"}, status=status.HTTP_400_BAD_REQUEST)
        unit = key.unit
        unit.public_profile = PublicProfile.objects.get(user=user)
        unit.save()
        return Response(status=status.HTTP_200_OK)
        
    def register_storage(self, request, **kwargs):
        """
        Register a storage unit for a user.

        Args:
            request (HttpRequest): The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response object indicating the success of the registration.

        Raises:
            Http404: If the registration key or user is not found.
        """
        key = request.data.get('key')
        user = request.data.get('user')
        key = StorageRegistrationKey.objects.get(key=key)
        user = User.objects.get(id=user)
        
        if key.user.user_id is not user.id:
            return Response({"details":"This registration key is not valid for you"}, status=status.HTTP_400_BAD_REQUEST)
        unit = key.unit
        unit.public_profile = PublicProfile.objects.get(user=user)
        unit.save()
        return Response(status=status.HTTP_200_OK)
        
        
    
    
class EmployeeProfileViewSet(ModelViewSet):
    """
        ViewSet for the Employee Profile  
    """
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    lookup_field = 'user'       
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
class CompanyProfileViewSet(ModelViewSet):
    """
        ViewSet for the Company Profile
    """
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    lookup_field = 'user'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

