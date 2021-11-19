from django import forms
from django.db import models
from django.forms import fields, widgets
from .models import NoticeBoard


class NoticeBoardForm(forms.ModelForm):
    class Meta:
        model = NoticeBoard
        fields = ('notice',)
        widgets = {
            'notice':forms.TextInput(attrs={'class':'form-control'})
        }

# {{noticeboard.notice|safe}}

#   if request.method == "POST":
#       if form.is_valid():

#           post = form.save(commit=False)
#           post.voter = request.user
#           post.movie = Entry.objects.get(slug=slug)
#           post.save()
#           return redirect('/movies')