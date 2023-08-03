from App_Auth.models import User
from App_Board.models import Category
user = User.objects.get(id = 1)
category = Category.objects.get(name = "자유게시판")
for i in range(10,50):
    user.board_set.create(category = category,
                          post_author = user,
                          post_name = f"[{i+1}]자유 게시판 작성 테스트",
                          post_content = "테스트\n"*30)
     