from App_Board.models import Category, Board, EditLog, Photo, Files 
from App_API.serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=True, methods=['get'])
    def boards(self, request, *args, **kwargs):
        category = self.get_object()
        posts = Board.objects.filter(category = category)
        serializer = BoardSerializer(posts, many = True)
        return Response(serializer.data)

class EditlogViewSet(viewsets.ModelViewSet):
    queryset = EditLog.objects.all()
    serializer_class = EditLogSerializer

class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
    # 게시글 조회시 조회수 증가
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.post_views_counting += 1 
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    # 게시글 업데이트 시 editlog 추가
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        editlog = EditLog()
        editlog.edit_date = timezone.now()
        editlog.editor = request.user
        editlog.post = instance
        editlog.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def editlogs(self, request, pk = None):
        board = self.get_object()
        editlogs = EditLog.objects.filter(post = board)
        serialiezer = EditLogSerializer(editlogs, many = True)
        return Response(serialiezer.data)

    @action(detail=True, methods=['get'])
    def photos(self, request, pk = None):
        board = self.get_object()
        photos = Photo.objects.filter(post = board)
        serializer = PhotoSerializer(photos, many = True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def files(self, request, pk = None):
        board = self.get_object()
        files = Files.objects.filter(post = board)
        serializer = FilesSerializer(files, many = True)
        return Response(serializer.data)
    
