# app/views.py
from django.shortcuts import render,redirect
from .models import Material

def index(request):
    return render(request, 'app/index.html')
    
def upload(request):

    if request.method == 'POST':
        # Retrieve material properties from the request body
        code = request.POST.get('code')
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        department = request.POST.get('department')
        level = request.POST.get('level')
        file = request.FILES.get('file')

        # Create a new Material instance and save it to the database
        material = Material(code=code, title=title, comment=comment, department=department, level=level, file=file)
        material.save()

        # Redirect to the home page or any other desired URL
        return redirect('index')  # Replace 'index' with the appropriate URL name

    return render(request, 'app/upload.html')


def material_list(request):
    d = {
        "0": "All",
        "solg": "Sociology",
        "mascom":"Mass Communication",
        "pols":"Political Science",
        "ints": "International Studies"
    }
    department_query = request.GET.get('department')
    level_query = request.GET.get('level')
    if department_query == "0":
        department_query = None
    if level_query == "000":
        level_query = None
    if department_query  and level_query:
        materials = Material.objects.filter(department=department_query, level=level_query)
    elif department_query:
        materials = Material.objects.filter(department=department_query)
    elif level_query:
        materials = Material.objects.filter(level=level_query)
    else:
        materials = Material.objects.all()

    return render(request, 'app/list.html', {'materials': materials, "department": d.get(department_query), "level": level_query})


def search_materials(request):
    search_query = request.GET.get('q')

    if search_query:
        materials = Material.objects.filter(code__icontains=search_query) | \
                    Material.objects.filter(title__icontains=search_query)
    else:
        materials = Material.objects.all()

    return render(request, 'app/search.html', {'materials': materials, "q": search_query})
# app/views.py
#from django.shortcuts import render
#from .models import Material
#from .filters import MaterialFilter

#def search_materials(request):
#    search_query = request.GET.get('q')
#    material_filter = MaterialFilter(request.GET, queryset=Material.objects.all())
#    return render(request, 'app/search.html', {'filter': material_filter, "q": search_query})
