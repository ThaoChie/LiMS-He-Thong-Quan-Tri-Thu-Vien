# 📚 LiMS — Hệ thống Quản lý Thư viện Đại học (Library Management System)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Alpine-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.3-37814A?style=for-the-badge&logo=celery&logoColor=white)

**LiMS** là nền tảng quản lý thư viện số tích hợp hiện đại chuẩn nghiệp vụ **SRS v4.0 / v5.0**, được thiết kế tối ưu cho các trường đại học. Hệ thống giải quyết bài toán tự động hóa luồng lưu thông sách, chuẩn hóa quy trình đề xuất bổ sung tài liệu theo chuẩn quốc tế **ISBN**, và áp dụng mô hình **Quản lý Tín nhiệm (Trust & Violation Model)** hiện đại thay thế hoàn toàn hình thức thu phí phạt truyền thống.

</div>

---

## 🌟 Điểm nổi bật trong chuẩn nghiệp vụ (SRS v4.0 / v5.0)

- 🔒 **Bảo mật & Phân quyền chặt chẽ (BR-30):** Khách vãng lai (Guest) chỉ được phép truy cập cổng đăng nhập. Mọi thao tác tra cứu, tìm kiếm và xem chi tiết sách bắt buộc phải xác thực tài khoản hợp lệ.
- 📦 **Chuẩn hóa Đề xuất & Phê duyệt theo ISBN (UC05, UC06):** Gom nhóm thông minh các đề xuất sách trùng mã **ISBN**. Hỗ trợ tính năng **Mass Approve** giúp Thủ thư phê duyệt đồng loạt tất cả yêu cầu cùng một đầu sách chỉ với 1 thao tác và gửi email thông báo tự động cho các giảng viên/sinh viên liên quan.
- 🛡️ **Mô hình Quản lý Tín nhiệm - Triệt tiêu Phí phạt (BR-13, BR-18, BR-19, BR-23):** Loại bỏ hoàn toàn các khâu thu tiền phạt trễ hạn rắc rối. Hệ thống ghi nhận trạng thái vi phạm (**Overdue / Reported Lost**) và tự động khóa quyền mượn sách (`can_borrow = False`) cũng như chặn đặt trước tài liệu đối với độc giả vi phạm cho đến khi hoàn tất bồi thường và được Thủ thư gỡ vi phạm.
- 📊 **Dashboard Thống kê Thời gian thực:** Cung cấp chỉ số trực quan về số lượng vi phạm tín nhiệm, tỷ lệ độc giả bị khóa tài khoản, và hiệu quả phê duyệt đề xuất mua sách theo mã ISBN.

---

## 🛠 Tech Stack (Công nghệ sử dụng)

| Thành phần | Công nghệ / Thư viện | Vai trò & Mục đích |
|---|---|---|
| **Backend Core** | Django 4.2 (Python 3.11) | Xử lý kiến trúc MVT, bảo mật, ORM và định tuyến nghiệp vụ |
| **Database** | MySQL 8.0 | Lưu trữ cấu trúc quan hệ chặt chẽ đảm bảo tính toàn vẹn dữ liệu (ACID) |
| **Async Task / Queue** | Celery 5.3 + Redis Alpine | Xử lý hàng đợi gửi Email thông báo mượt mà, chạy Cronjob kiểm tra hạn trả sách |
| **Frontend UI/UX** | Bootstrap 5.3 + HTMX + Vanilla JS | Giao diện hiện đại (Glassmorphism / Cards), tương tác bất đồng bộ không cần reload trang |
| **Containerization** | Docker & Docker Compose | Đóng gói toàn bộ dịch vụ (Web, DB, Redis, Celery, ChromaDB) chạy nhất quán trên mọi môi trường |

---

## 🏗 Kiến trúc Hệ thống

