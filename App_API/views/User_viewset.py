from App_Auth.models import User
from App_Board.models import Board
from App_API.serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    print()
    @action(detail=True, methods=['get'])
    def boards(self, request, *args, **kwargs):
        user = self.get_object()
        posts = Board.objects.filter(post_author = user)
        serializer = BoardSerializer(posts, many = True)
        return Response(serializer.data)
