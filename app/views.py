# app/views.py
from django.shortcuts import render,redirect
from django.http import JsonResponse 
from .models import Material, Department , Course, TimeTable, CourseComment , FlaggedIssue

from django.contrib import messages

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
        messages.success(request, "Material added successful")


    return render(request, 'app/upload.html', context)


def material_list(request):
    departments = Department.objects.all()
   
    levels = [100, 200, 300, 400]
    
    context = {"departments":departments}
    context["levels"] = levels 
    level = request.GET.get("level")
#    
    department_id = request.GET.get("department")
    course_code = request.GET.get("course")
#    
    if department_id and course_code:
        department = departments.get(id = department_id)
        course = department.course_set.get(code = course_code)
        context["course"] = course
        materials = course.material_set.all()
    
        context["materials"] = materials 
        if level:
            context["level"] = int(level)
        context["department"] = department.id
    else:
        context["materials"] = Material.objects.all()

    return render(request, 'app/list.html', context)


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
        department = int(request.GET.get("department"))
        level = request.GET.get("level")
        course = request.GET.get("course")
        
        dep = Department.objects.prefetch_related("course_set").get(id = department)
        course = dep.course_set.get(code = course)
        if request.method == "POST":
             user = request.POST.get("user")
             comment = request.POST.get("comment")
             if user == "":
                    user = "Anonymous User"
             c = CourseComment(user=user, comment=comment, course=course)
             c.save()
        context["course"] = course
        if level: 
            context["level"] = int(level)
        context["department"] = dep.id
    return render(request, "app/course.html", context)
    
    
def upload_outline(request, cid):
    course = Course.objects.get(id = cid)
    if request.method == "POST":
        
        file = request.FILES.get("outline")
        course.outline = file
        course.save()
        messages.success(request, "Course outline uploaded successful")
    return render(request, "app/course_outline.html", {"course":course})

def flag_course(request, cid):
    course = Course.objects.get(id = cid)
    context = {"course": course}
    if request.method == "POST":
        response = request.POST.get("response")
        
        issue = FlaggedIssue(response=response, issued_object=course)
        issue.save()
        context["flag_id"] = issue.id
        messages.info(request, "Issue reported successful.")
        
    return render(request, "app/flag_course.html", context)