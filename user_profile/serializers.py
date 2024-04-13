from rest_framework import serializers

from properties.serializers import CondoUnitSerializer
from .models import User, PublicProfile, EmployeeProfile, CompanyProfile, Profile

"""  
    Serializers for the profile and user models 
"""

class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer  
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class ProfileSerializer(serializers.ModelSerializer):
    """
        Profile Serializer for abstract profile class  
    """
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'address', 'city', 'province', 'postal_code', 'phone_number', 'avatar']
        

class PublicProfileSerializer(serializers.ModelSerializer):
    """
        Public Profile Serializer with inherited fields  
    """
    user = UserSerializer()
    condo_units = CondoUnitSerializer(many=True, read_only=True)
    class Meta(ProfileSerializer.Meta):
        model = PublicProfile
        fields = ProfileSerializer.Meta.fields + ['type', 'condo_units']


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """
        Employee Profile Serializer with inherited fields  
    """
    user = UserSerializer()
    class Meta(ProfileSerializer.Meta):
        model = EmployeeProfile
        fields = ProfileSerializer.Meta.fields + ['position']
        read_only_fields = ['position']

class CompanyProfileSerializer(serializers.ModelSerializer):
    """
        Company Profile Serializer with inherited fields  
    """
    user = UserSerializer()
    class Meta(ProfileSerializer.Meta):
        model = CompanyProfile
        fields = ProfileSerializer.Meta.fields