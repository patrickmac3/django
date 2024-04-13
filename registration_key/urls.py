from rest_framework.routers import DefaultRouter

from .views import CondoRegistrationKeyView, ParkingRegistrationKeyView, StorageRegistrationKeyView

router = DefaultRouter()

router.register(r'condo-registration-key', CondoRegistrationKeyView, basename="condo-registration-key" )
router.register(r'parking-registration-key', ParkingRegistrationKeyView, basename="parking-registration-key" )
router.register(r'storage-registration-key', StorageRegistrationKeyView, basename="storage-registration-key" )

urlpatterns = router.urls

"""
This module defines the URL patterns for the registration key endpoints.

The following URL patterns are defined:
- condo-registration-key/ : Maps to the CondoRegistrationKeyView class.
- parking-registration-key/ : Maps to the ParkingRegistrationKeyView class.
- storage-registration-key/ : Maps to the StorageRegistrationKeyView class.

These URL patterns are registered with the DefaultRouter and included in the urlpatterns list.
"""
