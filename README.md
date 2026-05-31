## 📚 LiMS — Hệ thống Quản lý Thư viện

LiMS (Library Management System) là hệ thống quản lý thư viện tích hợp dành cho trường đại học, hỗ trợ sinh viên mượn/trả sách, đặt trước, đề xuất bổ sung sách và đánh giá tài liệu.

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

| Thành phần   | Công nghệ                                     |
| ------------ | --------------------------------------------- |
| Backend      | Django 4.2 (Python 3.11)                      |
| Database     | MySQL 8.0                                     |
| Task Queue   | Celery + Redis                                |
| Vector Store | ChromaDB (dành cho RAG — mở rộng sau)         |
| Frontend     | Django Templates + Bootstrap 5.3 + Vanilla JS |
| Container    | Docker + Docker Compose                       |

---

## ✨ Tính năng

### 👤 Phân quyền 3 cấp

| Role                                 | Mô tả                                                 |
| ------------------------------------ | ----------------------------------------------------- |
| **Sinh viên** (reader)               | Tìm kiếm sách, mượn/trả, đặt trước, đề xuất, đánh giá |
| **Giảng viên / Thủ thư** (librarian) | Quản lý sách, duyệt mượn/trả, duyệt đề xuất           |
| **Quản trị viên** (admin)            | Toàn quyền + quản lý tài khoản người dùng             |

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
