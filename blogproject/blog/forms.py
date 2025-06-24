from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'category', 'tags') #author excluded (set automatically)