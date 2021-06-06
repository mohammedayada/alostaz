from django.contrib import admin
from .models import user, Advertising, Photo
# Register your models here.

admin.site.register(user)
admin.site.register(Advertising)
admin.site.register(Photo)
