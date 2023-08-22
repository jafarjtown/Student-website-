# app/views.py
from django.shortcuts import render,redirect
from django.http import JsonResponse 
from .models import Material, Department , Course, TimeTable

def index(request):
    return render(request, 'app/index.html')
    
def upload(request):
    context = {
            "departments": Department.objects.all()
    }
    if request.method == 'POST':
        course = request.POST.get('course')
        comment = request.POST.get('comment')
        department = request.POST.get('department')
        file = request.FILES.get('file')

        course = Course.objects.get(department__id = department, code = course)
        
        material = Material(course=course, comment=comment, file=file)
        material.save()


    return render(request, 'app/upload.html', context)


def material_list(request):
    departments = Department.objects.all()
    department_query = request.GET.get('department')
    level_query = request.GET.get('level')
    if department_query == "0":
        department_query = None
    if level_query == "000":
        level_query = None
    if department_query  and level_query:
        materials = Material.objects.select_related("course").filter(course__department__name=department_query,course__code__icontains=level_query[0])
    elif department_query:
        materials = Material.objects.select_related("course").filter(course__department__name=department_query)
    elif level_query:
        materials = Material.objects.select_related("course").filter(course__code__icontains=level_query[0])
    else:
        materials = Material.objects.select_related("course").all()

    return render(request, 'app/list.html', {'materials': materials, "department": department_query, "level": level_query, "departments": departments})


def search_materials(request):
    search_query = request.GET.get('q')

    if search_query:
        materials = Material.objects.select_related("course").filter(course__code__icontains=search_query) | \
                    Material.objects.select_related("course").filter(course__title__icontains=search_query)
    else:
        materials = Material.objects.all()

    return render(request, 'app/search.html', {'materials': materials, "q": search_query})


def courses_api(request, dep, lev):
    department = Department.objects.get(id = dep)
    courses = department.course_set.filter(code__gte=lev)
    courses = courses.filter(code__lt=(lev+100)).values("code", "title")
    
    return JsonResponse({"data": tuple(courses)})

def timetable_view(request):
    timetables = TimeTable.objects.all()
    return render(request , "app/timetable_view.html", {"timetables": timetables })


def timetable(request, id):
    time_table = TimeTable.objects.get(id = id)
    return render(request, "app/timetable.html", {"timetable": time_table})
    
    
def courses(request):
    context = {"departments": Department.objects.all(), "levels":[100, 200,300,400]}
    if request.GET.get("department") and request.GET.get("course"):
        department = request.GET.get("department")
        level = request.GET.get("level")
        course = request.GET.get("course")
        
        dep = Department.objects.prefetch_related("course_set").get(id = department)
        course = dep.course_set.get(code = course)
        context["course"] = course 
        context["level"] = int(level)
        context["department"] = dep.id
    return render(request, "app/course.html", context)