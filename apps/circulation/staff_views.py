from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Reservation

@login_required
def manage_reservations_view(request):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('home')
        
    status_filter = request.GET.get('status', '')
    reservations = Reservation.objects.all().select_related('user', 'book').order_by('queue_position', '-reserved_at')
    
    if status_filter:
        reservations = reservations.filter(status=status_filter)
        
    paginator = Paginator(reservations, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'circulation/manage_reservations.html', {'page_obj': page, 'status_filter': status_filter})

@login_required
def cancel_reservation_view(request, pk):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Không có quyền.')
        return redirect('home')
        
    reservation = get_object_or_404(Reservation, pk=pk)
    
    if request.method == 'POST':
        if reservation.status in ['Waiting', 'Notified']:
            reservation.status = 'Cancelled'
            reservation.save()
            messages.success(request, f'Đã hủy đặt trước của {reservation.user.username}.')
        else:
            messages.warning(request, 'Không thể hủy vì đặt trước không ở trạng thái Waiting hoặc Notified.')
            
    return redirect('circulation:manage_reservations')
