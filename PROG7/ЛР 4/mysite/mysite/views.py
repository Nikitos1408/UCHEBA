from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    """
    Регистрация нового пользователя.
    После успешной регистрации пользователь автоматически авторизуется
    и перенаправляется на список опросов.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("polls:index")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


