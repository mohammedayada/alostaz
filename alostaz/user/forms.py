from django import forms
from news.models import News, Category, Book, Video, Audio, TV
from .models import Photo, Advertising, Survey


class NewsForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = News
        exclude = ['user', 'approval', 'viewCount', 'commentCount']

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'name': 'العنوان'}),
        'category': forms.TextInput(attrs={'class': 'form-control', 'name': 'القسم'}),

    }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['user', 'viewCount']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'


class AdvertisingForm(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = '__all__'


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ['yes', 'no', 'all']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = '__all__'

class TVForm(forms.ModelForm):
    class Meta:
        model = TV
        fields = '__all__'