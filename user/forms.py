from django import forms
from news.models import News, Category
class NewsForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = News
        exclude = ['user', 'approval', 'viewCount']

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'name': 'العنوان'}),
        'category': forms.TextInput(attrs={'class': 'form-control', 'name': 'القسم'}),

    }


