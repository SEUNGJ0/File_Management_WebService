from App_Board.models import Board
from App_API.serializers import BoardSerializer

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

class BoardList_Mixin(ListModelMixin,
                      CreateModelMixin,
                      GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get(self, request, *args, **kawrgs):
        # 동작은 ListModeMixin에서 제공
        return self.list(request, *args, **kawrgs)
    
    def post(self, request, *args, **kawrgs):
        # 동작은 CreateModelMixin 제공
        return self.create(request, *args, **kawrgs)

class BoardDetail_Mixin(RetrieveModelMixin,
                        UpdateModelMixin,
                        DestroyModelMixin,
                        GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get(self, request, *args, **kwargs):
        # 동작은 RetrieveModelMixin에서 제공
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        # 동작은 UpdateModelMixin에서 제공
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        # 동작은 DestroyModelMixin에서 제공
        return self.destroy(request, *args, **kwargs)