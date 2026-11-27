# TeachFlow AI — Prototype Mock

Chạy python run.py hoặc mở codebase/prototype.html trực tiếp. Không cần server, framework, Internet hoặc API key.

1. Chọn bài mẫu hoặc dán nội dung đã trích xuất / đọc TXT, Markdown local.
2. Điền mục tiêu, thời lượng, trình độ, quy mô và thiết bị; xác nhận quyền dùng tài liệu.
3. Sinh kịch bản bằng mock quy tắc; xem timeline, nguồn và cảnh báo.
4. Sửa từng hoạt động, kiểm lại tổng phút; đánh dấu đã review và duyệt. Sửa đổi làm mất quyền xuất.
5. Xuất teaching-script.md/JSON (kịch bản chính), hoặc teaching-mode.html (HTML độc lập với CSS/JS nhúng). Teaching Mode có điều hướng, timer, tiến độ, nguồn, fallback, ẩn/hiện đáp án.

Kiểm thử: node tests/test_prototype.js (15 smoke test pass, bao gồm toàn dải 5–240 phút); đã chạy smoke test trình duyệt Edge headless với Playwright: tạo nháp, chặn export trước duyệt, duyệt, export và mở playbook offline, điều hướng, đánh dấu hoàn thành, sửa mất duyệt, không có page error. TEACHFLOW_NO_BROWSER=1 python run.py kiểm launcher không bật cửa sổ.

Giới hạn: mock tạo 4 phân đoạn theo quy tắc, chưa hiểu ngữ nghĩa nguồn/mục tiêu tổng quát, chưa cá nhân hóa sâu, chưa đọc PDF/PPTX trực tiếp. Phát hiện mâu thuẫn fixture và injection theo mẫu, không phải bộ lọc toàn diện. Danh mục chiến lược trong data là tài liệu thiết kế; mock dùng lựa chọn cố định, chưa gọi tool có tracing. Python answer, eval, simulate vẫn cần tích hợp thật ở CP3. Không có kết quả benchmark AI thật, không suy ra hiệu quả học tập. Chuẩn đạt và metric giữ nguyên.
