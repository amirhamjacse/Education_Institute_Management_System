from django import forms
from institute_dashaboard.models import (
    OnlineAdmission, complain, Notice_board, News_headline
)

class NoticeBoardForm(forms.ModelForm):
    class Meta:
        model = Notice_board
        fields = ['title', 'img_or_pdf', 'notice_published_date', 'url_link']

class NewsdForm(forms.ModelForm):
    class Meta:
        model = News_headline
        fields = ['title', 'img_or_pdf', 'notice_published_date', 'url_link']
