from django import forms


class UserLoginForm(forms.Form):

    username = forms.CharField(max_length=150, label="Nazwa użytkownika")
    password = forms.CharField(max_length=150, label="Hasło", widget=forms.PasswordInput)


class BookSearchForm(forms.Form):

    search = forms.CharField(label="Wyszukaj książkę", max_length=150)

