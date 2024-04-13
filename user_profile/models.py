
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from registration_key.models import RegistrationKey
from properties.models import PropertyProfile
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for creating and managing user accounts.
    """

    def create_superuser(self, email, password,  **other_fields):
        """
        Create a superuser with the given email, password, and other fields.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, password,  **other_fields)
    
    def create_user(self, email, password, **other_fields):
        """
        Create a user with the given email, password, and other fields.
        """
        
        if not email:
            raise ValueError('You must provide an email address')
        email = self.normalize_email(email)
        other_fields['role'] = User.Role.ADMIN
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication.
    """

    class Role(models.TextChoices):
        PUBLIC = 'PUBLIC', 'Public'
        EMPLOYEE = 'EMPLOYEE','Employee'
        COMPANY = 'COMPANY', 'Company'
        ADMIN = 'ADMIN', 'Admin'
        
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.PUBLIC)    
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'first_name', 'last_name']
    
    def __str__(self):
        """
        Return a string representation of the user.
        """
        return self.first_name + " " + self.last_name
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create associated profile based on user role.
    """
    if created and instance.is_superuser:
        return
    elif created and instance.role == 'PUBLIC':
        PublicProfile.objects.create(user=instance)
    elif created and instance.role == 'EMPLOYEE':
        EmployeeProfile.objects.create(user=instance)
    elif created and instance.role == 'COMPANY':
        CompanyProfile.objects.create(user=instance)
    
class Profile(models.Model):
    """
    Abstract profile model that is inherited by Public, Employee, and Company profiles.
    """

    class Meta:
        abstract = True
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)    
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to="avatar_images", default="avatar_images/pp.jpg")
    
    def __str__(self):
        """
        Return a string representation of the profile.
        """
        return str(self.user)
    
class PublicProfile(Profile):
    """
    Profile model for public users.
    """

    class Type(models.TextChoices):
        OWNER = 'OWNER', 'Owner'
        RENTER = 'RENTER', 'Renter'
    
    type = models.CharField(max_length=100, choices=Type.choices, default=Type.OWNER)
    registration_key = models.CharField(max_length=50, null=True)

class EmployeeProfile(Profile):
    """
    Profile model for employee users.
    """

    class Position(models.TextChoices):
        MANAGER = 'MANAGER', 'Manager'
        FINANCE = 'FINANCE', 'Finance'
        DAILY_OPERATIONS = 'DAILY_OPERATIONS', 'Daily_Operations'
    
    position = models.CharField(max_length=100, choices=Position.choices, default=Position.DAILY_OPERATIONS)
    
class CompanyProfileManager(models.Manager):
    """
    Manager for the CompanyProfile model.
    """

    def property_profiles(self):
        """
        Return the property profiles associated with the company.
        """
        return PropertyProfile.objects.filter(company=self)
    
class CompanyProfile(Profile):
    """
    Profile model for company users.
    """

    objects = CompanyProfileManager()
    
    def property_profiles(self):
        """
        Return the property profiles associated with the company.
        """
        return PropertyProfile.objects.filter(company=self)
    
    def send_registration_key(self, key, user):
        """
        Send a registration key to the user's email.
        """
        email = user.email
        send_mail(
            "unit registration_key",
            str(key),
            # TODO: change destination email address
            "patrickmaceachen78@gmail.com",
            ["patrickmaceachen78@gmail.com"],
            fail_silently=False
        )
