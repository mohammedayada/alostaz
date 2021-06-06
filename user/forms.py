from django import forms
from news.models import News, Category
from .models import Photo, Advertising


class NewsForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = News
        exclude = ['user', 'approval', 'viewCount']

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'name': 'العنوان'}),
        'category': forms.TextInput(attrs={'class': 'form-control', 'name': 'القسم'}),

    }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields= '__all__'


class AdvertisingForm(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = '__all__'
