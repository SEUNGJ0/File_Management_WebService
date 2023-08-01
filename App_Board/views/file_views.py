from ..models import *
from ..forms import *
import mimetypes # 한글 파일을 위한 패키진
import urllib
import os
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse


def file_download(request, file_id = None):
    if file_id :
        file = get_object_or_404(Files, id=file_id)
        path = file.get_filepath()
        file_name = file.get_filename()
    elif file_id == 0:
        file_name = "다중 압축 파일.zip"
        path = "file/관리/압축 파일/Multizip.zip"
    file_name = urllib.parse.quote(file_name.encode('utf-8'))
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type=mimetypes.guess_type(file_name))
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % file_name
        return response
    


