from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, 'You have registered successfully. Go to login page.')
            form = RegisterForm()
        else:
            messages.error(request, 'Registration failed.')
        #return redirect("/")
    else:
	    form = RegisterForm()

    return render(response, "register.html", {"form":form})
