"""
Management command: seed_data
Tạo bộ dữ liệu mẫu đầy đủ cho hệ thống LiMS để kiểm thử các chức năng.
Bao gồm: Category, Author, Publisher, Book, BorrowRecord, Reservation, BookProposal, Review
"""
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from apps.accounts.models import CustomUser
from apps.catalog.models import Category, Publisher, Book
from apps.circulation.models import BorrowRecord, Reservation, FineReceipt
from apps.proposals.models import BookProposal
from apps.reviews.models import Review


# ─── RAW DATA ────────────────────────────────────────────────────────────────

CATEGORIES = [
    {"name": "Công nghệ Thông tin", "description": "Sách về lập trình, phần mềm, trí tuệ nhân tạo, mạng máy tính"},
    {"name": "Kinh tế & Quản trị", "description": "Sách về kinh tế học, quản trị kinh doanh, tài chính, marketing"},
    {"name": "Văn học Việt Nam", "description": "Tác phẩm văn học của các tác giả Việt Nam qua các thời đại"},
    {"name": "Văn học Nước ngoài", "description": "Các tác phẩm văn học nổi tiếng thế giới được dịch sang tiếng Việt"},
    {"name": "Khoa học Tự nhiên", "description": "Vật lý, Hóa học, Sinh học, Toán học, Thiên văn học"},
    {"name": "Lịch sử & Địa lý", "description": "Lịch sử Việt Nam, lịch sử thế giới, địa lý học"},
    {"name": "Tâm lý học", "description": "Tâm lý học đại cương, tâm lý ứng dụng, kỹ năng sống"},
    {"name": "Ngoại ngữ", "description": "Giáo trình và sách học tiếng Anh, Nhật, Trung, Hàn..."},
]

AUTHORS = [
    {"name": "Nguyễn Nhật Ánh", "biography": "Nhà văn Việt Nam nổi tiếng với các tác phẩm dành cho thiếu nhi và tuổi mới lớn."},
    {"name": "Nam Cao", "biography": "Nhà văn hiện thực xuất sắc của văn học Việt Nam hiện đại."},
    {"name": "Tô Hoài", "biography": "Nhà văn Việt Nam, tác giả của 'Dế Mèn phiêu lưu ký'."},
    {"name": "Robert C. Martin", "biography": "Kỹ sư phần mềm và tác giả nổi tiếng với các cuốn sách về Clean Code."},
    {"name": "Andrew Ng", "biography": "Nhà khoa học AI nổi tiếng, giáo sư Stanford, người sáng lập Coursera."},
    {"name": "Daniel Kahneman", "biography": "Nhà tâm lý học người Israel-Mỹ, đoạt giải Nobel Kinh tế 2002."},
    {"name": "Dale Carnegie", "biography": "Nhà văn người Mỹ nổi tiếng với các tác phẩm về kỹ năng mềm và phát triển bản thân."},
    {"name": "Yuval Noah Harari", "biography": "Nhà sử học, triết học người Israel, tác giả của Sapiens, Homo Deus."},
    {"name": "Mark Lutz", "biography": "Chuyên gia lập trình Python, tác giả của nhiều cuốn sách về Python."},
    {"name": "Thomas H. Cormen", "biography": "Giáo sư khoa học máy tính tại Đại học Dartmouth, đồng tác giả CLRS."},
    {"name": "Ngô Bảo Châu", "biography": "Nhà toán học Việt Nam, giải thưởng Fields Medal 2010."},
    {"name": "Hồ Anh Thái", "biography": "Nhà văn Việt Nam đương đại, tác giả nhiều tiểu thuyết nổi tiếng."},
]

