import uuid

from django.db import models
from django.db.models import UUIDField
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Введите жанр ( Научная Литература, Французская Поэзия и т.д)')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Введите описание книги')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13-ти значный <a href="https://ru.wikipedia.org/wiki/Международный_'
                                      'стандартный_номер_книги">ISBN номер</a>')
    genre = models.ManyToManyField(Genre, help_text='Введите жанр книги')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный идентификатор книги в данной библиотеке')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.id, self.book.title}"

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.pk)])

    def __str__(self):
        return f"{self.last_name, self.first_name}"

    class Meta:
        ordering = ['last_name']
