from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View

from .forms import UserLoginForm, BookSearchForm, ReserveBookForm, BookAddForm
from .models import Book, BookOwned, BookReserved


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
        books_reserved = BookReserved.objects.filter(username=request.user)
        return render(request, "user-main.html", {"form": form, "user_list": user_list, "username": username,
                                                  "books_reserved": books_reserved})

    def post(self, request):
        form = BookSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            results = Book.objects.annotate(search=SearchVector("title", "author", "publishing_house"),
                                            ).filter(search__icontains=search)
            return render(request, "book-search.html", {"form": form, "results": results})


class AllBooksView(LoginRequiredMixin, View):

    def get(self, request):
        books = Book.objects.all().order_by("title")
        return render(request, "all-books.html", {"books": books})


class SpecificBookView(LoginRequiredMixin, View):

    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            return render(request, "specific-book.html", {"book": book})
        except:
            return HttpResponseRedirect("/logged-user/")


class ReserveBookView(LoginRequiredMixin, View):

    def get(self, request, book_id, owner_id):
        form = ReserveBookForm()
        book = Book.objects.get(pk=book_id)
        owner = User.objects.get(pk=owner_id)
        return render(request, "reserve-book.html", {"form": form, "book": book, "owner": owner})

    def post(self, request, book_id, owner_id):
        form = ReserveBookForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(pk=book_id)
            owner = User.objects.get(pk=owner_id)
            new_borrowing = BookReserved.objects.create(username=request.user,
                                                        owner=owner,
                                                        book=book,
                                                        date_from=form.cleaned_data["date_from"],
                                                        date_to=form.cleaned_data["date_to"])
            return HttpResponseRedirect("/logged-user/", {"form": form, "new_borrowing": new_borrowing})
        else:
            return HttpResponse("/logged-user/")


class AddBookView(LoginRequiredMixin, View):

    def get(self, request):
        form = BookAddForm()
        return render(request, "add-book.html", {"form": form})

    def post(self, request):
        form = BookAddForm(request.POST)
        if form.is_valid():
            new_book = Book.objects.create(title=form.cleaned_data["title"],
                                           author=form.cleaned_data["author"],
                                           publishing_house=form.cleaned_data["publishing_house"],
                                           year_published=form.cleaned_data["year_published"],
                                           book_kind=form.cleaned_data["book_kind"],
                                           print_kind=form.cleaned_data["print_kind"])
            return HttpResponseRedirect("/logged-user/", {"form": form, "new_book": new_book})

