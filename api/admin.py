from django.contrib import admin
from .models import Category, User, Course, VideoClass

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(VideoClass)
admin.site.register(Category)