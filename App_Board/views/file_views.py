from ..models import *
from ..forms import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse



def file_download(request, board_id):
    print('실행 1')
    board = get_object_or_404(Board, id=board_id)
    path = str(board.file)
    file_name = path.split('/')[-1]
    print(file_name)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
 
    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="multipart/formed-data")
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        return response
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")
