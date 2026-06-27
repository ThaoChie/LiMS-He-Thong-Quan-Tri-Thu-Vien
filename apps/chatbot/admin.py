from django.contrib import admin
from .models import ChatSession, ChatMessage, DocumentIndex


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    search_fields = ('user__username', 'title')
    raw_id_fields = ('user',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'created_at')
    list_filter = ('role',)
    raw_id_fields = ('session',)


@admin.register(DocumentIndex)
class DocumentIndexAdmin(admin.ModelAdmin):
    list_display = ('book', 'collection_name', 'chunk_count', 'indexed_at')
    raw_id_fields = ('book',)
