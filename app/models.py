# app/models.py
from django.db import models
from django.contrib.auth.models import User



class Department(models.Model):
    name = models.CharField(max_length=50)
    slogan = models.TextField()

class Material(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    file = models.FileField(upload_to='materials/')
    comment= models.TextField()
    @property
    def code(self):
        return self.course.code
    
    @property
    def title(self):
        return self.course.title
    @property
    def department(self):
        return self.course.department
    @property 
    def size(self):
        file_size = self.file.size
        if file_size < 1024:
            return f"{file_size} bytes"
        elif 1024 <= file_size < 1024 * 1024:
            return f"{file_size // 1024} KB"
        else:
            return f"{file_size // (1024 * 1024)} MB"

    def __str__(self):
        return self.title


class TimeTable(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    level = models.CharField(max_length=3)
    original = models.FileField(upload_to="timetable/org/")
    modified = models.FileField(upload_to="timetable/mod/")
    
    
class Course(models.Model):
    code = models.CharField(max_length=8)
    title = models.CharField(max_length=50)
    info = models.TextField()
    outline = models.FileField(upload_to="courses/outlines/")
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    
    
class Outline(models.Model):
    lecturer = models.TextField()
    topics = models.ManyToManyField("Topic", blank=False)
    cu = models.IntegerField(default=2)
    
    
class Topic(models.Model):
    title = models.CharField(max_length = 100)
    note = models.TextField()
    sub_topics = models.ManyToManyField("Topic", blank=True)

class BlogBase(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField()
    
    class Meta:
        abstract = True
    
class Blog(BlogBase):
    pass

class Comment(BlogBase):
    blog = models.ForeignKey("Blog", on_delete = models.CASCADE)
    reply = models.ManyToManyField("Comment", blank=True)
