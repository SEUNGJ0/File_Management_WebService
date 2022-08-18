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

@login_required(login_url='App_Auth:login')
def post_create(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()
    if str(category) == "공지사항" and str(request.user) != "국승조":
        print('실행')
        messages.error(request, '작성권한이 없습니다')
        return redirect("App_Board:post_in_category",category.slug)

    if request.method == 'POST':
        if request.POST['action'] == 'save':
            form = BoardForm(request.POST, request.FILES)
            if form.is_valid():
                # 게시판 폼에 추가
                Board = form.save(commit=False)
                Board.created_date = timezone.now()
                Board.category = get_object_or_404(Category, id=category_id)
                Board.post_author = request.user
                Board.save()   
                return redirect("App_Board:post_detail", Board.id)
            context = {'form': form, 'categories' : categories, 'current_category' : category,}
            return render(request, 'Board_create.html',context)
    else:
        form = BoardForm() # -> unboundForm

    context = {'form': form, 'categories' : categories, 'current_category' : category,}
    return render(request, 'Board_create.html', context)

@login_required(login_url='App_Auth:login')
def post_update(request, board_id):
    categories = Category.objects.all()
    board = get_object_or_404(Board, id=board_id)

    if request.user.company == board.post_author.company or request.user.company == 'admin' :
        if request.method == "POST":
            form = BoardForm(request.POST, request.FILES, instance=board)
            if form.is_valid():
                print(request.POST)
                if request.POST['action'] == 'save':
                    # 게시판 폼에 추가
                    board = form.save(commit=False)
                    board.updated_date = timezone.now()  # 수정일시 저장
                    board.save()
                    form_edit = EditLogForm()
                    editlog = form_edit.save(commit=False)
                    editlog.edit_date = timezone.now()
                    editlog.editor = request.user
                    editlog.board_id = board_id
                    editlog.save()
                    return redirect("App_Board:post_detail", board.id)
                    
                elif request.POST['action'] == 'delete':
                    board = form.save(commit=False)
                    board.file = None  
                    board.save()
                    context = {'form': form, 'categories' : categories, 'board' : board}
                    return render(request, 'Board_create.html', context)
        else:
            form = BoardForm(instance=board)

        context = {'form': form, 'categories' : categories, 'board' : board}
        return render(request, 'Board_create.html', context)
    else:
        messages.error(request, '수정권한이 없습니다')
        return redirect("App_Board:post_detail", board_id=board_id)
    
class post_delete(LoginRequiredMixin, generic.DeleteView):
    model = Board
    success_url = '/'
    template_name = 'Board_delete.html'
   
    def get_context_data(self, **kwargs):
        context = super(post_delete, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
