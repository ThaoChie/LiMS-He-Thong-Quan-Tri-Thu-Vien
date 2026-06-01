from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser.
    Roles: 'reader' (Bạn đọc), 'librarian' (Thủ thư), 'admin' (Quản trị viên).
    """
    ROLE_CHOICES = [
        ('reader', 'Bạn đọc'),
        ('librarian', 'Thủ thư'),
        ('admin', 'Quản trị viên'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='reader',
        verbose_name='Vai trò',
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Số điện thoại',
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Địa chỉ',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Đang hoạt động',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_reader(self):
        return self.role == 'reader'

    @property
    def is_librarian(self):
        return self.role == 'librarian'

    @property
    def is_admin_user(self):
        return self.role == 'admin'
