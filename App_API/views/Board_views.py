from App_Board.models import Board, Category, EditLog, Photo, Files
from App_API.serializers import *

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

class CategoryList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get(self, request, *args, **kawrgs):
        return self.list(request, *args, **kawrgs)
    
    def post(self, request, *args, **kawrgs):
        return self.create(request, *args, **kawrgs)

class CategoryDetail(RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin,GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class BoardList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    def get(self, request, *args, **kawrgs):
        return self.list(request, *args, **kawrgs)
    
    def post(self, request, *args, **kawrgs):
        return self.create(request, *args, **kawrgs)

class BoardDetail(RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin,GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class EditlogList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = EditLog.objects.all()
    serializer_class = EditLogSerializer
    def get(self, request, *args, **kawrgs):
        return self.list(request, *args, **kawrgs)
    
    def post(self, request, *args, **kawrgs):
        return self.create(request, *args, **kawrgs)
    
class EditlogDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = EditLog.objects.all()
    serializer_class = EditLogSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class PhotoList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    def get(self, request, *args, **kawrgs):
        return self.list(request, *args, **kawrgs)
    
    def post(self, request, *args, **kawrgs):
        return self.create(request, *args, **kawrgs)

class PhotoDetail(RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin,GenericAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class FilesList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    def get(self, request, *args, **kawrgs):
        return self.list(request, *args, **kawrgs)
    
    def post(self, request, *args, **kawrgs):
        return self.create(request, *args, **kawrgs)

class FilesDetail(RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin,GenericAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)