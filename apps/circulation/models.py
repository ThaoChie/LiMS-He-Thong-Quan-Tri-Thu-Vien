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
        ('lost', 'Báo mất'),
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
    renewal_count = models.PositiveIntegerField(default=0, verbose_name='Số lần gia hạn')
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

    @property
    def days_until_due(self):
        from django.utils import timezone
        if self.status == 'borrowed' and self.due_date:
            return (self.due_date.date() - timezone.now().date()).days
        return 0

    @property
    def has_violation(self):
        return self.status in ['overdue', 'lost']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user_id:
            has_violations = BorrowRecord.objects.filter(
                user_id=self.user_id,
                status__in=['overdue', 'lost']
            ).exists()
            self.user.can_borrow = not has_violations
            self.user.save(update_fields=['can_borrow'])


class Reservation(models.Model):
    """Đặt trước sách."""
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Notified', 'Notified'),
        ('Completed', 'Completed'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
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
        default='Waiting',
        verbose_name='Trạng thái',
    )
    queue_position = models.PositiveIntegerField(null=True)
    notified_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Đặt trước'
        verbose_name_plural = 'Đặt trước'
        ordering = ['-reserved_at']

    def __str__(self):
        return f"{self.user.username} đặt {self.book.title}"
