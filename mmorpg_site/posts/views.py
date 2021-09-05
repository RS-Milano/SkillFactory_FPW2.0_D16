from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import Post, Comment
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .filter import CommentFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
 
class Posts(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-data']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['limit_for_listing'] = Paginator(list(Post.objects.all()), 5).num_pages - 2
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class AddPost(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'addpost.html'
    context_object_name = 'post' #
    form_class = PostForm #

    def get_context_data(self, **kwargs):  #
        context = super().get_context_data(**kwargs) #
        context['form'] = PostForm() #
        return context #

    def post(self, request, *args, **kwargs):
        # title = request.POST['title']
        # text = request.POST['text']
        # author = request.user.id
        # category = request.POST['category']
        # post = Post(author=User.objects.get(id=author), title=title, text=text, category=category)
        # post.save()
        # return HttpResponseRedirect(f'{post.id}')
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    success_url = '/../../'

class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    fields = []
    template_name = 'editpost.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.get_full_path().split("/")[2])
        post.title = request.POST['title']
        post.text = request.POST['text']
        post.category = request.POST['category']
        post.save()
        return HttpResponseRedirect(f"../{post.id}")

class AddComment(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'comment.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        text = request.POST['text']
        author = request.user.id
        comment = Comment(author=User.objects.get(id=author), text=text, post=Post.objects.get(id=request.get_full_path().split("/")[2]))
        comment.save()
        return HttpResponseRedirect('/posts/comment_done')

class CommentDone(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'comment_done.html'

class CommentsList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments_list.html'
    context_object_name = 'comments'
    paginate_by = 5
    ordering = ['-data']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_posts = Post.objects.filter(author=User.objects.get(id=self.request.user.id))
        comments_for_my_posts = []
        for i in my_posts:
            if Comment.objects.filter(post=i):
                comments_for_my_posts.append(Comment.objects.filter(post=i))
        context['comments_for_my_posts'] = comments_for_my_posts
        context['limit_for_listing'] = Paginator(comments_for_my_posts, 5).num_pages - 2
        return context

class FilteredComment(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'searchcomment.html'
    context_object_name = 'comments'
    ordering = ['-data']
    filterset_class = None
        
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.all()

    def get_page_param(self):
        page_param = self.request.GET.get("page", None)
        return page_param

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['authors'] = User.objects.all()
        context['paginate'] = self.paginate_by
        my_posts = Post.objects.filter(author=User.objects.get(id=self.request.user.id))
        comments_for_my_posts = []
        for i in my_posts:
            if Comment.objects.filter(post=i):
                comments_for_my_posts.append(Comment.objects.filter(post=i))
        context['all_comments'] = comments_for_my_posts
        context['page_param'] = self.get_page_param()
        context['limit_for_listing'] = Paginator(comments_for_my_posts, 5).num_pages - 2
        context['object_list'] = comments_for_my_posts
        return context

class CommentSearch(FilteredComment):
    filterset_class = CommentFilter
    ordering = ['-data']
    paginate_by = 5

class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'commentdetail.html'
    context_object_name = 'comment'

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'commentdelete.html'
    context_object_name = 'comment'
    queryset = Comment.objects.all()
    success_url = '/posts/my_posts_comments'

def comment_accept(request, **kwargs):
    my_comment = Comment.objects.get(id=request.get_full_path().split('/')[3])
    my_comment.accepted = True
    my_comment.save()
    return redirect('/posts/my_posts_comments')