PUBLISHERS = [
    {"name": "NXB Giáo dục Việt Nam", "address": "81 Trần Hưng Đạo, Hoàn Kiếm, Hà Nội"},
    {"name": "NXB Trẻ", "address": "161B Lý Chính Thắng, Q.3, TP. Hồ Chí Minh"},
    {"name": "NXB Kim Đồng", "address": "55 Quang Trung, Hai Bà Trưng, Hà Nội"},
    {"name": "NXB Tổng hợp TP.HCM", "address": "62 Nguyễn Thị Minh Khai, Q.1, TP. Hồ Chí Minh"},
    {"name": "NXB Thông tin và Truyền thông", "address": "115 Trần Duy Hưng, Cầu Giấy, Hà Nội"},
    {"name": "O'Reilly Media", "address": "1005 Gravenstein Highway North, Sebastopol, CA 95472, USA"},
    {"name": "Addison-Wesley", "address": "501 Boylston Street, Boston, MA 02116, USA"},
]

BOOKS = [
    # CNTT
    {
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "isbn": "9780132350884",
        "author_names": ["Robert C. Martin"],
        "category": "Công nghệ Thông tin",
        "publisher": "Addison-Wesley",
        "year": 2008,
        "copies": 5,
        "description": "Cuốn sách kinh điển về viết code sạch, dễ đọc và dễ bảo trì. Bắt buộc phải đọc với mọi lập trình viên chuyên nghiệp.",
    },
    {
        "title": "Lập trình Python từ cơ bản đến nâng cao",
        "isbn": "9780596158064",
        "author_names": ["Mark Lutz"],
        "category": "Công nghệ Thông tin",
        "publisher": "O'Reilly Media",
        "year": 2013,
        "copies": 8,
        "description": "Hướng dẫn toàn diện về ngôn ngữ lập trình Python, từ kiến thức cơ bản đến các kỹ thuật nâng cao.",
    },
    {
        "title": "Introduction to Algorithms (CLRS)",
        "isbn": "9780262033848",
        "author_names": ["Thomas H. Cormen"],
        "category": "Công nghệ Thông tin",
        "publisher": "Addison-Wesley",
        "year": 2022,
        "copies": 4,
        "description": "Giáo trình thuật toán và cấu trúc dữ liệu tiêu chuẩn được sử dụng tại các trường đại học hàng đầu thế giới.",
    },
    {
        "title": "Machine Learning Yearning",
        "isbn": "9780999579503",
        "author_names": ["Andrew Ng"],
        "category": "Công nghệ Thông tin",
        "publisher": "O'Reilly Media",
        "year": 2018,
        "copies": 6,
        "description": "Hướng dẫn thực tế về xây dựng và tối ưu hóa các hệ thống machine learning.",
    },
    # Kinh tế
    {
        "title": "Tư duy nhanh và chậm",
        "isbn": "9780374533557",
        "author_names": ["Daniel Kahneman"],
        "category": "Kinh tế & Quản trị",
        "publisher": "NXB Thông tin và Truyền thông",
        "year": 2011,
        "copies": 7,
        "description": "Khám phá hai hệ thống tư duy chi phối cách chúng ta đưa ra quyết định, bản dịch tiếng Việt chính thức.",
    },
    {
        "title": "Đắc Nhân Tâm",
        "isbn": "9780671027032",
        "author_names": ["Dale Carnegie"],
        "category": "Kinh tế & Quản trị",
        "publisher": "NXB Tổng hợp TP.HCM",
        "year": 1936,
        "copies": 10,
        "description": "Cuốn sách kỹ năng giao tiếp và tạo ảnh hưởng với người khác, bestseller mọi thời đại.",
    },
    # Văn học Việt Nam
    {
        "title": "Cho tôi xin một vé đi tuổi thơ",
        "isbn": "9786041162044",
        "author_names": ["Nguyễn Nhật Ánh"],
        "category": "Văn học Việt Nam",
        "publisher": "NXB Trẻ",
        "year": 2008,
        "copies": 6,
        "description": "Cuốn tiểu thuyết đưa người đọc trở về những kỷ niệm trong sáng, hồn nhiên của tuổi thơ.",
    },
    {
        "title": "Chí Phèo",
        "isbn": "9786046871057",
        "author_names": ["Nam Cao"],
        "category": "Văn học Việt Nam",
        "publisher": "NXB Kim Đồng",
        "year": 1941,
        "copies": 9,
        "description": "Truyện ngắn nổi tiếng nhất của Nam Cao, phản ánh hiện thực xã hội Việt Nam trước cách mạng.",
    },
    {
        "title": "Dế Mèn phiêu lưu ký",
        "isbn": "9786041198562",
        "author_names": ["Tô Hoài"],
        "category": "Văn học Việt Nam",
        "publisher": "NXB Kim Đồng",
        "year": 1941,
        "copies": 12,
        "description": "Tác phẩm văn học thiếu nhi kinh điển của Việt Nam, kể về cuộc phiêu lưu của chú dế Mèn.",
    },
    {
        "title": "Mắt biếc",
        "isbn": "9786041162006",
        "author_names": ["Nguyễn Nhật Ánh"],
        "category": "Văn học Việt Nam",
        "publisher": "NXB Trẻ",
        "year": 1990,
        "copies": 5,
        "description": "Câu chuyện tình yêu đẹp và buồn của tuổi học trò, đã được chuyển thể thành phim điện ảnh.",
    },
    # Văn học Nước ngoài
    {
        "title": "Sapiens: Lược sử loài người",
        "isbn": "9780062316097",
        "author_names": ["Yuval Noah Harari"],
        "category": "Văn học Nước ngoài",
        "publisher": "NXB Thông tin và Truyền thông",
        "year": 2014,
        "copies": 8,
        "description": "Khám phá lịch sử nhân loại từ thời kỳ đồ đá đến thế kỷ 21, bán chạy nhất thế giới.",
    },
    # Khoa học
    {
        "title": "Toán học và cuộc sống",
        "isbn": "9786046871032",
        "author_names": ["Ngô Bảo Châu"],
        "category": "Khoa học Tự nhiên",
        "publisher": "NXB Giáo dục Việt Nam",
        "year": 2015,
        "copies": 4,
        "description": "Giáo sư Ngô Bảo Châu chia sẻ những câu chuyện thú vị về toán học và ứng dụng trong cuộc sống.",
    },
    # Tâm lý học
    {
        "title": "Tâm lý học đám đông",
        "isbn": "9786041162007",
        "author_names": ["Daniel Kahneman"],
        "category": "Tâm lý học",
        "publisher": "NXB Tổng hợp TP.HCM",
        "year": 2019,
        "copies": 5,
        "description": "Phân tích tâm lý học của các nhóm người và hiện tượng xã hội từ góc nhìn khoa học.",
    },
    # Lịch sử
    {
        "title": "Homo Deus: Lược sử tương lai",
        "isbn": "9780062464316",
        "author_names": ["Yuval Noah Harari"],
        "category": "Lịch sử & Địa lý",
        "publisher": "NXB Thông tin và Truyền thông",
        "year": 2016,
        "copies": 6,
        "description": "Khám phá tương lai của nhân loại trong thế kỷ 21, từ bất tử đến hạnh phúc nhân tạo.",
    },
    {
        "title": "Lịch sử Việt Nam bằng tranh",
        "isbn": "9786041062017",
        "author_names": ["Tô Hoài"],
        "category": "Lịch sử & Địa lý",
        "publisher": "NXB Trẻ",
        "year": 2020,
        "copies": 7,
        "description": "Bộ sách tranh kể về lịch sử Việt Nam từ thời Hùng Vương đến hiện đại, phù hợp mọi lứa tuổi.",
    },
]

