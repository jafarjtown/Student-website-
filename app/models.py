# app/models.py
from django.db import models

class Material(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    department = models.CharField(max_length=50)
    level = models.CharField(max_length=20)
    file = models.FileField(upload_to='materials/')

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
