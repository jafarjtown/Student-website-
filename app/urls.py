# app/urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('material_list/', views.material_list, name='material_list'),   
    path('search_materials/', views.search_materials, name='search'),
    path("api/courses/<int:dep>/<int:lev>/", views.courses_api, name="courses-api"),
    path("timetables/", views.timetable_view, name="timetables"),
    path("timetables/<int:id>/", views.timetable, name="timetable"),
        path("course/", views.courses, name="course"),
]
