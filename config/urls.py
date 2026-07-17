from django.contrib import admin
from django.urls import path, include

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from rest_framework_simplejwt.views import TokenRefreshView
from accounts.jwt_views import CustomTokenObtainPairView


from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('admin/', admin.site.urls),

    
    path('api/accounts/', include('accounts.urls')),

    
    path('api/token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),

   
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/music/', include('music.urls')),


    path('api/playlists/', include('playlists.urls')),


    path('api/subscription/',include('subscriptions.urls')),


    path('api/admin/', include('api.urls')),


    path('api/artists/', include('artists.urls')),


    path('api/notifications/',include('notifications.urls')),


    path('api/queue/',include('queue_system.urls')),

    path('api/auth/',include('accounts.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),

    path('api/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc'),


    path('api/accounts/password-reset/', include('django.contrib.auth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    
print("🔥 URLCONF LOADED")