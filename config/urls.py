from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App_Board.urls')),
    path('auth/', include('App_Auth.urls')),
    path('file/',include('App_Files.urls')),
    path('user/', include('App_Userpage.urls')),
    path('api/', include('App_API.urls')),
    path("api/auth", views.obtain_auth_token, name="obtain_auth_token"),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')) # DRF 웹 로그인 
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

