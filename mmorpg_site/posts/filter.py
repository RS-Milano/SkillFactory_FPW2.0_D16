from django_filters import FilterSet
from .models import Comment

class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'author': ['exact'],
            'data': ['gt'],
            'text': ['icontains']
        }
