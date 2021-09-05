from django.urls import path, include
from .views import Posts, PostDetail, AddPost, DeletePost, PostEdit, AddComment, CommentDone, CommentsList, CommentDetail, CommentDelete, comment_accept, CommentSearch
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Posts.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('addpost', AddPost.as_view()),
    path('<int:pk>/delete', DeletePost.as_view()),
    path('<int:pk>/edit', PostEdit.as_view()),
    path('<int:pk>/comment', AddComment.as_view()),
    path('comment_done', CommentDone.as_view()),
    path('my_posts_comments', CommentsList.as_view()),
    path('my_posts_comments/search', CommentSearch.as_view()),
    path('my_posts_comments/<int:pk>', CommentDetail.as_view()),
    path('my_posts_comments/<int:pk>/accept', comment_accept),
    path('my_posts_comments/<int:pk>/delete', CommentDelete.as_view()),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
