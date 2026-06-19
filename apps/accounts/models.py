from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser.
    Roles: 'reader' (Bạn đọc), 'librarian' (Thủ thư), 'admin' (Quản trị viên).
    """
    ROLE_CHOICES = [
        ('reader', 'Bạn đọc'),
        ('lecturer', 'Giảng viên'),
        ('librarian', 'Thủ thư'),
        ('admin', 'Quản trị viên'),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        error_messages={
            'unique': 'Địa chỉ email này đã tồn tại trong hệ thống.'
        }
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='reader',
        verbose_name='Vai trò',
    )
    phone_regex = RegexValidator(regex=r'^0[0-9]{9}$', message="Số điện thoại không hợp lệ. Phải bắt đầu bằng số 0 và có đúng 10 chữ số.")
    phone_number = models.CharField(
        validators=[phone_regex],
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
    can_borrow = models.BooleanField(
        default=True,
        verbose_name='Được phép mượn sách',
    )
    failed_login_attempts = models.IntegerField(
        default=0,
        verbose_name='Số lần đăng nhập sai',
    )
    locked_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Khóa tài khoản đến',
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
    def is_lecturer(self):
        return self.role == 'lecturer'

    @property
    def is_librarian(self):
        return self.role == 'librarian'

    @property
    def is_admin_user(self):
        return self.role == 'admin'
