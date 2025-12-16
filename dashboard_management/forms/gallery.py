# forms.py
from django import forms
from institute_dashaboard.models import (
    Gallery, complain, Notice_board, News_headline
)

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'gallery_photo']
