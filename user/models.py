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
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='Advertisement/')

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='Photos/')

    def __str__(self):
        return self.title