PROPOSALS = [
    {
        "username": "sv_an",
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author_name": "Gang of Four (GoF)",
        "isbn": "9780201633610",
        "reason": "Cuốn sách này rất quan trọng cho môn học Thiết kế phần mềm. Sinh viên CNTT năm 3-4 rất cần tài liệu này để học Design Patterns.",
        "status": "pending",
    },
    {
        "username": "sv_binh",
        "title": "The Pragmatic Programmer",
        "author_name": "David Thomas, Andrew Hunt",
        "isbn": "9780135957059",
        "reason": "Sách hướng dẫn thực tiễn cho lập trình viên chuyên nghiệp. Phù hợp với định hướng đào tạo kỹ sư phần mềm của trường.",
        "status": "approved",
    },
    {
        "username": "sv_cuong",
        "title": "Atomic Habits",
        "author_name": "James Clear",
        "isbn": "9780735211292",
        "reason": "Sách về xây dựng thói quen tốt, rất phù hợp cho sinh viên trong việc quản lý thời gian và học tập hiệu quả.",
        "status": "rejected",
    },
    {
        "username": "sv_dung",
        "title": "Docker và Kubernetes cho Devops",
        "author_name": "Nguyen Van A",
        "isbn": "",
        "reason": "Trường đang đẩy mạnh môn học Cloud Computing nhưng chưa có sách tiếng Việt về Docker/Kubernetes trong thư viện.",
        "status": "pending",
    },
]

