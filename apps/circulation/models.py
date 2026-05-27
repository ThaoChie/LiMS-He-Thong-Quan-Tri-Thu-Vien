from django.db import models
from django.conf import settings
from django.utils import timezone


class BorrowRecord(models.Model):
    """Phiếu mượn sách."""
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('approved', 'Đã duyệt'),
        ('borrowed', 'Đang mượn'),
        ('returned', 'Đã trả'),
        ('overdue', 'Quá hạn'),
        ('cancelled', 'Đã hủy'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrow_records',
        verbose_name='Người mượn',
    )
    book = models.ForeignKey(
        'catalog.Book',
        on_delete=models.CASCADE,
        related_name='borrow_records',
        verbose_name='Sách',
    )
    borrow_date = models.DateTimeField(default=timezone.now, verbose_name='Ngày mượn')
    due_date = models.DateTimeField(verbose_name='Ngày hẹn trả')
    return_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Ngày trả thực tế',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Trạng thái',
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_borrows',
        verbose_name='Người duyệt',
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        verbose_name = 'Phiếu mượn'
        verbose_name_plural = 'Phiếu mượn'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.status == 'borrowed' and self.due_date < timezone.now():
            return True
        return False


class Reservation(models.Model):
    """Đặt trước sách."""
    STATUS_CHOICES = [
        ('active', 'Đang đặt'),
        ('fulfilled', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
        ('expired', 'Đã hết hạn'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Người đặt',
    )
    book = models.ForeignKey(
        'catalog.Book',
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Sách',
    )
    reserved_at = models.DateTimeField(default=timezone.now, verbose_name='Ngày đặt')
    expires_at = models.DateTimeField(verbose_name='Ngày hết hạn')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Trạng thái',
    )

    class Meta:
        verbose_name = 'Đặt trước'
        verbose_name_plural = 'Đặt trước'
        ordering = ['-reserved_at']

    def __str__(self):
        return f"{self.user.username} đặt {self.book.title}"
