from django.test import TestCase
from user_profile.models import CompanyProfile, User
from .models import PropertyProfile, CondoUnit, ParkingUnit, StorageUnit

class PropertyProfileTest(TestCase):

    @classmethod
    def setUp(cls):
        # Create a test objects
        cls.testuser = User.objects.create_superuser(password='testpass', email='test@email.com')
        cls.company = CompanyProfile.objects.create(user=cls.testuser)
        cls.property = PropertyProfile.objects.create(company=cls.company, address='123 Test St', city='Montreal', province='QC', postal_code='T1T 1T1')
        cls.condo_unit = CondoUnit.objects.create(property=cls.property, location='Montreal', purchase_price=100, rent_price=50)
        cls.parking_unit = ParkingUnit.objects.create(property=cls.property, location='Montreal', purchase_price=100, rent_price=50)
        cls.storage_unit = StorageUnit.objects.create(property=cls.property, location='Montreal', purchase_price=100, rent_price=50)

    def test_property_get_units_methods(self):
        # Test the get condo/parking/storage_units methods in a property
        self.assertEqual(self.property.get_condo_units().count(), 1)
        self.assertEqual(self.property.get_parking_units().count(), 1)
        self.assertEqual(self.property.get_storage_units().count(), 1)
    
    def test_property_num_units_properties(self):
        # Test the number of condo_units, parking_units and storage_units in a property
        self.assertEqual(self.property.num_condo_units, 1)
        self.assertEqual(self.property.num_parking_units, 1)
        self.assertEqual(self.property.num_storage_units, 1)

    def test_condo_unit_created(self):
        self.assertIsInstance(self.condo_unit, CondoUnit)

    def test_parking_unit_created(self):
        self.assertIsInstance(self.parking_unit, ParkingUnit)

    def test_storage_unit_created(self):
        self.assertIsInstance(self.storage_unit, StorageUnit)