from rest_framework import generics
from App_API.serializers import BoardSerializer
from App_Board.models import Board

class BoardList_GCBV(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDetail_GCBV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer