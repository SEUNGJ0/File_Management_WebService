from django.shortcuts import render, get_object_or_404
from App_Board.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# 메인 페이지 
def mainpage_render_view(request):
    all_category = Category.objects.all()
    return render(request, 'Board_home.html',{'all_category' : all_category})

# 카테고리별 게시판 페이지
def board_render_view(request, category_slug = None):
    all_category = Category.objects.all()
    all_board = Board.objects.all()
    
    if category_slug:
        select_category = get_object_or_404(Category, slug=category_slug)
        select_board = all_board.filter(category=select_category)
        page = request.GET.get('page', '1')
        page_obj = pagination(page, select_board, 5)
    else:
        select_category = None
    
    context = {
        'select_category' : select_category, 
        'all_category' : all_category, 
        'select_board' : page_obj,
        'page_obj': page_obj
        }
    return render(request, 'Board_index.html', context)
    
# 게시글 상세 페이지
def post_render_view(request, board_id):
    all_category = Category.objects.all()
    select_post = get_object_or_404(Board, id=board_id)
    select_post.post_views_counting += 1 
    select_post.save()
    for key, value in request.session.items():
        print(f"Key: {key}, Value: {value}")
    editlogs = select_post.editlogs.all()
    select_category = get_object_or_404(Category, id = select_post.category.id)
    if select_category == "자료 취합":
        pass
    else:
        context = { 
            'select_post':select_post, 
            'all_category' : all_category, 
            'select_category': select_category,
            'editlogs' : editlogs,
        }
    return render(request, 'Board_post.html', context)

def pagination(page, model, set_num):
    # Paginator(쿼리셋, 한 페이지에 몇개의 포스트를 볼지 설정)
    paginator = Paginator(model, set_num)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger: # page 값이 없을 때
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage: # page를 너무 크게 입력하는 경우
        page = paginator.num_pages # 가장 마지막 page를 출력
        page_obj = paginator.page(page)
    return page_obj
   
