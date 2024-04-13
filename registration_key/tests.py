
from django.test import TestCase
from django.urls import reverse

from properties.models import CondoUnit, ParkingUnit, PropertyProfile, StorageUnit
from registration_key.models import CondoRegistrationKey, ParkingRegistrationKey, StorageRegistrationKey
from user_profile.models import CompanyProfile, PublicProfile, User
from rest_framework import status

class CreateCondoRegistrationKeyTestCase(TestCase):
    """
    Test case for creating condo registration keys.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        """
        cls.public_user = User.objects.create_user(
            email='public@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            role='PUBLIC'
        )
        cls.company_user = User.objects.create_user(
            email='company@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            role='COMPANY'
        )
        cls.company = CompanyProfile.objects.get(user=cls.company_user)
        cls.public = PublicProfile.objects.get(user=cls.public_user)
        
        cls.property = PropertyProfile.objects.create(
            company=cls.company,
            address='123 Test St',
            city='Montreal',
            province='QC',
            postal_code='T1T 1T1'
        )
        cls.condo = CondoUnit.objects.create(
            property=cls.property, 
            location='Montreal',
            purchase_price=100,
            rent_price=50
        )
        cls.url = reverse('condo-registration-key-list')
        
    def test_create_registration_key(self):
        """
        Test creating a registration key for a condo unit with the user as the owner.
        """
        data = {
            'unit': self.condo.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.public_user.id)
        self.assertEqual(response.data['unit'], self.condo.id)
        self.assertTrue(response.data['is_owner'])
        self.assertTrue('key' in response.data)
        registration_key = CondoRegistrationKey.objects.get(user=self.public, unit=self.condo)
        self.assertEqual(registration_key.key, response.data['key'])
    
    def test_create_registration_key_with_is_owner(self):
        """
        Test creating a registration key for a condo unit with the user as a non-owner.
        """
        data = {
            'unit': self.condo.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': False
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.public_user.id)
        self.assertEqual(response.data['unit'], self.condo.id)
        self.assertFalse(response.data['is_owner'])
        self.assertTrue('key' in response.data)
        registration_key = CondoRegistrationKey.objects.get(user=self.public, unit=self.condo)
        self.assertEqual(registration_key.key, response.data['key'])

    def test_create_registration_key_with_invalid_user(self):
        """
        Test creating a registration key with an invalid user email.
        """
        data = {
            'unit': self.condo.id,
            'company': self.company.user_id,
            'user': 'invalid@example.com',
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no user with the given email')
        
    def test_create_registration_key_with_non_public_user(self):
        """
        Test creating a registration key with a non-public user.
        """
        data = {
            'unit': self.condo.id,
            'company': self.company.user_id,
            'user': self.company.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], "The user associated with this email is not a public user")
        
    def test_create_registration_key_with_invalid_unit(self):
        """
        Test creating a registration key with an invalid condo unit ID.
        """
        data = {
            'unit': 999,  # Invalid unit ID
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no condo unit associated with the given id')
    
    def test_create_registration_key_with_invalid_company(self):
        """
        Test creating a registration key with an invalid company ID.
        """
        data = {
            'unit': self.condo.id,
            'company': 999,  # Invalid company ID
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no Company Profile associated with the given id')
        
    def test_create_registration_key_with_existing_unit(self):
        """
        Test creating a registration key for a condo unit that is already in use.
        """
        self.condo.public_profile = self.public
        self.condo.save()
        data = {
            'unit': self.condo.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['details'], 'this unit is already in use.')
        
class CreateStorageRegistrationKeyTestCase(TestCase):
    """
    Test case for creating a storage registration key.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        """
        cls.public_user = User.objects.create_user(
            email='public@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            role='PUBLIC'
        )
        cls.company_user = User.objects.create_user(
            email='company@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            role='COMPANY'
        )
        cls.company = CompanyProfile.objects.get(user=cls.company_user)
        cls.public = PublicProfile.objects.get(user=cls.public_user)
        
        cls.property = PropertyProfile.objects.create(
            company=cls.company,
            address='123 Test St',
            city='Montreal',
            province='QC',
            postal_code='T1T 1T1'
        )
        cls.storage = StorageUnit.objects.create(
            property=cls.property, 
            location='Montreal',
            purchase_price=100,
            rent_price=50
        )
        cls.url = reverse('storage-registration-key-list')
        
    def test_create_registration_key(self):
        """
        Test creating a registration key for a storage unit.
        """
        data = {
            'unit': self.storage.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.public_user.id)
        self.assertEqual(response.data['unit'], self.storage.id)
        self.assertTrue(response.data['is_owner'])
        self.assertTrue('key' in response.data)
        registration_key = StorageRegistrationKey.objects.get(user=self.public, unit=self.storage)
        self.assertEqual(registration_key.key, response.data['key'])
    
    def test_create_registration_key_with_is_owner(self):
        """
        Test creating a registration key for a storage unit with is_owner set to False.
        """
        data = {
            'unit': self.storage.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': False
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.public_user.id)
        self.assertEqual(response.data['unit'], self.storage.id)
        self.assertFalse(response.data['is_owner'])
        self.assertTrue('key' in response.data)
        registration_key = StorageRegistrationKey.objects.get(user=self.public, unit=self.storage)
        self.assertEqual(registration_key.key, response.data['key'])

    def test_create_registration_key_with_invalid_user(self):
        """
        Test creating a registration key with an invalid user email.
        """
        data = {
            'unit': self.storage.id,
            'company': self.company.user_id,
            'user': 'invalid@example.com',
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no user with the given email')
        
    def test_create_registration_key_with_non_public_user(self):
        """
        Test creating a registration key with a non-public user.
        """
        data = {
            'unit': self.storage.id,
            'company': self.company.user_id,
            'user': self.company.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], "The user associated with this email is not a public user")
        
        
    def test_create_registration_key_with_invalid_unit(self):
        """
        Test creating a registration key with an invalid storage unit ID.
        """
        data = {
            'unit': 999,  # Invalid unit ID
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no storage unit associated with the given id')
    
    def test_create_registration_key_with_invalid_company(self):
        """
        Test creating a registration key with an invalid company ID.
        """
        data = {
            'unit': self.storage.id,
            'company': 999,  # Invalid company ID
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no Company Profile associated with the given id')
        
    def test_create_registration_key_with_existing_unit(self):
        """
        Test creating a registration key for a storage unit that is already in use.
        """
        self.storage.public_profile = self.public
        self.storage.save()
        data = {
            'unit': self.storage.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['details'], 'this unit is already in use.')
        


class CreateParkingRegistrationKeyTestCase(TestCase):
    """
    Test case for creating a parking registration key.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        """
        cls.public_user = User.objects.create_user(
            email='public@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            role='PUBLIC'
        )
        cls.company_user = User.objects.create_user(
            email='company@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            role='COMPANY'
        )
        cls.company = CompanyProfile.objects.get(user=cls.company_user)
        cls.public = PublicProfile.objects.get(user=cls.public_user)
        
        cls.property = PropertyProfile.objects.create(
            company=cls.company,
            address='123 Test St',
            city='Montreal',
            province='QC',
            postal_code='T1T 1T1'
        )
        cls.parking = ParkingUnit.objects.create(
            property=cls.property, 
            location='Montreal',
            purchase_price=100,
            rent_price=50
        )
        cls.url = reverse('parking-registration-key-list')
        
    def test_create_registration_key(self):
        """
        Test creating a registration key with valid data.
        """
        data = {
            'unit': self.parking.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.public_user.id)
        self.assertEqual(response.data['unit'], self.parking.id)
        self.assertTrue(response.data['is_owner'])
        self.assertTrue('key' in response.data)
        registration_key = ParkingRegistrationKey.objects.get(user=self.public, unit=self.parking)
        self.assertEqual(registration_key.key, response.data['key'])
    
    def test_create_registration_key_with_is_owner(self):
        """
        Test creating a registration key with is_owner set to False.
        """
        data = {
            'unit': self.parking.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': False
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.public.user.id)
        self.assertEqual(response.data['unit'], self.parking.id)
        self.assertFalse(response.data['is_owner'])
        self.assertTrue('key' in response.data)
        registration_key = ParkingRegistrationKey.objects.get(user=self.public, unit=self.parking)
        self.assertEqual(registration_key.key, response.data['key'])

    def test_create_registration_key_with_invalid_user(self):
        """
        Test creating a registration key with an invalid user email.
        """
        data = {
            'unit': self.parking.id,
            'company': self.company.user_id,
            'user': 'invalid@example.com',
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no user with the given email')
        
    def test_create_registration_key_with_non_public_user(self):
        """
        Test creating a registration key with a non-public user email.
        """
        data = {
            'unit': self.parking.id,
            'company': self.company.user_id,
            'user': self.company.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], "The user associated with this email is not a public user")
        
        
    def test_create_registration_key_with_invalid_unit(self):
        """
        Test creating a registration key with an invalid parking unit ID.
        """
        data = {
            'unit': 999,  # Invalid unit ID
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no parking unit associated with the given id')
    
    def test_create_registration_key_with_invalid_company(self):
        """
        Test creating a registration key with an invalid company ID.
        """
        data = {
            'unit': self.parking.id,
            'company': 999,  # Invalid company ID
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['details'], 'There is no Company Profile associated with the given id')
        
    def test_create_registration_key_with_existing_unit(self):
        """
        Test creating a registration key for a parking unit that is already in use.
        """
        self.parking.public_profile = self.public
        self.parking.save()
        data = {
            'unit': self.parking.id,
            'company': self.company.user_id,
            'user': self.public.user.email,
            'is_owner': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['details'], 'this unit is already in use.')
        
        