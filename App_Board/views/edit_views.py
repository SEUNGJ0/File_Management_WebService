from ..models import *
from ..forms import *
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


# 함수형 뷰에서 사용하는 권한 제한
from django.contrib.auth.decorators import login_required
# 클레스형 뷰애서 사용하는 권한 제한
from django.contrib.auth.mixins import LoginRequiredMixin

all_category = Category.objects.all()

@login_required(login_url='App_Auth:login')
def post_create_view(request, category_id):
    select_category = get_object_or_404(Category, id = category_id)
    context = {
        'all_category' : all_category, 
        'select_category' : select_category
    }
    # 공지사항 작성 권한 분리
    if str(select_category) == "공지사항" and not request.user.is_admin :
        messages.error(request, '작성권한이 없습니다')
        return redirect("App_Board:board_render_view",select_category.slug)

    if request.method == 'POST' and request.POST['action'] == 'save':
        form = BoardForm(request.POST) # -> boundForm
        if form.is_valid():
            # 게시판 폼에 추가
            post = form.save(commit=False)
            post.created_date = timezone.now()
            post.category = get_object_or_404(Category, id=category_id)
            post.post_author = request.user
            post.save()   
            # 첨부 이미지 및 파일 저장을 위한 함수 호출
            return handle_save_action(request, post = post)     
           
        context['form'] = form
        return render(request, 'Board_create.html',context)
    else:
        context['form'] = BoardForm() # -> unboundForm

    return render(request, 'Board_create.html', context)

@login_required(login_url='App_Auth:login')
def post_update_view(request, board_id):
    select_post = get_object_or_404(Board, id=board_id)

    if request.user.company == select_post.post_author.company or request.user.is_admin :
        if request.method == "POST":
            form = BoardForm(request.POST, instance=select_post)# -> boundForm
            form_edit = EditLogForm()
            if form.is_valid():
                action = request.POST['action']
                # 게시판 폼에 추가
                select_post = form.save(commit=False)
                select_post.updated_date = timezone.now()  # 수정일시 저장
                select_post.save()

                if action == 'save':
                    return handle_save_action(request, post = select_post, form_edit = form_edit)
                                        
                elif action.startswith("delete"):
                    del_id = action[7:]
                    handle_delete_action(del_id)
                    
        else:
            form = BoardForm(instance=select_post)

        context = {
            'form': form, 
            'all_category' : all_category, 
            'select_post' : select_post
        }
        return render(request, 'Board_create.html', context)
    else:
        messages.error(request, '수정권한이 없습니다')
        return redirect("App_Board:post_render_view", board_id = board_id)
    
def handle_save_action(request, post, form_edit = None):
    for image in request.FILES.getlist('image'):
        photo = Photo()
        photo.post = post
        photo.image = image
        photo.save()

    for file in request.FILES.getlist('file'):
        files = Files()
        files.post = post
        files.user = request.user
        files.file = file
        files.save()
    
    if form_edit:
        editlog = form_edit.save(commit=False)
        editlog.edit_date = timezone.now()
        editlog.editor = request.user
        editlog.post = post
        editlog.save()

    return redirect('App_Board:post_render_view', post.id)

def handle_delete_action(del_id):
    if del_id[0] == 'i':
        image = Photo.objects.get(pk=del_id[1:])
        # file_delete(image_id=image.id) # 디렉토리에서 파일 삭제 함수
        image.delete()
    else:
        file = Files.objects.get(pk=del_id[1:])
        # file_delete(file_id=file.id)
        file.delete()

class post_delete(LoginRequiredMixin, generic.DeleteView):
    model = Board
    success_url = '/'
    template_name = 'Board_delete.html'
   
    def get_context_data(self, **kwargs):
        context = super(post_delete, self).get_context_data(**kwargs)
        context['all_category'] = all_category
        return context

