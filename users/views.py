from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/registern.html')

def profile(request):
    return render(request, 'users/profile.html')

def logout(request):
    return render(request, 'users/login.html')
