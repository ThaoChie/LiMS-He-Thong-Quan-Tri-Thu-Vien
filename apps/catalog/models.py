from django.db import models


class Category(models.Model):
    """Danh mục / Thể loại sách."""
    name = models.CharField(max_length=200, unique=True, verbose_name='Tên thể loại')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        verbose_name = 'Thể loại'
        verbose_name_plural = 'Thể loại'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    """Tác giả."""
    name = models.CharField(max_length=255, verbose_name='Tên tác giả')
    biography = models.TextField(blank=True, null=True, verbose_name='Tiểu sử')

    class Meta:
        verbose_name = 'Tác giả'
        verbose_name_plural = 'Tác giả'
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Nhà xuất bản."""
    name = models.CharField(max_length=255, unique=True, verbose_name='Tên NXB')
    address = models.TextField(blank=True, null=True, verbose_name='Địa chỉ')

    class Meta:
        verbose_name = 'Nhà xuất bản'
        verbose_name_plural = 'Nhà xuất bản'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Đầu sách (Book Title) in the library."""
    STATUS_CHOICES = [
        ('available', 'Có sẵn'),
        ('borrowed', 'Đang mượn'),
        ('reserved', 'Đã đặt trước'),
        ('maintenance', 'Bảo trì'),
    ]

    title = models.CharField(max_length=500, verbose_name='Tên sách')
    isbn = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Mã ISBN',
    )
    authors = models.ManyToManyField(
        Author,
        related_name='books',
        verbose_name='Tác giả',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Thể loại',
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Nhà xuất bản',
    )
    publication_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Năm xuất bản',
    )
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    cover_image = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        verbose_name='Ảnh bìa',
    )
    pdf_file = models.FileField(
        upload_to='books_pdf/',
        blank=True,
        null=True,
        verbose_name='File PDF',
    )
    total_copies = models.PositiveIntegerField(default=1, verbose_name='Tổng số bản')
    available_copies = models.PositiveIntegerField(default=1, verbose_name='Số bản có sẵn')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Trạng thái',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        verbose_name = 'Sách'
        verbose_name_plural = 'Sách'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.available_copies > 0
