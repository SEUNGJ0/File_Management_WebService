from django.contrib import messages
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
# 함수형 뷰에서 사용하는 권한 제한
from django.contrib.auth.decorators import login_required
# 클레스형 뷰애서 사용하는 권한 제한
from django.contrib.auth.mixins import LoginRequiredMixin


def board_home(request):
    categories = Category.objects.all()
    return render(request, 'Board_home.html',{'categories' : categories})

def post_in_category(request, category_slug = None):
    current_category = None
    categories = Category.objects.all()
    boards = Board.objects.all()

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        boards = boards.filter(category=current_category)

    context = {'current_category' : current_category, 'categories' : categories, 'boards' : boards}
    return render(request, 'Board_index.html', context)
    
def post_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    categories = Category.objects.all()
    current_category = get_object_or_404(Category, id = board.category.id)
    context = { 
        'board':board, 
        'categories' : categories, 
        'current_category': current_category,
      }
    return render(request, 'Board_post.html', context)   

@login_required(login_url='App_Auth:login')
def post_create(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        if request.POST['action'] == 'save':
            form = BoardForm(request.POST, request.FILES)
            print('save 진행 1')
            if form.is_valid():
                print('save 진행 2')
                # 게시판 폼에 추가
                Board = form.save(commit=False)
                Board.created_date = timezone.now()
                Board.category = get_object_or_404(Category, id=category_id)
                Board.post_author = request.user
                Board.save()   
                print("보드 저장")
                return redirect("App_Board:post_detail", Board.id)
            return render(request, 'Board_create.html',{'categories' : categories, 'current_category' : category,})
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

