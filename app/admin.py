from django.contrib import admin

from .models import Course, Outline, Department
# Register your models here.

admin.site.register(Course)
admin.site.register(Outline)
admin.site.register(Department)