from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect("accounts:login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})
