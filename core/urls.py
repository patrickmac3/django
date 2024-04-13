
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from jwt_auth_token.views import BlackListTokenView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # JWT token 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/blacklist/', BlackListTokenView.as_view(), name='blacklist'),
    # apps 
    path('profiles/', include('user_profile.urls')),
    path('properties/', include('properties.urls')),
    path('registration-keys/', include('registration_key.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
