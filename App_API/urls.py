from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from App_API.views.Board_viewset import *
from App_API.views.User_viewset import UserViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'boards', BoardViewSet)
router.register(r'files', FilesViewSet)
router.register(r'photos', PhotosViewSet)
router.register(r'editlogs', EditlogViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
   path('', include(router.urls))
]

# urlpatterns = format_suffix_patterns(urlpatterns)
"""
format_suffix_patterns : URL 패턴 리스트를 받아 URL 패턴에 형식 접미사를 지원하는 패턴으로 변환
/example/1.json -> JSON 형식으로 응답
/example/1.xml ->  XML 형식으로 응답
"""