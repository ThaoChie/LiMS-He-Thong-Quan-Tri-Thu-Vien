from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import BorrowRecord, Reservation
from apps.catalog.models import Book


@login_required
def borrow_request_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        if not book.is_available:
            messages.error(request, 'Sách hiện không có sẵn.')
            return redirect('catalog:book_detail', pk=book.pk)
        # Check if user already has pending/active borrow
        existing = BorrowRecord.objects.filter(user=request.user, book=book, status__in=['pending', 'borrowed']).exists()
        if existing:
            messages.warning(request, 'Bạn đã có yêu cầu mượn hoặc đang mượn sách này.')
            return redirect('catalog:book_detail', pk=book.pk)
        BorrowRecord.objects.create(
            user=request.user, book=book, due_date=timezone.now() + timedelta(days=14),
            notes=request.POST.get('notes', ''), status='pending',
        )
        messages.success(request, 'Yêu cầu mượn sách đã được gửi! Chờ thủ thư duyệt.')
        return redirect('circulation:borrow_history')
    return render(request, 'circulation/borrow_request.html', {'book': book})


@login_required
def borrow_history_view(request):
    status_filter = request.GET.get('status', '')
    records = BorrowRecord.objects.filter(user=request.user).select_related('book')
    if status_filter:
        records = records.filter(status=status_filter)
    paginator = Paginator(records.order_by('-created_at'), 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'circulation/borrow_history.html', {'page_obj': page, 'status_filter': status_filter})


@login_required
def borrow_cancel_view(request, pk):
    if request.method == 'POST':
        record = get_object_or_404(BorrowRecord, pk=pk, user=request.user, status='pending')
        record.status = 'cancelled'
        record.save()
        messages.success(request, 'Đã hủy yêu cầu mượn sách.')
    return redirect('circulation:borrow_history')


@login_required
def manage_borrows_view(request):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('home')
    status_filter = request.GET.get('status', '')
    records = BorrowRecord.objects.all().select_related('user', 'book')
    if status_filter:
        records = records.filter(status=status_filter)
    paginator = Paginator(records.order_by('-created_at'), 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'circulation/manage_borrows.html', {'page_obj': page, 'status_filter': status_filter})


@login_required
def approve_borrow_view(request, pk):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Không có quyền.')
        return redirect('home')
    record = get_object_or_404(BorrowRecord, pk=pk, status='pending')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            due_days = int(request.POST.get('due_days', 14))
            record.status = 'borrowed'
            record.due_date = timezone.now() + timedelta(days=due_days)
            record.approved_by = request.user
            record.notes = request.POST.get('notes', record.notes)
            record.save()
            book = record.book
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save()
            messages.success(request, f'Đã duyệt mượn sách "{record.book.title}".')
        else:
            record.status = 'cancelled'
            record.notes = request.POST.get('notes', record.notes)
            record.save()
            messages.info(request, f'Đã từ chối yêu cầu mượn sách "{record.book.title}".')
    return redirect('circulation:manage_borrows')


@login_required
def return_book_view(request, pk):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Không có quyền.')
        return redirect('home')
    record = get_object_or_404(BorrowRecord, pk=pk, status='borrowed')
    if request.method == 'POST':
        record.status = 'returned'
        record.return_date = timezone.now()
        record.notes = request.POST.get('notes', record.notes)
        record.save()
        book = record.book
        book.available_copies += 1
        book.save()
        messages.success(request, f'Đã xử lý trả sách "{record.book.title}" thành công.')
    return redirect('circulation:manage_borrows')


@login_required
def reservation_create_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        existing = Reservation.objects.filter(user=request.user, book=book, status='active').exists()
        if existing:
            messages.warning(request, 'Bạn đã đặt trước sách này rồi.')
        else:
            Reservation.objects.create(
                user=request.user, book=book, expires_at=timezone.now() + timedelta(days=3),
            )
            messages.success(request, f'Đã đặt trước sách "{book.title}". Hạn: 3 ngày.')
        return redirect('catalog:book_detail', pk=book.pk)
    return render(request, 'circulation/reserve_confirm.html', {'book': book})


@login_required
def reservation_list_view(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('book').order_by('-reserved_at')
    return render(request, 'circulation/reservation_list.html', {'reservations': reservations})


@login_required
def reservation_cancel_view(request, pk):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user, status='active')
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Đã hủy đặt trước.')
    return redirect('circulation:reservation_list')
