from email.policy import default
from pyexpat import model
from turtle import title
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_instructor = models.BooleanField(default=False)

class Course(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=180)
    created_at = models.DateTimeField(auto_now_add= True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_list_instructor")
    students = models.ManyToManyField(User, related_name='course_list', blank=True)
    cover = models.ImageField(upload_to='courses_covers/', validators=[])

    def __str__(self):
        return self.name

class VideoClass(models.Model):
    title = models.TextField(max_length=50)
    video = models.FileField(upload_to="videos/")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="videoclass_list")

    def __str__(self):
        return f"{self.title} - {self.course.name} - {self.course.id}"

class Category(models.Model):
    name = models.TextField(max_length=50)
    courses = models.ManyToManyField(Course, related_name='course_list')
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    score = models.IntegerField()
    comment = models.TextField(max_length=255)