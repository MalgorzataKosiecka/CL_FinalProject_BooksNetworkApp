from django.contrib.auth.models import User
from django.db import models


BOOK_KIND = (
    (1, "akcja, sensacja, kryminał, horror"),
    (2, "science-fiction"),
    (3, "fantastyka"),
    (4, "obyczajowa"),
    (5, "klasyka, literatura piękna, poezja"),
    (6, "romans"),
    (7, "biografie, pamiętniki"),
    (8, "historyczne, literatura faktu"),
    (9, "literatura naukowa i popularnonaukowa"),
    (10, "poradniki"),
    (11, "podręczniki, języki obce"),
    (12, "komiks"),
    (13, "opowiadania"),
    (14, "dla dzieci i młodzieży"),
    (15, "inne"),
)


PRINT_KIND = (
    (1, "książka, oprawa twarda"),
    (2, "książka, oprawa miękka"),
    (3, "ebook"),
    (4, "audiobook"),
    (5, "podanie słowne"),
)


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tytuł")
    author = models.CharField(max_length=255, verbose_name="Autor")
    publishing_house = models.CharField(max_length=255, verbose_name="Wydawnictwo")
    year_published = models.IntegerField(verbose_name="Rok wydania")
    book_kind = models.IntegerField(choices=BOOK_KIND, verbose_name="Kategoria")
    print_kind = models.IntegerField(choices=PRINT_KIND, verbose_name="Forma wydania")
    description = models.TextField(verbose_name="Opis")
    owned_by = models.ManyToManyField(User, through="BookOwned", related_name="owner_name",
                                      verbose_name="Właściciel")
    reserved_by = models.ManyToManyField(User, through="BookReserved", related_name="borrower_name",
                                         verbose_name="Zamawiający")

    def __str__(self):
        return '"{}", {}, wyd. {}, rok wydania {}, {}, {}, opis: {}'.\
            format(self.title, self.author, self.publishing_house, self.year_published, self.book_kind,
                   self.print_kind, self.description)


class BookOwned(models.Model):
    username = models.ForeignKey(User, on_delete=None)
    book = models.ForeignKey(Book, on_delete=None)


class BookReserved(models.Model):
    username = models.ForeignKey(User, on_delete=None, related_name="borrower_name")
    owner = models.ForeignKey(User, on_delete=None, related_name="owner_name")
    book = models.ForeignKey(Book, on_delete=None)
    date_from = models.DateField()
    date_to = models.DateField()
    possibility_to_reserve = models.BooleanField(default=True)
    user_number_in_line = models.IntegerField()

