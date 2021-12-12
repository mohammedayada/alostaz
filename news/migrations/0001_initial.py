# Generated by Django 3.2.4 on 2021-08-03 16:25

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='العنوان')),
                ('link', models.URLField(verbose_name='الرابط')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='العنوان')),
                ('Publish_date', models.DateTimeField(auto_now_add=True)),
                ('details', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='البيانات')),
                ('img', models.ImageField(upload_to='books/', verbose_name='الصوره')),
                ('viewCount', models.IntegerField(default=0, verbose_name='عدد المشاهديين')),
            ],
            options={
                'ordering': ['-Publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Carton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='العنوان')),
                ('Publish_date', models.DateTimeField(auto_now_add=True)),
                ('details', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='البيانات')),
                ('img', models.ImageField(upload_to='books/', verbose_name='الصوره')),
                ('viewCount', models.IntegerField(default=0, verbose_name='عدد المشاهديين')),
            ],
            options={
                'ordering': ['-Publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='اسم القسم')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('auther', models.CharField(max_length=100)),
                ('Publish_date', models.DateTimeField(auto_now_add=True)),
                ('approval', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='العنوان')),
                ('Publish_date', models.DateTimeField(auto_now_add=True)),
                ('details', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='البيانات')),
                ('img', models.ImageField(upload_to='', verbose_name='الصوره')),
                ('approval', models.BooleanField(default=False, verbose_name='الموافقه')),
                ('viewCount', models.IntegerField(default=0, verbose_name='عدد المشاهديين')),
                ('commentCount', models.IntegerField(default=0, verbose_name='عدد التعليقات')),
            ],
            options={
                'ordering': ['-Publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='العنوان')),
                ('link', models.URLField(verbose_name='الرابط')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='العنوان')),
                ('link', models.URLField(verbose_name='الرابط')),
            ],
        ),
        migrations.CreateModel(
            name='Tag_news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.tag')),
            ],
        ),
    ]