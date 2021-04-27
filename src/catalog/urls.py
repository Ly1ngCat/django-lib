from django.urls import path
from .views import index, BookListView, BookDetailView, AuthorListView, AuthorDetailView

from django.conf.urls import url

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^books/$', BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book-detail'),
    url(r'^authors/$', AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author-detail'),
]