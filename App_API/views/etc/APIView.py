from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from App_Board.models import Board, EditLog, Files, Photo
from App_API.serializers import *

class BoardList_APIView(APIView):
    def get(self, request):
        all_board = Board.objects.all()
        # 여러 개의 객체를 serialization 하기 위해 "many = True"로 설정
        serializer = BoardSerializer(all_board, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class BoardDetail_APIView(APIView):
    def get(self, request, pk, format = None):
        board = get_object_or_404(Board, id = pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk):
        board = get_object_or_404(Board, id = pk)
        serializer = BoardSerializer(board, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        board = get_object_or_404(Board, id = pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)