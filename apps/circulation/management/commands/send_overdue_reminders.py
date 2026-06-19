import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from apps.circulation.models import BorrowRecord

class Command(BaseCommand):
    help = 'Gửi email nhắc nhở cho các sinh viên mượn sách quá hạn'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        overdue_records = BorrowRecord.objects.filter(status='borrowed', due_date__lt=now)
        count = 0
        for record in overdue_records:
            days_late = (now - record.due_date).days
            subject = f'[Cảnh báo] Trễ hạn trả sách: {record.book.title}'
            msg = f'Xin chào {record.user.username},\n\nPhiếu mượn cuốn sách "{record.book.title}" của bạn đã quá hạn {days_late} ngày.\nVui lòng mang sách đến thư viện trả ngay để tránh bị phạt thêm và khóa tài khoản.\n\nTrân trọng!'
            try:
                send_mail(subject, msg, getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@lims.local'), [record.user.email])
                count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Lỗi gửi email cho {record.user.username}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Đã quét và gửi {count} email nhắc trả sách quá hạn.'))