REVIEW_COMMENTS = [
    "Sách rất hay, nội dung dễ hiểu và có nhiều ví dụ thực tế. Rất khuyến khích đọc!",
    "Một cuốn sách tuyệt vời, thay đổi cách mình nhìn nhận vấn đề. Đã đọc đi đọc lại nhiều lần.",
    "Nội dung khá sâu sắc, cần đọc kỹ mới hiểu hết. Phù hợp cho người đã có kiến thức nền.",
    "Bản dịch tiếng Việt khá tốt, dễ đọc. Nội dung chất lượng và thiết thực.",
    "Sách cũ nhưng kiến thức vẫn còn nguyên giá trị đến ngày nay.",
    "Rất phù hợp với chương trình học. Thầy giáo cũng hay nhắc đến cuốn này.",
    "Đọc xong mở ra nhiều góc nhìn mới. Recommend cho tất cả các bạn sinh viên!",
    "Hơi khó đọc ở đầu nhưng càng về sau càng cuốn. Xứng đáng 5 sao.",
]


class Command(BaseCommand):
    help = "Tạo bộ dữ liệu mẫu đầy đủ cho hệ thống LiMS"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Xóa dữ liệu cũ trước khi seed (chỉ xóa data, không xóa user)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("🗑  Đang xóa dữ liệu cũ..."))
            Review.objects.all().delete()
            BookProposal.objects.all().delete()
            FineReceipt.objects.all().delete()
            Reservation.objects.all().delete()
            BorrowRecord.objects.all().delete()
            Book.objects.all().delete()
            Publisher.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("   Đã xóa xong.\n"))

        self.stdout.write(self.style.SUCCESS("🚀 Bắt đầu tạo dữ liệu mẫu...\n"))

        # 1. Categories
        self.stdout.write("📂 Tạo thể loại sách...")
        cat_map = {}
        for data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=data["name"], defaults={"description": data["description"]}
            )
            cat_map[data["name"]] = cat
            if created:
                self.stdout.write(f"   ✓ {cat.name}")
        self.stdout.write(self.style.SUCCESS(f"   → {len(cat_map)} thể loại\n"))

        # 2. Publishers
        self.stdout.write("🏢 Tạo nhà xuất bản...")
        pub_map = {}
        for data in PUBLISHERS:
            pub, created = Publisher.objects.get_or_create(
                name=data["name"], defaults={"address": data["address"]}
            )
            pub_map[data["name"]] = pub
            if created:
                self.stdout.write(f"   ✓ {pub.name}")
        self.stdout.write(self.style.SUCCESS(f"   → {len(pub_map)} NXB\n"))

        # 4. Books
        self.stdout.write("📚 Tạo sách...")
        book_map = {}
        for data in BOOKS:
            defaults = {
                "category": cat_map.get(data["category"]),
                "publisher": pub_map.get(data["publisher"]),
                "publication_year": data["year"],
                "description": data["description"],
                "total_copies": data["copies"],
                "available_copies": data["copies"],
                "status": "available",
                "authors": ", ".join(data["author_names"]),
            }
            book, created = Book.objects.get_or_create(
                title=data["title"], defaults={**defaults, "isbn": data.get("isbn")}
            )
            if created:
                self.stdout.write(f"   ✓ {book.title[:60]}")
            book_map[data["title"]] = book
        self.stdout.write(self.style.SUCCESS(f"   → {len(book_map)} cuốn sách\n"))

        # 5. Borrow Records & Reservations
        self.stdout.write("🔄 Tạo phiếu mượn sách...")
        readers = list(CustomUser.objects.filter(role="reader"))
        librarian = CustomUser.objects.filter(role__in=["librarian", "admin"]).first()
        books = list(Book.objects.all())

        if readers and librarian and books:
            now = timezone.now()
            borrow_scenarios = [
                # (user_idx, book_idx, status, days_ago, due_offset, return_offset)
                (0, 0, "returned", 30, 14, 12),   # sv_an trả Clean Code (đúng hạn)
                (0, 1, "borrowed", 7,  14, None),  # sv_an đang mượn Python
                (1, 3, "pending",  1,  14, None),  # sv_binh chờ duyệt ML
                (1, 4, "returned", 20, 14, 18),   # sv_binh trả Tư duy (trễ 4 ngày) -> unpaid
                (2, 5, "borrowed", 5,  14, None),  # sv_cuong đang mượn Đắc Nhân Tâm
                (2, 6, "borrowed", 25, 14, None),  # sv_cuong đang mượn nhưng quá hạn (thực tế over 11 ngày)
                (3, 7, "returned", 45, 14, 16),   # sv_dung trả Chí Phèo (trễ 2 ngày) -> paid
                (3, 8, "borrowed", 3,  14, None),  # sv_dung mượn Dế Mèn
                
                # Thêm test data
                (0, 9, "returned", 50, 14, 14),   # sv_an trả đúng hạn (Mắt biếc)
                (0, 10, "overdue", 30, 14, None), # sv_an quá hạn (Sapiens)
                (1, 11, "returned", 60, 14, 20),  # sv_binh trả trễ 6 ngày -> unpaid (Toán học)
                (1, 12, "borrowed", 2, 14, None), # sv_binh mượn Tâm lý học đám đông
                (2, 13, "returned", 70, 14, 15),  # sv_cuong trả trễ 1 ngày -> paid (Homo Deus)
                (2, 14, "pending", 2, 14, None),  # sv_cuong đang chờ duyệt (Lịch sử VN)
                (3, 2, "borrowed", 16, 14, None), # sv_dung đang mượn nhưng đã lố 2 ngày (Algorithms)
                (3, 4, "returned", 80, 14, 10),   # sv_dung trả sớm 4 ngày (Tư duy)
            ]
            borrow_created = 0
            for user_idx, book_idx, status, days_ago, due_days, return_offset in borrow_scenarios:
                if user_idx >= len(readers) or book_idx >= len(books):
                    continue
                user = readers[user_idx % len(readers)]
                book = books[book_idx % len(books)]
                borrow_date = now - timedelta(days=days_ago)
                due_date = borrow_date + timedelta(days=due_days)
                return_date = borrow_date + timedelta(days=return_offset) if return_offset else None

                if BorrowRecord.objects.filter(user=user, book=book, status=status).exists():
                    continue

                fine_amount = 0
                fine_status = 'none'
                if return_date and return_offset > due_days:
                    fine_amount = (return_offset - due_days) * 5000
                    fine_status = 'unpaid' if user_idx == 1 else 'paid'

                record = BorrowRecord.objects.create(
                    user=user,
                    book=book,
                    borrow_date=borrow_date,
                    due_date=due_date,
                    return_date=return_date,
                    status=status,
                    approved_by=librarian if status not in ["pending"] else None,
                    notes="Phiếu mượn mẫu" if days_ago < 20 else "Nhắc nhở: sách quá hạn!",
                )
                
                if fine_amount > 0:
                    FineReceipt.objects.create(
                        borrow_record=record,
                        reason='late_fee',
                        amount=fine_amount,
                        status=fine_status
                    )
                if status == "borrowed" and book.available_copies > 0:
                    book.available_copies -= 1
                    book.save()

                self.stdout.write(f"   ✓ {user.username} ← {book.title[:40]} [{status}]")
                borrow_created += 1

            self.stdout.write(self.style.SUCCESS(f"   → {borrow_created} phiếu mượn\n"))

            # 6. Reservations
            self.stdout.write("🔖 Tạo đặt trước...")
            reservation_data = [
                (0, 2),  # sv_an → Introduction to Algorithms
                (1, 9),  # sv_binh → Mắt biếc
            ]
            res_created = 0
            for user_idx, book_idx in reservation_data:
                if user_idx >= len(readers) or book_idx >= len(books):
                    continue
                user = readers[user_idx]
                book = books[book_idx % len(books)]
                if not Reservation.objects.filter(user=user, book=book).exists():
                    Reservation.objects.create(
                        user=user,
                        book=book,
                        reserved_at=now - timedelta(days=1),
                        expires_at=now + timedelta(days=2),
                        status="active",
                    )
                    self.stdout.write(f"   ✓ {user.username} đặt trước: {book.title[:40]}")
                    res_created += 1
            self.stdout.write(self.style.SUCCESS(f"   → {res_created} đặt trước\n"))

        # 7. Book Proposals
        self.stdout.write("💡 Tạo đề xuất sách...")
        librarian_user = CustomUser.objects.filter(role__in=["librarian", "admin"]).first()
        proposals_created = 0
        for data in PROPOSALS:
            user = CustomUser.objects.filter(username=data["username"]).first()
            if not user:
                continue
            if BookProposal.objects.filter(user=user, title=data["title"]).exists():
                continue
            proposal = BookProposal.objects.create(
                user=user,
                title=data["title"],
                author_name=data.get("author_name", ""),
                isbn=data.get("isbn", ""),
                reason=data["reason"],
                status=data["status"],
                admin_notes=(
                    "Đề xuất hợp lý, sẽ xem xét bổ sung vào quý tới." if data["status"] == "approved"
                    else "Sách này chưa phù hợp với chương trình đào tạo hiện tại." if data["status"] == "rejected"
                    else ""
                ),
                reviewed_by=librarian_user if data["status"] != "pending" else None,
            )
            self.stdout.write(f"   ✓ {user.username}: {proposal.title[:50]} [{data['status']}]")
            proposals_created += 1
        self.stdout.write(self.style.SUCCESS(f"   → {proposals_created} đề xuất\n"))

        # 8. Reviews
        self.stdout.write("⭐ Tạo đánh giá sách...")
        reviews_created = 0
        # Chỉ tạo review cho sách đã được trả
        returned_records = BorrowRecord.objects.filter(status="returned").select_related("user", "book")
        ratings_pool = [5, 5, 4, 4, 4, 3, 5, 4]
        for i, record in enumerate(returned_records):
            if Review.objects.filter(user=record.user, book=record.book).exists():
                continue
            review = Review.objects.create(
                user=record.user,
                book=record.book,
                rating=ratings_pool[i % len(ratings_pool)],
                comment=REVIEW_COMMENTS[i % len(REVIEW_COMMENTS)],
            )
            self.stdout.write(f"   ✓ {record.user.username} → {record.book.title[:40]} ({review.rating}★)")
            reviews_created += 1
        self.stdout.write(self.style.SUCCESS(f"   → {reviews_created} đánh giá\n"))

        # ── Summary ───────────────────────────────────────────────────────────
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ HOÀN THÀNH! Tóm tắt dữ liệu đã tạo:"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"  📂 Thể loại      : {Category.objects.count()}")
        self.stdout.write(f"  ✍️  Tác giả       : {Author.objects.count()}")
        self.stdout.write(f"  🏢 Nhà xuất bản  : {Publisher.objects.count()}")
        self.stdout.write(f"  📚 Sách          : {Book.objects.count()}")
        self.stdout.write(f"  🔄 Phiếu mượn    : {BorrowRecord.objects.count()}")
        self.stdout.write(f"  🔖 Đặt trước     : {Reservation.objects.count()}")
        self.stdout.write(f"  💡 Đề xuất       : {BookProposal.objects.count()}")
        self.stdout.write(f"  ⭐ Đánh giá      : {Review.objects.count()}")
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("\n🎉 Hệ thống sẵn sàng kiểm thử tại http://localhost:8000\n"))
