from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from App_API.ViewSet import *

router = routers.DefaultRouter()
router.register('board', BoardViewSet)
router.register('category', CategoryViewSet)

urlpatterns = [
   path('', include(router.urls)),
#    # APIView
#    path('blog/apiv/', APIView.BlogList.as_view()),
#    path('blog/apiv/<int:pk>/', APIView.BlogDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
"""
format_suffix_patterns : URL 패턴 리스트를 받아 URL 패턴에 형식 접미사를 지원하는 패턴으로 변환
/example/1.json -> JSON 형식으로 응답
/example/1.xml ->  XML 형식으로 응답
"""