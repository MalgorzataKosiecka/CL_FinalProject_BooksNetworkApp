from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import UserLoginForm, BookSearchForm
from .models import Book, BookOwned


class UserLoginView(View):

    def get(self, request):
        form = UserLoginForm()
        return render(request, "main-page.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_authenticated = authenticate(username=username, password=password)
            if user_authenticated:
                login(request, user_authenticated)
                return HttpResponseRedirect("/logged-user")
            else:
                login_message = "Podano nieprawidłowy login lub hasło."
                return render(request, "main-page.html", {"form": form, "login_message": login_message})
        return render(request, "main-page.html", {"form": form})


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class UserMainPageView(LoginRequiredMixin, View):

    def get(self, request):
        form = BookSearchForm()
        user_list = Book.objects.filter(owned_by=request.user)
        username = User.objects.filter(username=request.user)
        # all_books = Book.objects.all()
        # username = all_books.owned_by.all()
        return render(request, "user-main.html", {"form": form, "user_list": user_list, "username": username})

    def post(self, request):
        form = BookSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            results = Book.objects.annotate(search=SearchVector("title", "author", "publishing_house"),
                                            ).filter(search__icontains=search)
            return render(request, "book-search.html", {"form": form, "results": results})

