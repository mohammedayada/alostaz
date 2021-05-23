from django.db import models
from django.conf import settings


# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class News(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    Publish_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    img = models.ImageField()
    approval = models.BooleanField(default=False)
    viewCount = models.IntegerField(default=0)

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


class Advertising(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    img = models.ImageField()

    def __str__(self):
        return f'Title: {self.title} user: {self.user.name}'

class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images/')
    def __str__(self):
        return f'Title: {self.title} user: {self.user}'

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