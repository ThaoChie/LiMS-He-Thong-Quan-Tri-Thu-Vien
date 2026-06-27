"""
Management command: seed_users
Tạo tài khoản mẫu cho các role: admin, librarian (giảng viên), reader (sinh viên)
"""
from django.core.management.base import BaseCommand
from apps.accounts.models import CustomUser


SAMPLE_USERS = [
    # ── ADMIN ──────────────────────────────────────────
    {
        "username": "admin",
        "email": "admin@lims.edu.vn",
        "password": "Admin@123",
        "role": "admin",
        "first_name": "Quản trị",
        "last_name": "Viên",
        "phone_number": "0900000001",
        "address": "Phòng Quản trị, Thư viện Trung tâm",
    },
    # ── GIẢNG VIÊN / THỦ THƯ ───────────────────────────
    {
        "username": "gv_nguyen",
        "email": "nguyen.tv@lims.edu.vn",
        "password": "GiangVien@123",
        "role": "librarian",
        "first_name": "Văn",
        "last_name": "Nguyễn Thành",
        "phone_number": "0911111111",
        "address": "Khoa Công nghệ Thông tin",
    },
    {
        "username": "gv_tran",
        "email": "tran.lh@lims.edu.vn",
        "password": "GiangVien@123",
        "role": "librarian",
        "first_name": "Lan Hương",
        "last_name": "Trần",
        "phone_number": "0911111112",
        "address": "Khoa Kinh tế",
    },
    # ── SINH VIÊN / BẠN ĐỌC ────────────────────────────
    {
        "username": "sv_an",
        "email": "an.nv@student.lims.edu.vn",
        "password": "SinhVien@123",
        "role": "reader",
        "first_name": "Văn An",
        "last_name": "Nguyễn",
        "phone_number": "0922222221",
        "address": "Ký túc xá A, Phòng 201",
    },
    {
        "username": "sv_binh",
        "email": "binh.lt@student.lims.edu.vn",
        "password": "SinhVien@123",
        "role": "reader",
        "first_name": "Thị Bình",
        "last_name": "Lê",
        "phone_number": "0922222222",
        "address": "Ký túc xá B, Phòng 305",
    },
    {
        "username": "sv_cuong",
        "email": "cuong.pv@student.lims.edu.vn",
        "password": "SinhVien@123",
        "role": "reader",
        "first_name": "Văn Cường",
        "last_name": "Phạm",
        "phone_number": "0922222223",
        "address": "123 Nguyễn Trãi, Q.1",
    },
    {
        "username": "sv_dung",
        "email": "dung.ht@student.lims.edu.vn",
        "password": "SinhVien@123",
        "role": "reader",
        "first_name": "Thị Dung",
        "last_name": "Hoàng",
        "phone_number": "0922222224",
        "address": "456 Lê Lợi, Q.3",
    },
]


class Command(BaseCommand):
    help = "Seed tài khoản mẫu cho hệ thống VietNhatLiMS"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Xóa và tạo lại tài khoản mẫu đã tồn tại",
        )

    def handle(self, *args, **options):
        reset = options["reset"]
        created = 0
        skipped = 0
        updated = 0

        for data in SAMPLE_USERS:
            username = data["username"]
            existing = CustomUser.objects.filter(username=username).first()

            if existing:
                if reset:
                    existing.set_password(data["password"])
                    existing.email = data["email"]
                    existing.role = data["role"]
                    existing.first_name = data["first_name"]
                    existing.last_name = data["last_name"]
                    existing.phone_number = data["phone_number"]
                    existing.address = data["address"]
                    existing.is_active = True
                    existing.save()
                    self.stdout.write(
                        self.style.WARNING(f"  ↻ Đã cập nhật: {username}")
                    )
                    updated += 1
                else:
                    self.stdout.write(
                        self.style.NOTICE(f"  ⏭ Bỏ qua (đã tồn tại): {username}")
                    )
                    skipped += 1
                continue

            user = CustomUser.objects.create_user(
                username=username,
                email=data["email"],
                password=data["password"],
                role=data["role"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone_number=data["phone_number"],
                address=data["address"],
                is_active=True,
            )
            # Cấp quyền staff/superuser cho admin
            if data["role"] == "admin":
                user.is_staff = True
                user.is_superuser = True
                user.save()

            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Đã tạo [{data['role'].upper():12}]: {username}")
            )
            created += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS(f"  Tạo mới : {created}"))
        self.stdout.write(self.style.WARNING(f"  Cập nhật: {updated}"))
        self.stdout.write(self.style.NOTICE(f"  Bỏ qua  : {skipped}"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write("")
        self.stdout.write("📋 THÔNG TIN ĐĂNG NHẬP MẪU:")
        self.stdout.write("─" * 50)
        self.stdout.write(
            f"{'Role':<14} {'Username':<15} {'Mật khẩu'}"
        )
        self.stdout.write("─" * 50)
        for u in SAMPLE_USERS:
            role_label = {
                "admin": "Quản trị viên",
                "librarian": "Giảng viên",
                "reader": "Sinh viên",
            }[u["role"]]
            self.stdout.write(
                f"{role_label:<14} {u['username']:<15} {u['password']}"
            )
        self.stdout.write("─" * 50)
