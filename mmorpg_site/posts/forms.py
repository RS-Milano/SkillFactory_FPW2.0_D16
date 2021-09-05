from django.forms import ModelForm, fields
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']