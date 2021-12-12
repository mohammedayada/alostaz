from django.db import models
# from django.contrib.auth.models import User
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')
        user = self.create_user(
            email,
            password,
            **extra_fields
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'ADMIN'
    STAFF = 'STAFF'
    role_choice = [
        (ADMIN, ADMIN),
        (STAFF, STAFF),
    ]
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
    username = None
    type = models.CharField(max_length=15, choices=type_choice)
    name = models.CharField('name', max_length=125)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField('email', max_length=125, unique=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)
    is_superuser = models.BooleanField('is_superuser', default=False)
    role = models.CharField('role', max_length=125, choices=role_choice)
    is_staff = models.BooleanField('is_staff', default=False)
    is_active = models.BooleanField('is_active', default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.role == User.ADMIN:
            self.is_superuser = True
            self.is_staff = True
            self.can_view_bar_code = True
        super(User, self).save(*args, **kwargs)


# Create your models here.
# class user(User):
#     contributor = 'contributor'
#     writer = 'writer'
#     editor = 'editor'
#     editor_in_chief = 'editor_in_chief'
#     chairman = 'chairman'
#     type_choice = [
#         (contributor, 'مساهم'),
#         (writer, "كاتب"),
#         (editor, "محرر"),
#         (editor_in_chief, "رئيس تحرير"),
#         (chairman, "رئيس مجلس اداره"),
#     ]
#     type = models.CharField(max_length=15, choices=type_choice)
#     name = models.CharField(max_length=125)
#     phone = models.CharField(max_length=11, blank=True)
#     USERNAME_FIELD = 'email'
#
#     def __str__(self):
#         return f'name: {self.name} telephone number: {self.phone}'


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
