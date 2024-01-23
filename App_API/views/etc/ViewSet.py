# 데이터 처리
from App_API.serializers import BoardSerializer, CategorySerializer
from App_Board.models import Board, Category

# REST_Framework
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer
   permission_classes = [permissions.IsAuthenticated]

class BoardViewSet(viewsets.ModelViewSet):
   queryset = Board.objects.all()
   serializer_class = BoardSerializer
   
   def perform_create(self, serializer):
      serializer.save(user = self.request.user)

@api_view(['GET'])
def HelloAPI(request):
   return Response("hello world!")
