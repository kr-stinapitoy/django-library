from django.contrib import admin
from .models import Book, BookComments, BookCheckout
# Register your models here.

admin.site.register(Book)
admin.site.register(BookComments)
admin.site.register(BookCheckout)