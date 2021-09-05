from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    data = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 255)
    text = RichTextUploadingField(blank = True, null = True)
    categories = [
        ('tank', 'tank'),
        ('healer', 'healer'),
        ('damage dealer', 'damage dealer'),
        ('vendor', 'vendor'),
        ('guildmaster', 'guildmaster'),
        ('questgiver', 'questgiver'),
        ('blacksmith', 'blacksmith'),
        ('leatherworker', 'leatherworker'),
        ('potion maker', 'potion maker'),
        ('spellmaster', 'spellmaster')
    ]
    category = models.CharField(max_length = 20, choices = categories)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    data = models.DateTimeField(auto_now_add = True)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    accepted = models.BooleanField(default = False)
