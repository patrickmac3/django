from django.db import models

from finance.models import FinanceModel


class PropertyProfile(models.Model):
    """
    Represents a property profile.

    Attributes:
        company (ForeignKey): The company profile associated with the property.
        address (CharField): The address of the property.
        city (CharField): The city where the property is located.
        province (CharField): The province where the property is located.
        postal_code (CharField): The postal code of the property.
        fee_rate (DecimalField): The fee rate of the property.
    """
    name = models.CharField(max_length=100, null=True)
    company = models.ForeignKey('user_profile.CompanyProfile', on_delete=models.CASCADE, related_name='property_profiles')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=12)
    fee_rate = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    image = models.ImageField(upload_to="property_images", default="property_images/defaultProperty.jpg")
    
    
    def __str__(self):
        """
        Returns a string representation of the property profile.

        Returns:
            str: The string representation of the property profile.
        """
        return str(self.company)

    def get_condo_units(self):
        """
        Returns the condo units associated with the property.

        Returns:
            QuerySet: The queryset of condo units associated with the property.
        """
        return CondoUnit.objects.filter(property=self)

    def get_parking_units(self):
        """
        Returns the parking units associated with the property.

        Returns:
            QuerySet: The queryset of parking units associated with the property.
        """
        return ParkingUnit.objects.filter(property=self)

    def get_storage_units(self):
        """
        Returns the storage units associated with the property.

        Returns:
            QuerySet: The queryset of storage units associated with the property.
        """
        return StorageUnit.objects.filter(property=self)

    @property
    def num_condo_units(self):
        """
        Returns the number of condo units associated with the property.

        Returns:
            int: The number of condo units associated with the property.
        """
        return self.condo_units.count()

    @property
    def num_parking_units(self):
        """
        Returns the number of parking units associated with the property.

        Returns:
            int: The number of parking units associated with the property.
        """
        return self.parking_units.count()

    @property
    def num_storage_units(self):
        """
        Returns the number of storage units associated with the property.

        Returns:
            int: The number of storage units associated with the property.
        """
        return self.storage_units.count()


class Unit(models.Model):
    """
    Represents a unit.

    Attributes:
        location (CharField): The location of the unit.
        size (DecimalField): The size of the unit.
        purchase_price (DecimalField): The purchase price of the unit.
        rent_price (DecimalField): The rent price of the unit.
        extra_information (TextField): Additional information about the unit.
    """

    class Meta:
        abstract = True

    location = models.CharField(max_length=4)
    size = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=20)
    rent_price = models.DecimalField(decimal_places=2, max_digits=20)
    extra_information = models.TextField(null=True)
    operational_expense = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    
    @property
    def property_fee(self):
        """
        Calculates and returns the property fee for the unit.

        Returns:
            Decimal: The property fee for the unit.
        """
        return FinanceModel.calculate_fee(self)


class CondoUnit(Unit):
    """
    Represents a condo unit.

    Attributes:
        property (ForeignKey): The property profile associated with the condo unit.
        public_profile (ForeignKey): The public profile associated with the condo unit.
    """

    property = models.ForeignKey('PropertyProfile', on_delete=models.CASCADE, related_name='condo_units')
    public_profile = models.ForeignKey('user_profile.PublicProfile', on_delete=models.SET_NULL, related_name='condo_units', null=True)
    image = models.ImageField(upload_to='condoUnit_images', default="condoUnit_images/defaultCondoUnit.jpg")

    def __str__(self):
        """
        Returns a string representation of the condo unit.

        Returns:
            str: The string representation of the condo unit.
        """
        return str(self.property)


class ParkingUnit(Unit):
    """
    Represents a parking unit.

    Attributes:
        property (ForeignKey): The property profile associated with the parking unit.
        public_profile (ForeignKey): The public profile associated with the parking unit.
    """

    property = models.ForeignKey('PropertyProfile', on_delete=models.CASCADE, related_name='parking_units')
    public_profile = models.ForeignKey('user_profile.PublicProfile', on_delete=models.SET_NULL, related_name='parking_units', null=True)
    image = models.ImageField(upload_to='parkingUnit_images', default="parkingUnit_images/defaultParkingUnit.jpg")

    def __str__(self):
        """
        Returns a string representation of the parking unit.

        Returns:
            str: The string representation of the parking unit.
        """
        return str(self.property)


class StorageUnit(Unit):
    """
    Represents a storage unit.

    Attributes:
        property (ForeignKey): The property profile associated with the storage unit.
        public_profile (ForeignKey): The public profile associated with the storage unit.
    """

    property = models.ForeignKey('PropertyProfile', on_delete=models.CASCADE, related_name='storage_units')
    public_profile = models.ForeignKey('user_profile.PublicProfile', on_delete=models.SET_NULL, related_name='storage_units', null=True)
    image = models.ImageField(upload_to='storageUnit_images', default="storageUnit_images/defaultStorageUnit.jpg")

    def __str__(self):
        """
        Returns a string representation of the storage unit.

        Returns:
            str: The string representation of the storage unit.
        """
        return str(self.property)






