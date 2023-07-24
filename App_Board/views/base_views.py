from django.shortcuts import render, get_object_or_404
from ..models import *


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
    board.counting += 1 
    board.save()
    categories = Category.objects.all()
    current_category = get_object_or_404(Category, id = board.category.id)
    context = { 
        'board':board, 
        'categories' : categories, 
        'current_category': current_category,
      }
    return render(request, 'Board_post.html', context)   
