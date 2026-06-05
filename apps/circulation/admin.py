from django.contrib import admin
from .models import BorrowRecord, Reservation


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    raw_id_fields = ('user', 'book', 'approved_by')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'reserved_at', 'expires_at', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    raw_id_fields = ('user', 'book')
