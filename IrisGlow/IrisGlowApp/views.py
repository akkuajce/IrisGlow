from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html',)
def about(request):
    return render(request,'about.html',)
def appointment(request):
    return render(request,'appointment.html',)
def login(request):
    return render(request,'login.html',)
def register(request):
    return render(request,'register.html',)
def testimonial(request):
    return render(request,'testimonial.html',)
def login(request):
    return render(request,'login.html',)
