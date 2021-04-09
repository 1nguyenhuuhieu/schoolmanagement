from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate

def index(request):

    if request.user.is_authenticated:
        return render(request, 'base.html', context)
    else:
        return redirect(login)

def login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(username=username, password=pwd)

        if user is not None:
            login(request, user)
        else:
            print("fuck wrong")
    context = {}
    return render(request, 'login.html', context)



    