from django.db import models
import hashlib
import random


class RegistrationKeyManager(models.Manager):
    """
    A custom manager for the RegistrationKey model.
    """

    def get_queryset(self):
        """
        Returns a queryset of RegistrationKey objects that are activated.
        """
        return super().get_queryset().filter(is_active=True)
    
    def create_key(self, user, unit):
        """
        Creates a new RegistrationKey object with the specified user and unit.
        
        Args:
            user (User): The user associated with the key.
            unit (Unit): The unit associated with the key.
        
        Returns:
            RegistrationKey: The newly created RegistrationKey object.
        """
        key = self.model(user=user, unit=unit)
        key.generate_key(user, unit)
        key.save(using=self._db)
        return key

class RegistrationKey(models.Model):
    """
    An abstract base class for registration keys.
    """

    class Meta:
        abstract = True
        
    key = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey('user_profile.PublicProfile', on_delete=models.CASCADE, null=False, blank=False)
    is_owner = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        """
        Returns a string representation of the registration key.
        """
        return self.key
    
    @staticmethod
    def generate_key(user, unit):
        """
        Generates a unique key based on the user's email and the unit's ID.
        
        Args:
            user (User): The user associated with the key.
            unit (Unit): The unit associated with the key.
        
        Returns:
            str: The generated key.
        """ 
        salt = hashlib.sha256(str(random.random()).encode()).hexdigest()[:5]
        email = user.email.encode('utf-8')
        unit_id = str(unit.id).encode('utf-8')
        key = hashlib.sha256(salt.encode() + email + unit_id).hexdigest()
        return key
    
    def deactivate(self):
        """
        Deactivates the registration key.
        """
        self.is_active = False

    
class CondoRegistrationKey(RegistrationKey):
    """
    A registration key for a condo unit.
    """

    unit = models.ForeignKey('properties.CondoUnit', on_delete=models.CASCADE, blank=False)
    # objects = RegistrationKeyManager()
   
    def __str__(self):
        """
        Returns a string representation of the condo registration key.
        """
        return self.key
    
class ParkingRegistrationKey(RegistrationKey):
    """
    A registration key for a parking unit.
    """

    unit = models.ForeignKey('properties.ParkingUnit', on_delete=models.CASCADE, blank=False)
    objects = RegistrationKeyManager()
    
    def __str__(self):
        """
        Returns a string representation of the parking registration key.
        """
        return self.key
    
       
class StorageRegistrationKey(RegistrationKey):
    """
    A registration key for a storage unit.
    """

    unit = models.ForeignKey('properties.StorageUnit', on_delete=models.CASCADE, blank=False)
    objects = RegistrationKeyManager()
    
    def __str__(self):
        """
        Returns a string representation of the storage registration key.
        """
        return self.key
