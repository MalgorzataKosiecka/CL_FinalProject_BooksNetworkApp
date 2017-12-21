from django import forms
import datetime


class UserLoginForm(forms.Form):

    username = forms.CharField(max_length=150, label="Nazwa użytkownika")
    password = forms.CharField(max_length=150, label="Hasło", widget=forms.PasswordInput)


class BookSearchForm(forms.Form):

    search = forms.CharField(label="Wyszukaj książkę", max_length=150)


class ReserveBookForm(forms.Form):

    date_from = forms.DateField(label="Pożyczam od dnia", initial=datetime.date.today)
    date_to = forms.DateField(label="Pożyczam do dnia", initial=datetime.date.today)

