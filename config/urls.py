from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App_Board.urls')),
    path('auth/', include('App_Auth.urls')),
    path('file/',include('App_Files.urls')),
    path('user/', include('App_Userpage.urls')),
    path('api/', include('App_API.urls'))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

