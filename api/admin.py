from django.contrib import admin

# Register your models here.
from .models import Book, Cart, User

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Cart)
