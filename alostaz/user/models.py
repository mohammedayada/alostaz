from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class user(User):
    contributor = 'contributor'
    writer = 'writer'
    editor = 'editor'
    editor_in_chief = 'editor_in_chief'
    chairman = 'chairman'
    type_choice = [
        (contributor, 'مساهم'),
        (writer, "كاتب"),
        (editor, "محرر"),
        (editor_in_chief, "رئيس تحرير"),
        (chairman, "رئيس مجلس اداره"),
    ]
    type = models.CharField(max_length=15, choices=type_choice)
    name = models.CharField(max_length=125)
    phone = models.CharField(max_length=11, blank=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'name: {self.name} telephone number: {self.phone}'


class Advertising(models.Model):
    title = models.CharField(max_length=200, verbose_name='العنوان')
    img = models.ImageField(upload_to='Advertisement/', verbose_name='الصوره')

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=200, verbose_name='العنوان')
    img = models.ImageField(upload_to='Photos/', verbose_name='الصوره')

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Survey(models.Model):
    question = models.CharField(max_length=250, verbose_name='السؤال')
    first_choice = models.CharField(max_length=250, verbose_name='الأختيار الأول')
    yes = models.IntegerField(default=0, verbose_name='نعم')
    second_choice = models.CharField(max_length=250, verbose_name='الأختيار الثاني')
    no = models.IntegerField(default=0, verbose_name='لا')
    all = models.IntegerField(default=0, verbose_name='عدد الأصوات')
    approval = models.BooleanField(default=True, verbose_name='الأتاحه')

    def __str__(self):
        return self.question

    def yes_percentage(self):
        if self.all == 0:
            return 0
        else:
            return (self.yes / self.all) * 100

    def no_percentage(self):
        if self.all == 0:
            return 0
        else:
            return (self.no / self.all) * 100
