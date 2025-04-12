
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from blog import views
from blogsphere.views import home_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/blog/', include('blog.urls')),
    path('api/users/', include('users.urls')),
    path('users/', include('users.urls')), # for browser URLs like /users/profile/madara/
    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