```
┌──────────────────────────────────────────────────────────────┐
│                        Docker Network                        │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │   lims_web   │    │   lims_db    │    │   lims_redis   │  │
│  │  Django Web  │◄──►│  MySQL 8.0   │    │  Redis Broker  │  │
│  │  Port: 8000  │    │  Port: 3306  │    │   Port: 6379   │  │
│  └──────┬───────┘    └──────────────┘    └───────┬────────┘  │
│         │                                        │           │
│  ┌──────▼───────┐                        ┌───────▼────────┐  │
│  │ lims_celery  │                        │ lims_chromadb  │  │
│  │ Celery Worker│                        │ Vector Storage │  │
│  │ Async Tasks  │                        │   Port: 8001   │  │
│  └──────────────┘                        └────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 👥 Phân quyền Người dùng (Roles)

1. **👨‍🎓 Sinh viên / Giảng viên (Reader):**
   - Tra cứu danh mục sách, xem tình trạng sẵn có.
   - Gửi yêu cầu mượn sách, đặt trước tài liệu khi sách đang hết.
   - Đề xuất mua sách mới theo mã ISBN.
   - Viết đánh giá & cho điểm sao (chỉ áp dụng với sách đã mượn và trả hoàn tất).
   - Theo dõi điểm tín nhiệm và lịch sử vi phạm cá nhân.

2. **👩‍💼 Thủ thư (Librarian):**
   - Quản lý kho sách, thể loại, nhà xuất bản.
   - Xử lý mượn/trả sách tại quầy, kiểm tra tình trạng hư hỏng.
   - Ghi nhận vi phạm tín nhiệm (Trả trễ / Mất sách) và thao tác **Gỡ vi phạm**.
   - Phê duyệt đề xuất mua sách đồng loạt (Mass Approve).

3. **⚙️ Quản trị viên (Admin):**
   - Toàn quyền giám sát hệ thống và phân quyền người dùng.
   - Theo dõi chỉ số cảnh báo tín nhiệm & thống kê hiệu quả thư viện qua Dashboard.

---

## 🚀 Hướng dẫn Cài đặt & Khởi chạy (Docker)

Hệ thống đã được tích hợp sẵn cấu hình Docker Compose, giúp việc triển khai chỉ mất vài phút.

### 1. Yêu cầu hệ thống
- Máy tính đã cài đặt **Docker** và **Docker Compose**.

### 2. Khởi chạy hệ thống
Mở terminal tại thư mục gốc của dự án và chạy lệnh:
```bash
docker-compose up --build -d
```

### 3. Tạo dữ liệu mẫu (Seed Data)
Để có ngay dữ liệu test phong phú (sách, người dùng, phiếu mượn, đề xuất, vi phạm...), chạy lệnh sau:
```bash
docker exec lims_web python manage.py seed_data
```

### 4. Kiểm thử tự động (Unit Tests)
Chạy bộ test kiểm chứng độ bao phủ nghiệp vụ:
```bash
docker exec lims_web python manage.py test
```

---

## 🔑 Tài khoản Demo (Sẵn sàng trải nghiệm)

Sau khi chạy lệnh `seed_data`, hệ thống sẽ tự động khởi tạo các tài khoản chuẩn với mật khẩu chung là `password123`:

| Vai trò | Tài khoản Đăng nhập | Mật khẩu | Ghi chú |
|---|---|---|---|
| **👑 Admin** | `admin` | `password123` | Quản trị viên tối cao (Đã tắt OTP 2FA để tiện demo) |
| **👩‍💼 Thủ thư** | `librarian` | `password123` | Quản lý lưu thông & duyệt sách (Đã tắt OTP 2FA) |
| **👨‍🏫 Giảng viên** | `lecturer1` | `password123` | Hạn mức mượn cao (5 cuốn), ưu tiên đề xuất |
| **👨‍🎓 Sinh viên** | `student1` | `password123` | Hạn mức mượn chuẩn (3 cuốn) |
| **👨‍🎓 Sinh viên** | `student2` | `password123` | Tài khoản sinh viên thứ 2 |

> 💡 **Lưu ý kiểm thử:** Để tạo sự thuận tiện tối đa cho việc demo nghiệm thu đồ án, tính năng gửi mã xác thực 2 bước (OTP 2FA) qua email cho role Admin và Thủ thư đã được **tạm thời đăng nhập thẳng**.

---

## 📁 Cấu trúc Thư mục

```text
lims_project/
├── apps/
│   ├── accounts/          # Quản lý người dùng, phân quyền, đăng nhập & OTP
│   ├── catalog/           # Quản lý đầu sách, danh mục, kiểm soát quyền Guest
│   ├── circulation/       # Nghiệp vụ mượn/trả, đặt trước, quản lý vi phạm tín nhiệm
│   ├── proposals/         # Nghiệp vụ đề xuất mua sách theo ISBN & Mass Approve
│   ├── reviews/           # Đánh giá & bình luận sách
│   └── dashboard/         # Thống kê quản trị & lịch sử tín nhiệm cá nhân
├── lims_project/          # Cấu hình core Django, Celery setup
├── templates/             # Giao diện tổng thể Bootstrap 5 + HTMX
├── media/                 # Lưu trữ ảnh bìa sách, tài liệu tải lên
├── docker-compose.yml     # Cấu hình triển khai đa container
└── README.md              # Tài liệu giới thiệu hệ thống
```
