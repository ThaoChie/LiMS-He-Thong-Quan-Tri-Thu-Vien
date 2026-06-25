from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Author, Publisher, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'isbn',
        'category',
        'status',
        'available_copies',
        'total_copies',
        'pdf_status',
        'created_at',
    )
    list_filter = ('status', 'category')
    search_fields = ('title', 'isbn')
    filter_horizontal = ('authors',)
    readonly_fields = ('pdf_preview',)

    @admin.display(description='PDF')
    def pdf_status(self, obj):
        if not obj.pdf_file:
            return '-'
        return format_html('<a href="{}" target="_blank">Xem PDF</a>', obj.pdf_file.url)

    @admin.display(description='File PDF hi?n t?i')
    def pdf_preview(self, obj):
        if not obj or not obj.pdf_file:
            return 'Ch?a c? PDF'
        return format_html('<a href="{}" target="_blank">{}</a>', obj.pdf_file.url, obj.pdf_file.name)
