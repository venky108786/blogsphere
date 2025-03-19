
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from blogsphere.views import api_home

urlpatterns = [
    path('', api_home, name='api-home'),
    #app urls
    path('admin/', admin.site.urls),
    path('api/blog/', include('blog.urls')),  # 👈 Changed from 'api/' to 'api/blog/'
    path('api/users/', include('users.urls')),  # 👈 Changed from 'api/' to 'api/users/'

    # ✅ JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
