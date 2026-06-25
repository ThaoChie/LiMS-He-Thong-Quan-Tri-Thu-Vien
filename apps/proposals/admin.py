from django.contrib import admin
from .models import BookProposal


@admin.register(BookProposal)
class BookProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'user__username')
    raw_id_fields = ('user', 'reviewed_by')
