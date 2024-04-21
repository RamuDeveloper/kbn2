from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Items
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    obj=Items.objects.all()
    return render(request,'index.html',{'obj':obj})

def products(request):
    if  request.method=='POST':
        name = request.POST['name']
        price = request.POST['price']   
        detail = request.POST['description']
        img=request.FILES.get('image')
        product=Items(name=name,price=price,description=detail,img=img)
        product.save()
        return redirect('/')
    return render(request,"product.html")

def delete_product(request,id):
    product=Items.objects.filter(id=id)
    product.delete()
    return redirect("/")

def edit(request,id):
    if request.method=="POST":
        obj=Items.objects.get(id=id)
        obj.name=request.POST['name']
        obj.price=request.POST['price']
        obj.description=request.POST['description']
        obj.img=request.FILES.get('image')
        obj.save()
        return redirect("/")

    product=Items.objects.get(id=id)
    return render(request,'edit.html',{'product':product})


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        name1=request.POST["firstName"]
        name2=request.POST["lastName"]
        username=request.POST["username"]
        password1=request.POST["password"]
        password2=request.POST["confirmPassword"]
        email=request.POST['email']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists! Please try another one.")
                return render(request,"register.html")
            elif User.objects.filter(email=email).exists():
                 messages.error(request,"email already exists! Please try another one.")
                 return render(request,"register.html")
            else:
                user=User.objects.create_user(first_name=name1,last_name=name2,username=username,password=password1,email=email)
                user.save()
                messages.success(request,"Registration Successful! You can now login.")
                return render(request,"login.html")
                
        else:
            messages.error(request,"Password didn't match with Confirmpassword")
    return render(request,'register.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        name1=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=name1, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfull")
            return redirect('/')
        else:
            messages.error(request,"Enter Correct Credentials!")
            return redirect('login')
    return  render(request,'login.html')

def user_logout(request):
    logout(request)
    return render(request,'login.html')
@login_required
def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')
