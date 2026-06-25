from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.catalog.models import Book
from apps.accounts.models import CustomUser
from apps.circulation.models import BorrowRecord, Reservation, FineReceipt

@login_required
def admin_dashboard_view(request):
    total_books = Book.objects.count()
    total_users = CustomUser.objects.count()
    total_borrowed = BorrowRecord.objects.filter(status='borrowed').count()
    total_overdue = BorrowRecord.objects.filter(status='overdue').count()

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_borrowed': total_borrowed,
        'total_overdue': total_overdue,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def user_history_view(request):
    user = request.user
    
    # Sách đang mượn (BorrowRecord borrowed/overdue)
    borrowed_records = BorrowRecord.objects.filter(
        user=user, 
        status__in=['borrowed', 'overdue']
    )
    
    # Lịch sử trả (returned)
    returned_records = BorrowRecord.objects.filter(
        user=user, 
        status='returned'
    )
    
    # Đặt trước (Reservation)
    reservations = Reservation.objects.filter(user=user)
    
    # Phiếu phạt (FineReceipt)
    fines = FineReceipt.objects.filter(borrow_record__user=user)

    context = {
        'borrowed_records': borrowed_records,
        'returned_records': returned_records,
        'reservations': reservations,
        'fines': fines,
    }
    return render(request, 'dashboard/user_history.html', context)
