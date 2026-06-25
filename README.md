# 📚 LiMS — Hệ thống Quản lý Thư viện

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Alpine-DC382D?style=for-the-badge&logo=redis&logoColor=white)

**LiMS** (Library Management System) là hệ thống quản lý thư viện tích hợp dành cho trường đại học,  
hỗ trợ sinh viên mượn/trả sách, đặt trước, đề xuất bổ sung sách và đánh giá tài liệu.

</div>

---

## 🗂 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Yêu cầu cài đặt](#-yêu-cầu-cài-đặt)
- [Hướng dẫn chạy](#-hướng-dẫn-chạy)
- [Tài khoản mẫu](#-tài-khoản-mẫu)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Lệnh hữu ích](#-lệnh-hữu-ích)

---

## 📖 Giới thiệu

LiMS được xây dựng theo mô hình **Client–Server** sử dụng Django làm backend và template engine, thiết kế giao diện **Holographic 3D Light Mode** hiện đại, responsive hoàn toàn từ mobile đến desktop.

| Thành phần | Công nghệ |
|---|---|
| Backend | Django 4.2 (Python 3.11) |
| Database | MySQL 8.0 |
| Task Queue | Celery + Redis |
| Frontend | Django Templates + Bootstrap 5.3 + Vanilla JS |
| Container | Docker + Docker Compose |

---

## ✨ Tính năng

### 👤 Phân quyền 3 cấp
| Role | Mô tả |
|---|---|
| **Sinh viên** (reader) | Tìm kiếm sách, mượn/trả, đặt trước, đề xuất, đánh giá |
| **Giảng viên / Thủ thư** (librarian) | Quản lý sách, duyệt mượn/trả, duyệt đề xuất |
| **Quản trị viên** (admin) | Toàn quyền + quản lý tài khoản người dùng |

### 📚 Quản lý danh mục
- Thêm/sửa/xóa sách, tác giả, nhà xuất bản, thể loại
- Upload ảnh bìa và file PDF
- Tìm kiếm theo tên, tác giả, ISBN, thể loại, trạng thái

### 🔄 Mượn / Trả sách
- Sinh viên gửi yêu cầu mượn → Thủ thư duyệt → Mượn → Trả
- Theo dõi hạn trả, cảnh báo quá hạn
- Lịch sử mượn sách cá nhân

### 🔖 Đặt trước
- Đặt trước khi sách không có sẵn (hạn 3 ngày)
- Quản lý danh sách đặt trước cá nhân

### 💡 Đề xuất sách
- Sinh viên đề xuất mua sách mới
- Thủ thư/Admin duyệt hoặc từ chối kèm phản hồi

### ⭐ Đánh giá sách
- Đánh giá 1–5 sao + nhận xét (chỉ sau khi đã mượn và trả)
- Hiển thị điểm trung bình trên trang chi tiết sách

---

## 🏗 Kiến trúc hệ thống

```
┌──────────────────────────────────────────────────────┐
│                    Docker Network                    │
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌───────────────┐  │
│  │  lims_web │    │ lims_db  │    │  lims_redis   │  │
│  │ Django   │◄──►│ MySQL8.0 │    │  Redis Alpine │  │
│  │ :8000    │    │  :3306   │    │    :6379      │  │
│  └────┬─────┘    └──────────┘    └───────┬───────┘  │
│       │                                  │           │
│  ┌────▼─────┐                   ┌────────▼───────┐  │
│  │          │                   │    :8001       │  │
│  └──────────┘                   └────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## 💻 Yêu cầu cài đặt

Máy tính chỉ cần cài đúng **2 thứ**:

| Phần mềm | Phiên bản tối thiểu | Link tải |
|---|---|---|
| **Docker Desktop** | 24.x trở lên | https://www.docker.com/products/docker-desktop |
| **Git** | bất kỳ | https://git-scm.com/downloads |

> **Không cần** cài Python, MySQL, hay bất kỳ thứ gì khác.  
> Tất cả đều chạy trong Docker container.

---

## 🚀 Hướng dẫn chạy

### Bước 1 — Cài Docker Desktop

1. Truy cập https://www.docker.com/products/docker-desktop
2. Tải bản phù hợp với hệ điều hành (Windows / macOS / Linux)
3. Cài đặt và **khởi động Docker Desktop**
4. Đợi icon Docker ở thanh taskbar/menu bar chuyển sang màu **xanh** (running)

> ⚠️ Trên Windows: Docker Desktop yêu cầu **WSL 2**. Nếu được hỏi, chọn "Install WSL 2 backend".

---

### Bước 2 — Tải mã nguồn

Mở **Terminal** (macOS/Linux) hoặc **PowerShell** (Windows), chạy:

```bash
git clone <URL_REPOSITORY> lims_project
cd lims_project
```

> Nếu không dùng Git, có thể tải file ZIP từ repository rồi giải nén.

---

### Bước 3 — Tạo file cấu hình `.env`

Sao chép file mẫu:

```bash
# macOS / Linux
cp .env.example .env

# Windows PowerShell
copy .env.example .env
```

File `.env` mặc định đã dùng được ngay. Nếu muốn thay đổi mật khẩu, mở file và chỉnh sửa:

```env
# .env — Cấu hình mặc định (có thể dùng ngay)
MYSQL_DATABASE=lims_db
MYSQL_USER=lims_user
MYSQL_PASSWORD=lims_password
MYSQL_ROOT_PASSWORD=root_password
DB_HOST=db
DB_PORT=3306

SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=*

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0


```

---

### Bước 4 — Build và khởi động

```bash
docker compose up -d --build
```

> Lần đầu sẽ tải Docker images (~2–5 phút tùy tốc độ mạng). Các lần sau chỉ mất vài giây.

Kiểm tra tất cả container đang chạy:

```bash
docker compose ps
```

Kết quả mong đợi:

```
NAME             STATUS          PORTS
lims_celery      Up
lims_db          Up              0.0.0.0:3306->3306/tcp
lims_redis       Up              0.0.0.0:6379->6379/tcp
lims_web         Up              0.0.0.0:8000->8000/tcp
```

---

### Bước 5 — Khởi tạo cơ sở dữ liệu

Chạy lần lượt 3 lệnh sau (chỉ cần chạy **một lần duy nhất**):

```bash
# 1. Tạo bảng trong database
docker compose exec web python manage.py migrate

# 2. Tạo tài khoản mẫu (admin, giảng viên, sinh viên)
docker compose exec web python manage.py seed_users

# 3. Tạo dữ liệu mẫu (sách, mượn trả, đề xuất, đánh giá...)
docker compose exec web python manage.py seed_data
```

---

### Bước 6 — Truy cập ứng dụng

| URL | Mô tả |
|---|---|
| **http://localhost:8000** | Trang chủ hệ thống LiMS |
| **http://localhost:8000/accounts/login/** | Trang đăng nhập |
| **http://localhost:8000/admin/** | Django Admin panel |

🎉 **Xong!** Hệ thống đã sẵn sàng.

---

## 🔑 Tài khoản mẫu

### Quản trị viên
| Username | Mật khẩu | Quyền |
|---|---|---|
| `admin` | `Admin@123` | Toàn quyền hệ thống |

### Giảng viên / Thủ thư
| Username | Mật khẩu | Khoa |
|---|---|---|
| `gv_nguyen` | `GiangVien@123` | Khoa Công nghệ Thông tin |
| `gv_tran` | `GiangVien@123` | Khoa Kinh tế |

### Sinh viên
| Username | Mật khẩu |
|---|---|
| `sv_an` | `SinhVien@123` |
| `sv_binh` | `SinhVien@123` |
| `sv_cuong` | `SinhVien@123` |
| `sv_dung` | `SinhVien@123` |

---

## 📁 Cấu trúc thư mục

```
lims_project/
│
├── 📄 docker-compose.yml       # Định nghĩa các services Docker
├── 📄 Dockerfile               # Image cho web & celery
├── 📄 requirements.txt         # Thư viện Python
├── 📄 manage.py                # Django CLI
├── 📄 .env                     # Biến môi trường (tự tạo từ .env.example)
├── 📄 .env.example             # Mẫu file .env
│
├── 📂 lims_project/            # Cấu hình Django
│   ├── settings.py             # Cài đặt chính
│   ├── urls.py                 # URL routing gốc
│   ├── celery.py               # Cấu hình Celery
│   └── views.py                # View trang chủ
│
├── 📂 apps/                    # Các Django apps
│   ├── accounts/               # Quản lý tài khoản & phân quyền
│   │   └── management/
│   │       └── commands/
│   │           ├── seed_users.py   # Lệnh tạo tài khoản mẫu
│   │           └── seed_data.py    # Lệnh tạo dữ liệu mẫu
│   ├── catalog/                # Quản lý sách, tác giả, thể loại
│   ├── circulation/            # Mượn/trả sách, đặt trước
│   ├── proposals/              # Đề xuất mua sách mới
│   ├── reviews/                # Đánh giá sách
│
├── 📂 templates/               # Base templates dùng chung
│   ├── base.html               # Layout chính (sidebar + topbar)
│   └── home.html               # Dashboard trang chủ
│
└── 📂 static/
    ├── css/style.css           # Design system (Holographic 3D Light)
    └── js/main.js              # JavaScript xử lý UI
```

---

## 🛠 Lệnh hữu ích

### Quản lý Docker

```bash
# Khởi động hệ thống
docker compose up -d

# Dừng hệ thống
docker compose down

# Xem log realtime
docker compose logs -f web

# Xem log của service cụ thể
docker compose logs -f web
docker compose logs -f celery

# Khởi động lại service
docker compose restart web
```

### Quản lý Django

```bash
# Mở Django shell
docker compose exec web python manage.py shell

# Tạo migration sau khi sửa model
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Thu thập static files (production)
docker compose exec web python manage.py collectstatic

# Tạo lại dữ liệu mẫu (xóa cũ, tạo mới)
docker compose exec web python manage.py seed_data --clear
docker compose exec web python manage.py seed_data

# Reset tài khoản mẫu về mật khẩu gốc
docker compose exec web python manage.py seed_users --reset
```

### Xử lý sự cố thường gặp

**❓ Lỗi `docker-credential-desktop` khi build:**
```bash
# Mở file config Docker và xóa dòng chứa "credsStore"
# macOS: ~/.docker/config.json
# Windows: C:\Users\<tên>\AppData\Roaming\Docker\config.json
```

**❓ Port 8000 đã bị chiếm:**
```bash
# Đổi port trong docker-compose.yml
ports:
  - "8080:8000"  # dùng port 8080 thay vì 8000
```

**❓ Database chưa sẵn sàng (lỗi kết nối MySQL):**
```bash
# Đợi MySQL khởi động xong (~15 giây) rồi chạy lại migrate
docker compose logs db  # kiểm tra MySQL đã ready chưa
docker compose exec web python manage.py migrate
```

**❓ Muốn xóa toàn bộ data và làm lại từ đầu:**
```bash
docker compose down -v   # xóa cả volumes (database)
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_users
docker compose exec web python manage.py seed_data
```

---

## 📝 Ghi chú phát triển

- **Không dùng SPA** (React/Vue) — toàn bộ render server-side với Django Templates
- **Bootstrap 5.3** + **Bootstrap Icons** tải qua CDN
- **Font Inter** tải qua Google Fonts
- **Celery** dùng để xử lý tác vụ nền (gửi email nhắc nhở, ...)

---

<div align="center">
  <sub>Built with ❤️ using Django + Docker</sub>
</div>
