from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    """Phiên hội thoại với chatbot RAG."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_sessions',
        verbose_name='Người dùng',
    )
    title = models.CharField(
        max_length=255,
        default='Cuộc trò chuyện mới',
        verbose_name='Tiêu đề',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Phiên chat'
        verbose_name_plural = 'Phiên chat'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ChatMessage(models.Model):
    """Tin nhắn trong phiên hội thoại."""
    ROLE_CHOICES = [
        ('user', 'Người dùng'),
        ('assistant', 'Trợ lý AI'),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Phiên chat',
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name='Vai trò',
    )
    content = models.TextField(verbose_name='Nội dung')
    sources = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Nguồn tham khảo (RAG)',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian')

    class Meta:
        verbose_name = 'Tin nhắn'
        verbose_name_plural = 'Tin nhắn'
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.get_role_display()}] {self.content[:50]}..."


class DocumentIndex(models.Model):
    """Theo dõi các tài liệu PDF đã được index vào ChromaDB."""
    book = models.OneToOneField(
        'catalog.Book',
        on_delete=models.CASCADE,
        related_name='document_index',
        verbose_name='Sách',
    )
    collection_name = models.CharField(
        max_length=255,
        verbose_name='Tên Collection trong ChromaDB',
    )
    chunk_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Số chunks đã index',
    )
    indexed_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày index')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        verbose_name = 'Tài liệu đã Index'
        verbose_name_plural = 'Tài liệu đã Index'

    def __str__(self):
        return f"{self.book.title} - {self.chunk_count} chunks"
