# Báo cáo Kiểm tra chéo (Double Check) Hệ thống LiMS so với Tài liệu SRS v4.0

Dựa trên quá trình kiểm tra mã nguồn hiện tại của dự án và đối chiếu với tài liệu `SRS_DEHA_NHOM2_v4.0.md`, dưới đây là danh sách chi tiết các chức năng/thành phần đang bị **thiếu** (Missing) hoặc **sai lệch/chưa đúng** (Incorrect) so với thiết kế:

## 1. Các Module và Chức năng bị THIẾU hoàn toàn (Missing)

*   **App `dashboard` (UC14 & UC15):** 
    *   Toàn bộ app `dashboard` chưa được khởi tạo. 
    *   **UC14 (Dashboard Thống kê cho Admin/Thủ thư):** Không tồn tại. Thiếu các widget thống kê tổng quan (tổng sách, user, đang mượn, quá hạn), biểu đồ, top 10 sách phổ biến, và thống kê doanh thu phạt.
*   **Hệ thống Background Tasks (Celery & Redis):**
    *   Hoàn toàn không có file `tasks.py` trong các app.
    *   Việc gửi email hiện tại đang thực hiện đồng bộ (synchronous) ngay trong HTTP request, gây block hệ thống và vi phạm nguyên tắc kiến trúc số [9].
    *   Thiếu toàn bộ các Cronjob tự động: `remind_due_date_task()` (nhắc nhở trước hạn), `auto_expire_reservations()` (hủy đặt trước quá hạn 48h), `auto_mark_overdue()` (đánh dấu quá hạn).
*   **Luồng RAG Pipeline (Xử lý PDF):**
    *   Thiếu Model `PDFDocument` để lưu trữ trạng thái nhúng (embed_status).
    *   Thiếu task `process_pdf_rag(book_id)` để chia chunks và đẩy dữ liệu vào ChromaDB.

## 2. Các Chức năng bị SAI LỆCH hoặc CHƯA ĐẦY ĐỦ (Incorrect / Incomplete)

*   **UC09 (Xử lý Mượn Sách tại Quầy): Sai luồng hoàn toàn**
    *   **Thiết kế SRS:** User mang sách ra quầy, Thủ thư nhập/quét mã sinh viên và mã sách để tạo phiếu mượn trực tiếp (Counter Borrowing).
    *   **Thực tế code:** Hiện đang làm theo luồng User "Yêu cầu mượn online" (`borrow_request_view` trạng thái `pending`) và Thủ thư vào màn hình quản lý để "Duyệt" (`approve_borrow_view`). Điều này sai hoàn toàn với nghiệp vụ thực tế của thư viện được mô tả.
*   **UC11 (Trả sách / Báo Hỏng / Mất): Thiếu luồng "Sách bị hỏng"**
    *   **Thiết kế SRS:** Khi trả sách, Thủ thư phải có tuỳ chọn chọn tình trạng sách (Nguyên vẹn / Hỏng / Mất). Nếu hỏng, Thủ thư tự nhập số tiền phạt.
    *   **Thực tế code:** Hàm `return_book_view` chỉ tự động tính phạt trễ hạn (Late fee), hoàn toàn không có input để chọn tình trạng sách hỏng và nhập tiền đền bù.
*   **UC16 (Quản lý Hàng đợi Đặt trước): Thiếu chức năng cho Staff**
    *   **Thiết kế SRS:** Thủ thư xem được toàn bộ danh sách hàng đợi đặt trước của tất cả các sách, có thể can thiệp (Hủy reservation của user, xem ngày thông báo...).
    *   **Thực tế code:** Chỉ có view `reservation_list_view` cho User xem các sách mình đã đặt. Thủ thư/Admin **không có màn hình** quản lý hàng đợi.
*   **UC15 (Xem Lịch sử Mượn/Trả cá nhân): Làm sai vị trí và thiếu dữ liệu**
    *   **Thiết kế SRS:** Nằm trong app `dashboard`, có 4 Tab: Đang mượn, Đã trả, Đặt trước, Phiếu phạt.
    *   **Thực tế code:** Tạm nằm ở `circulation/borrow_history_view` nhưng chỉ hiển thị các `BorrowRecord`. Không tổng hợp `Reservation` và `FineReceipt` vào cùng một giao diện như yêu cầu.
*   **UC17 (Thanh toán Phạt): Thiếu Phương thức thanh toán (BR-32)**
    *   **Thiết kế SRS:** BR-32 yêu cầu mỗi lần thanh toán phạt phải ghi nhận phương thức (Tiền mặt / Chuyển khoản).
    *   **Thực tế code:** Model `FineReceipt` thiếu field `payment_method`. View `pay_fine_view` chỉ đơn giản chuyển status sang 'paid' mà không yêu cầu chọn hình thức thu tiền.
*   **Model `Reservation` (Đặt trước): Sai thiết kế thuộc tính**
    *   **Thiết kế SRS:** Các status là: `Waiting, Notified, Completed, Expired, Cancelled`. Cần có thuộc tính `queue_position` và `notified_at`.
    *   **Thực tế code:** Các status đang là: `active, fulfilled, cancelled, expired`. Thiếu `queue_position` và `notified_at` để tính toán 48h ưu tiên.
*   **Model `Book` (Kho sách): Sai cấu trúc**
    *   **Thiết kế SRS:** `author` là một trường Text (CharField max 255). File PDF được tách riêng ra Model `PDFDocument`.
    *   **Thực tế code:** `authors` đang là ManyToManyField nối đến bảng `Author` riêng (sai thiết kế Input Data). Trường `pdf_file` đang được nhét trực tiếp vào bảng `Book`.

## 3. Các chức năng "Thừa" hoặc Ngoài Luồng (Out of Scope)
*   **Hệ thống Accounts:** Đang triển khai tính năng tự do "Đăng ký tài khoản" (`register_view`), "Quên mật khẩu", và xác thực 2 bước (2FA / OTP). Trong khi SRS định nghĩa quyền tạo User thuộc về Admin (UC03a, UC03e) và User chỉ có đăng nhập bằng Mã SV/Email do trường cấp phát.
