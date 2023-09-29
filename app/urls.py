# app/urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('materials/', views.material_list, name='material_list'),   
    path('search/materials/', views.search_materials, name='search'),
    path("api/courses/<int:dep>/<int:lev>/", views.courses_api, name="courses-api"),
    path("timetables/", views.timetable_view, name="timetables"),
    path("timetables/<int:id>/", views.timetable, name="timetable"),
        path("courses/", views.courses, name="course"),
        path("courses/<int:cid>/outline", views.upload_outline, name="upload_outline"),
        path("courses/<int:cid>/flag-issue", views.flag_course, name="flag_course"),
        path("materials/<int:mid>/flag-issue", views.flag_material, name="flag_material"),
        path("register_newsletter/", views.register_newsletter, name="register_newsletter"),

]
