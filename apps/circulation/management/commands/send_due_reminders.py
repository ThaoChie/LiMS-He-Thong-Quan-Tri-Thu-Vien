import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from apps.circulation.models import BorrowRecord
from datetime import timedelta

class Command(BaseCommand):
    help = 'Gửi email nhắc nhở sắp đến hạn trả sách (trước 2 ngày)'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        target_date = (now + timedelta(days=2)).date()
        
        records = BorrowRecord.objects.filter(status='borrowed')
        count = 0
        for record in records:
            if record.due_date.date() == target_date:
                subject = f'[Nhắc nhở] Sắp đến hạn trả sách: {record.book.title}'
                msg = (
                    f'Xin chào {record.user.username},\n\n'
                    f'Cuốn sách "{record.book.title}" bạn đang mượn sắp đến hạn trả vào ngày {timezone.localtime(record.due_date).strftime("%d/%m/%Y")}.\n'
                    f'Nếu bạn chưa đọc xong, bạn có thể đăng nhập vào hệ thống để gia hạn thêm tối đa 10 ngày (Lưu ý: chỉ gia hạn được nếu sách chưa có ai xếp hàng chờ mượn).\n'
                    f'Vui lòng lưu ý trả sách đúng hạn để không bị phạt vi phạm.\n\n'
                    f'Trân trọng!'
                )
                try:
                    send_mail(subject, msg, getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@lims.local'), [record.user.email])
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Lỗi gửi email cho {record.user.username}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Đã quét và gửi {count} email nhắc sắp đến hạn.'))
