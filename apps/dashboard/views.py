from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.catalog.models import Book
from apps.accounts.models import CustomUser
from apps.circulation.models import BorrowRecord, Reservation
from apps.proposals.models import BookProposal

@login_required
def admin_dashboard_view(request):
    total_books = Book.objects.count()
    total_users = CustomUser.objects.count()
    total_borrowed = BorrowRecord.objects.filter(status='borrowed').count()
    total_overdue = BorrowRecord.objects.filter(status='overdue').count()
    
    # Chỉ số cảnh báo tín nhiệm
    total_violations = BorrowRecord.objects.filter(status__in=['overdue', 'lost']).count()
    locked_users = CustomUser.objects.filter(can_borrow=False).count()
    
    # Tỷ lệ duyệt mua sách theo ISBN
    total_proposals = BookProposal.objects.count()
    approved_proposals = BookProposal.objects.filter(status__in=['approved', 'purchased']).count()
    proposal_approval_rate = round((approved_proposals / total_proposals * 100), 1) if total_proposals > 0 else 0

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_borrowed': total_borrowed,
        'total_overdue': total_overdue,
        'total_violations': total_violations,
        'locked_users': locked_users,
        'total_proposals': total_proposals,
        'approved_proposals': approved_proposals,
        'proposal_approval_rate': proposal_approval_rate,
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
    
    # Vi phạm tín nhiệm (Overdue / Lost)
    violations = BorrowRecord.objects.filter(user=user, status__in=['overdue', 'lost'])

    context = {
        'borrowed_records': borrowed_records,
        'returned_records': returned_records,
        'reservations': reservations,
        'violations': violations,
    }
    return render(request, 'dashboard/user_history.html', context)
