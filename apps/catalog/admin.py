from django.contrib import admin
from .models import Category, Publisher, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)



@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'category', 'status', 'available_copies', 'total_copies', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'isbn')
