# app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import mimetypes
def materials_directory_path(instance, filename):
    
    return f"materials/{instance.department.name}/{instance.code}/{filename}"


class Department(models.Model):
    name = models.CharField(max_length=50)
    slogan = models.TextField()

class Material(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    file = models.FileField(upload_to=materials_directory_path)
    comment= models.TextField()
    
    @property
    def type(self):
        types = {
                        "audio":["mp3", "mpeg"],
                        "video":["mp4"],
                        "pdf":["pdf", "docx"],
                        "img": ["jpg" "jpeg", "png"]
        }
        mime_type, _ = mimetypes.guess_type(self.file.name)
        if mime_type:
            main_type, sub_type = mime_type.split('/')
            return main_type
            #for k, v in types.items():
#                print(sub_type, main_type)
#                if sub_type in v:
#                    return k
#            return "files"
        return "files"
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
    modified = models.FileField(upload_to="timetable/mod/", null=True)
    
    
class Course(models.Model):
    code = models.CharField(max_length=8)
    title = models.CharField(max_length=50)
    info = models.TextField()
    outline = models.FileField(upload_to="courses/outlines/", null=True)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    
    def comments_set(self):
        return self.comments.all().order_by("-posted_on")[:10]
    

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

class CourseComment(models.Model):
    user = models.CharField(max_length=20)
    comment = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    posted_on = models.DateTimeField(auto_now_add=True)
    
    
    
class FlaggedIssue(models.Model):
    response = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    issued_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]