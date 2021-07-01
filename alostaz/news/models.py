from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.db.models import Q

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    def all_news(self):
        return News.objects.filter(Q(Q(category=self) & Q(approval=True)) | (Q(category__parent=self) & Q(approval=True)) | (Q(category__parent__parent=self) & Q(approval=True)))[:9]


class News(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE, related_name='NEWS', verbose_name='القسم')
    title = models.CharField(max_length=200, verbose_name='العنوان')
    Publish_date = models.DateTimeField(auto_now_add=True)
    details = RichTextField(blank=True, null=True, verbose_name='البيانات')
    img = models.ImageField(verbose_name='الصوره')
    approval = models.BooleanField(default=False, verbose_name='الموافقه')
    viewCount = models.IntegerField(default=0, verbose_name='عدد المشاهديين')
    commentCount = models.IntegerField(default=0, verbose_name='عدد التعليقات')
    class Meta:
        ordering = ['-Publish_date']

    def __str__(self):
        return f'Title: {self.title} user: {self.user}'

    def incrementViewCount(self):
        self.viewCount += 1
        self.save()


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    email = models.EmailField()
    text = models.TextField()
    auther = models.CharField(max_length=100)
    Publish_date = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return f'email: {self.email} news: {self.news.title} comment: {self.text} date: {self.Publish_date} approval: {self.approval}'


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'Title: {self.title} user: {self.user}'


class Tag(models.Model):
    text = models.CharField(max_length=20)

    def __str__(self):
        return f'Text: {self.text}'


class Tag_news(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('news', 'tag',)

    def __str__(self):
        return f'Tag: {self.tag} news: {self.news}'
