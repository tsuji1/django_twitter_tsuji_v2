from django.shortcuts import render

def homepage(request):
    return render(request,'twitter/homepage.html',{})

# Create your views here.
