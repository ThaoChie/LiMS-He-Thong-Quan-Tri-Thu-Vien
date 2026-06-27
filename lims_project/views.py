from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    from apps.catalog.models import Book
    from apps.circulation.models import BorrowRecord, Reservation

    total_books = Book.objects.count()
    available_books = Book.objects.filter(available_copies__gt=0).count()
    active_borrows = BorrowRecord.objects.filter(user=request.user, status='borrowed').count()
    active_reservations = Reservation.objects.filter(user=request.user, status='active').count()
    recent_books = Book.objects.all().order_by('-created_at')[:8]

    return render(request, 'home.html', {
        'total_books': total_books,
        'available_books': available_books,
        'active_borrows': active_borrows,
        'active_reservations': active_reservations,
        'recent_books': recent_books,
    })
