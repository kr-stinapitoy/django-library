from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils import timezone
import datetime

from .models import Book, BookCheckout, BookComments
from user.models import CustomUser

from .forms import CreateBookForm, EditBookForm, AddComment
from user.forms import LoginForm

class BookView(TemplateView):

    def get(request, *args, **kwargs):

        book_page = get_object_or_404(Book, pk=kwargs.get('pk'))
        context = {
            'book_page': book_page,
        }
        if request.user.is_authenticated:
            return render(request, "book/book-page.html",  context)
        else:
            return render(request, "book/book-page.html",  context)

    def post(request, *args, **kwargs):

        CB_form = CreateBookForm(request.POST, request.FILES)
        if CB_form.is_valid():
            create_book = CB_form.save(commit=False)
            create_book.owner = request.user
            CB_form.save()
            return redirect('book:owned_books', request.user.id)
        else:
            return redirect('book:home')

    def update_book(request, *args, **kwargs):

        template_name = 'book/owned-books.html'
        if request.user.is_authenticated:
            book_data = get_object_or_404(Book, pk=kwargs.get('pk'))

            initial_data = {
                'title' : book_data.title,
                'author': book_data.author,
                'location': book_data.location,
                'book_image': book_data.book_image,
                'is_digital': book_data.is_digital,
            }

            UB_form = EditBookForm(request.POST, request.FILES, instance=book_data, initial=initial_data)
            context = {
                'book_data': book_data,
                'UB_form': UB_form,
                'pk': kwargs.get('pk'),
            }

            if UB_form.is_valid():
                update_book = UB_form.save(commit=False)
                update_book.save()
                return redirect('book:owned_books', request.user.id)
            else:
                UB_form = EditBookForm(request.POST, initial=initial_data)
                return render(request, template_name, context)
        else:
            redirect('user:login')

    def delete(request, *args, **kwargs):

        if request.user.is_authenticated:
            book = get_object_or_404(Book, pk=kwargs.get('pk'))
            if request.user == book.owner:
                book.delete()
                return redirect('book:owned_books', request.user.pk)
        else:
            return redirect('user:login')


class HomePageView(TemplateView):

    def get(self, request):
        CC_form = AddComment()
        books = Book.objects.all().order_by('-date_created')
        co_books = BookCheckout.objects.all()
        comments = BookComments.objects.all()

        context = {
                'CC_form': CC_form,
                'books':books,
                'comments': comments,
                'co_books': co_books,
            }
        if request.user.is_authenticated:
            return render(request,'book/home-page.html', context)
        else:
            form = LoginForm()
            return render(request, "user/login.html", {"form": form})


class BookCommentView(TemplateView):

    def post(request, *args, **kwargs):

        CC_form = AddComment(request.POST)
        if CC_form.is_valid():
            book_data = get_object_or_404(Book, pk=kwargs.get('pk'))
            create_comment = CC_form.save(commit=False)
            create_comment.user = request.user
            create_comment.book = book_data
            create_comment.save()
            return redirect('book:home')
        else:
            return redirect('book:home')


class BookCheckoutViews(TemplateView):

    def post(request, *args, **kwargs):

        book_data = Book.objects.get(pk=kwargs.get('pk'))
        book_data.status = 'checkedout'
        checkout = BookCheckout.objects.create(book=book_data, borrower=request.user)
        book_data.save()
        messages.success(request, 'Check your borrowed books')
        return redirect('book:home')


class ReturnBookView(TemplateView):

    def post(request, *args, **kwargs):

        book_data = Book.objects.get(pk=kwargs.get('pk'))
        book_data.status = 'available'
        checkout = BookCheckout.objects.get(book=book_data, borrower=request.user, is_returned='False')
        checkout.return_date = datetime.datetime.now(tz=timezone.utc)
        checkout.is_returned = 'True'
        book_data.save()
        checkout.save()
        return redirect('book:borrowed_books', request.user.id)


class SearchBookView(TemplateView):

    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            query = request.POST.get('bookSearch')
            books = Book.objects.filter(title__icontains=query).order_by('-date_created')
            return render(request, 'book/home-page.html', {'books': books})
        else:
            return redirect('user:login')


class FilterBookView(TemplateView):

    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            query = request.POST.get('book_filter')

            if query == 'True':
                books = Book.objects.filter(is_digital=query).order_by('-date_created')
            else:
                books = Book.objects.filter(status=query).order_by('-date_created')
            return render(request, 'book/home-page.html', {'books': books})
        else:
            return redirect('user:login')


class OwnedBooksView(TemplateView):

    template_name = 'book/owned-books.html'

    def get_context_data(self, *args, **kwargs):

        owned_books = Book.objects.filter(owner=self.request.user).order_by('-date_created')
        # context = super(OwnedBooksView,self).get_context_data(*args, **kwargs)
        CB_form = CreateBookForm()
        UB_form = EditBookForm()

        context = {
            'owned_books': owned_books,
            'UB_form': UB_form,
            'CB_form': CB_form,
        }

        return context


class BorrowedBooksView(TemplateView):

    template_name = 'book/borrowed-books.html'

    def get_context_data(self, *args, **kwargs):

        borrowed_books = BookCheckout.objects.filter(borrower=self.request.user).order_by('-checkedout_date')
        context = super(BorrowedBooksView,self).get_context_data(*args, **kwargs)
        UB_form = EditBookForm()
        page_user = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        context = {
            'borrowed_books': borrowed_books,
            'page_user': page_user,
            'UB_form': UB_form,
        }

        return context
