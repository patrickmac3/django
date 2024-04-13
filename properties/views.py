
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import PropertyProfile, CondoUnit, ParkingUnit, StorageUnit
from .serializers import PropertyProfileSerializer, CondoUnitSerializer, StorageUnitSerializer, ParkingUnitSerializer
from user_profile.models import CompanyProfile
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class PropertyProfileViewSet(ModelViewSet):
    """  
        View Set for Property Profile model 
    """
    queryset = PropertyProfile.objects.all()
    serializer_class = PropertyProfileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def list(self, request, **kwargs):
        """  
            overriding the inherites .list() method 
            *
            * 2 possible listings
            *      1. profiles/company-profile/<int:company_id>/properties/
            *          - list property profiles related to this company profile
            *      2. properties/property-profile/
            *          - list all property profiles ModelViewSet base .list() method
            *
        """
        company_id = self.kwargs.get('company_id', None)
        if company_id:
            try:
                company = CompanyProfile.objects.get(user_id=company_id)
                properties = PropertyProfile.objects.filter(company=company)
                serializer = PropertyProfileSerializer(properties, many=True)
                return Response(serializer.data)
            except CompanyProfile.DoesNotExist:
                return Response({"details":"Company Profile does not exist"},status=status.HTTP_404_NOT_FOUND)
        return super().list(request)
    
    def create(self, request, **kwargs):
        """  
            overriding the inherites .create() method 
            *
            * 2 possible listings
            *      1. profiles/company-profile/<int:company_id>/property-profiles/
            *          - creates the profile and associated it to user with user_id
            *      2. properties/property-profile/
            *          - create property normally
            *
        """
        company_id = self.kwargs.get('company_id', None)
        if not company_id:
            return super().create(request, **kwargs)
        try:
                company = CompanyProfile.objects.filter(user_id=company_id).first()
                request.data['company'] = company
                return super().create(request, **kwargs)
        except CompanyProfile.DoesNotExist:
                return Response({"details":"Company Profile does not exist"},status=status.HTTP_404_NOT_FOUND)
        
        
    
class CondoUnitViewSet(ModelViewSet):
    """
        View Set for Condo Unit model  
    """
    queryset = CondoUnit.objects.all()
    serializer_class = CondoUnitSerializer
    
    # added list functionnality to list units belonging to property specified in endpoint url
    def list(self, request, **kwargs):
        property_id = self.kwargs.get('property_id', None)
        if not property_id:
            return super().list(request, **kwargs)
        try:
            condos = CondoUnit.objects.filter(property_id=property_id)
            serializer = CondoUnitSerializer(condos, many=True)
            return Response(serializer.data)
        except CompanyProfile.DoesNotExist:
            return Response({"details":"Company Profile does not exist"},status=status.HTTP_404_NOT_FOUND)
        
    # added functionnality to directly connect unit to the property
    def create(self, request, **kwargs):
        property_id = self.kwargs.get('property_id', None)
        if not property_id:
            return super().create(request, **kwargs)
        request.data['property'] = property_id
        return super().create(request, **kwargs)
    
        
class ParkingUnitViewSet(ModelViewSet):
    """
        View Set for Parking Unit model 
    """
    queryset = ParkingUnit.objects.all()
    serializer_class = ParkingUnitSerializer
    
    # added list functionnality to list units belonging to property specified in endpoint url
    def list(self, request, **kwargs):
        property_id = self.kwargs.get('property_id', None)
        if not property_id:
            return super().list(request, **kwargs)
        try:
            condos = CondoUnit.objects.filter(property_id=property_id)
            serializer = CondoUnitSerializer(condos, many=True)
            return Response(serializer.data)
        except CompanyProfile.DoesNotExist:
            return Response({"details":"Company Profile does not exist"},status=status.HTTP_404_NOT_FOUND)
    
    # added functionnality to directly connect unit to the property
    def create(self, request, **kwargs):
        property_id = self.kwargs.get('property_id', None)
        if not property_id:
            return super().create(request, **kwargs)
        request.data['property'] = property_id
        return super().create(request, **kwargs)

class StorageUnitViewSet(ModelViewSet):
    """
        View Set for Storage Unit model 
    """
    queryset = StorageUnit.objects.all()
    serializer_class = StorageUnitSerializer
    
    # added functionnality to directly connect unit to the property
    def create(self, request, **kwargs):
        property_id = self.kwargs.get('property_id', None)
        if not property_id:
            return super().create(request, **kwargs)
        request.data['property'] = property_id
        return super().create(request, **kwargs)
    
    # added list functionnality to list units belonging to property specified in endpoint url
    def list(self, request, **kwargs):
        property_id = self.kwargs.get('property_id', None)
        if not property_id:
            return super().list(request, **kwargs)
        try:
            condos = CondoUnit.objects.filter(property_id=property_id)
            serializer = CondoUnitSerializer(condos, many=True)
            return Response(serializer.data)
        except CompanyProfile.DoesNotExist:
            return Response({"details":"Company Profile does not exist"},status=status.HTTP_404_NOT_FOUND)