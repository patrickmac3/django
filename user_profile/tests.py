from django.test import TestCase, client
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from .serializers import UserSerializer
from .models import User, PublicProfile, EmployeeProfile, CompanyProfile

UserModel = get_user_model()


class TestProfileModels(TestCase):
    """ Test User Profile Models """
    
    @classmethod
    def setUpTestData(cls):
        # Set up test data to be used 
        cls.user = User.objects.create_superuser(         
            email='test@example.com',
            password='password',
            role='PUBLIC',
            first_name='Test',
            last_name='User'
        )
        cls.public = User.objects.create_user(
            email='public@example.com',
            password='password',
            role='PUBLIC',
            first_name='Test',
            last_name='User'
        )
        cls.employee = User.objects.create_user(
            email='employee@example.com',
            password='password',
            role='EMPLOYEE',
            first_name='Test',
            last_name='User'
        )
        cls.company = User.objects.create_user(
            email='company@example.com',
            password='password',
            role='COMPANY',
            first_name='Test',
            last_name='User'
        )

    """ Test superuser and is_staff """
    def test_create_superuser_is_superuser(self):
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_create_superuser_invalid(self):
        with self.assertRaises(ValueError) as err:
            User.objects.create_superuser(
                email='testuser1@gmail.com',
                first_name="test",
                last_name="user",
                password="password",
                role="PUBLIC",
                is_superuser=True,
                is_staff=False,
            )
        self.assertEqual(str(err.exception), 'Superuser must be assigned to is_staff=True.')
        with self.assertRaises(ValueError) as err:
            User.objects.create_superuser(
                email='testuser2@gmail.com',
                first_name="test",
                last_name="user",
                password="password",
                role="PUBLIC",
                is_superuser=False,
                is_staff=True,
            )
        self.assertEqual(str(err.exception), 'Superuser must be assigned to is_superuser=True.')

    def test_create_user_is_not_superuser(self):
        self.assertFalse(self.public.is_superuser)
        self.assertFalse(self.public.is_staff)
        self.assertTrue(self.public.is_active)
   
    def test_created_user_role_choices(self):
        self.assertEqual(self.user.role, 'PUBLIC')
        self.assertEqual(self.employee.role, 'EMPLOYEE')
        self.assertEqual(self.company.role, 'COMPANY')

    def test_public_profile_created(self):
        public_profile = PublicProfile.objects.get(user=self.public)
        self.assertIsInstance(public_profile, PublicProfile)

     
    def test_employee_profile_created(self):
        employee_profile = EmployeeProfile.objects.get(user=self.employee)
        self.assertIsInstance(employee_profile, EmployeeProfile)

     
    def test_company_profile_created(self):
        company_profile = CompanyProfile.objects.get(user=self.company)
        self.assertIsInstance(company_profile, CompanyProfile)
        


class TestUserSignUp(TestCase):
    """ Testing Sign up endpoints for public profile/user """
    @classmethod
    def setUpTestData(cls):
        # create test data user
        cls.user = User.objects.create_user(
            email='public@example.com',
            password='password',
            role='PUBLIC',
            first_name='Test',
            last_name='User'
        )
        
    # sign up for public profile
    def test_user_creation(self):
        respnse = self.client.post('/profiles/user/',{
            "email": "test4@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "PUBLIC",
            "password": "password"
        })
        test_user = User.objects.get(email="test4@example.com")
        self.assertEqual(respnse.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test4@example.com").exists())
        self.assertTrue(PublicProfile.objects.filter(user=test_user).exists())
    
    # sign up with email that is already in use
    def test_user_creation_existing_email(self):
        response = self.client.post('/profiles/user/',{
            "email": "public@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "PUBLIC",
            "password": "password"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'],["user with this email address already exists."])
    
    # sign up with invalid email 
    def test_user_creation_invalid_email(self):
        response = self.client.post('/profiles/user/',{
            "email": "public",
            "first_name": "John",
            "last_name": "Doe",
            "role": "PUBLIC",
            "password": "password"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'],["Enter a valid email address."])
    
    # sign up without password 
    def test_user_creation_without_password(self):
        response = self.client.post('/profiles/user/',{
            "email": "publhhic@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "PUBLIC",
            "password": ""
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"],["This field may not be blank."])