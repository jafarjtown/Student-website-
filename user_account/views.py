from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Account, User, Plan, PlanType
from app.models import Request 
from django.utils import timezone
from datetime import datetime


#Logout view
def user_logout(request):
    logout(request)
    return redirect("/")
# Login view
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "account/login.html")

# Registration view
def user_register(request):
    messages.info(request, "Sorry no registration can be done now.\nTo create an Account contact administrator.")
    return redirect("index")
    if request.method == "POST":
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists, please try again")
        else:
            first_name, *last_name = full_name.split(" ")
            user = User.objects.create_user(
                email=email,
                username=email,
                password=password,
                first_name=first_name,
                last_name=" ".join(last_name)
            )
            Account.objects.create(user=user)
            messages.success(request, "Account created successfully")
        
    return render(request, "account/register.html")

# Account settings view
def account_settings(request):
    context = {"plans":PlanType.objects.all()}
    if request.method == "POST":
        user = request.user
        user.last_name = request.POST.get("last_name")
        user.first_name = request.POST.get("first_name")
        user.save()
        messages.success(request, "Account updated successfully")
    
    return render(request, "account/settings.html", context)

# Update subscription view
def update_subscription(request):
    if request.method == "POST":
        user = request.user
        plan_id = int(request.POST.get("plan"))
        print(plan_id)
        planType = PlanType.objects.get(id=plan_id)
        plan,_ = Plan.objects.get_or_create(user=user)
        plan.type = planType
        #plan.last_due = timezone.now()
        
        plan.save()
        messages.success(request, f"You have subscribed to {plan.type.name}")
    
    return redirect("account_settings")

# Delete account view
def delete_account(request):
    if request.method == "POST":
        user = request.user
        password = request.POST.get("password")
        password_correct = user.check_password(password)
        
        if password_correct:
            #Perform account deletion and logout if needed
            #logout(request)
            user.delete()
            messages.info(request, "Account deleted")
        else:
            messages.error(request, "Incorrect password")
            return redirect("account_settings")
    
    return redirect("/")

# Other views: make_request, update_user - no changes made
def make_request(request):
    if request.method == "POST":
        post = request.POST
        req = Request()
        req.body = post.get("request")
        req.topic = post.get("topic")
        req.priority = post.get("priority")
        req.type = post.get("type")
        req.email = post.get("email")
        req.save()
        messages.success(request,"Request is submitted")
    return render(request, "account/request.html")

def update_user(request):
    if request.method == "POST":
        user = request.user
        user.last_name = request.POST.get("last_name")
        user.first_name = request.POST.get("first_name")
        user.save()
        messages.success(request, "Account updated successfully")
    return redirect("account_settings")
