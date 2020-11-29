from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            form = RegisterForm()
            return redirect("/")
        else:
            messages.error(response, 'Registration failed.')       
    else:
	    form = RegisterForm()
    return render(response, "register.html", {"form":form})
