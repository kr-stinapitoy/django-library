from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('home/', views.HomePageView.as_view(), name='home'),
    path('create-book/', views.BookView.post, name='create_book'),
    path('<int:pk>/book-page', views.BookView.get, name='book_page'),
    path('<int:pk>/book-page/add-comment', views.BookCommentView.post, name='add_comment'),
    # path('<int:pk>/postpage/deletecomment', views.CommentView.delete, name='deletecomment'),
    path('<int:pk>/edit-book', views.BookView.update_book, name='edit_book'),
    path('<int:pk>/book-page/delete-book', views.BookView.delete, name='delete_book'),
    path('<int:pk>/book-page/checkout', views.BookCheckoutViews.post, name='checkout'),
    path('<int:pk>/book-page/return-book', views.ReturnBookView.post, name='return_book'),
    path('<int:pk>/owned-books', views.OwnedBooksView.as_view(), name='owned_books'),
    path('<int:pk>/borrowed-books', views.BorrowedBooksView.as_view(), name='borrowed_books'),
    path('search/', views.SearchBookView.post, name='search'),
    path('filter/', views.FilterBookView.post, name='filter'),
]