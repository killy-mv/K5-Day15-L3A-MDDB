# TeachFlow AI — Studio local CP3

Chạy `python run.py` từ repo; mở http://127.0.0.1:8765/ nếu trình duyệt không tự mở. Ctrl+C để tắt. Có thể đổi port bằng TEACHFLOW_PORT; TEACHFLOW_NO_BROWSER=1 chỉ tắt tự mở trình duyệt, không tắt server. CLI: `python codebase/app.py --cli`, nhập LessonRequest JSON.

Studio mới (codebase/studio.html) gọi GET /api/health, GET /api/lessons và POST /api/generate trên cùng origin. Backend chỉ bind 127.0.0.1, không cần framework, không gửi key sang browser. Chọn OOP hoặc fixture cũ; nguồn cố định chỉ đọc, chọn mã nguồn nếu cần. Custom chỉ đọc TXT/MD hoặc dán text; xác nhận quyền sử dụng. Chưa có parser PDF/PPTX trực tiếp.

Giảng viên sửa và duyệt bản nháp, xuất Markdown/JSON hoặc mở cửa sổ riêng đọc kịch bản đã duyệt. Cửa sổ có timer, tiến độ, điều hướng, lời dẫn, tham chiếu và đáp án; sửa kịch bản đóng cửa sổ và hủy duyệt. Nếu popup bị chặn thì đọc tại chỗ. Slide gốc vẫn chiếu cho học viên, không tạo slide mới. Prototype HTML offline CP2 cũ giữ nguyên để tái lập mốc, không phải luồng sản phẩm hiện tại.

Agent dùng contract_mock khi TEACHFLOW_MODE=mock (mặc định nếu MODEL_PROVIDER=fake), dùng module thật khi TEACHFLOW_MODE=real hoặc provider khác fake. Chưa có module thật của Đạt/Bảo; real mode sẽ báo lỗi thay vì tự chuyển mock. Một lần gọi generator, không repair ở orchestration hiện tại; cần kiểm chứng giới hạn 5 quyết định/2 repair và trace token sau tích hợp. Mock chỉ sinh khung đơn giản, không có chấm ngữ nghĩa hoặc kết quả eval thật.

Kiểm thử:
- python -m unittest discover -s tests -p "test_local_studio.py" -v (12/12 pass).
- python tests/browser_studio_smoke.py (Playwright + Edge cài local; tùy chọn, đã pass luồng API/duyệt/popup/timer/export/sửa hủy duyệt/hỏi lại).
- python -m unittest discover -s tests -p "test_contract_mock.py" -v
- node tests/test_prototype.js (prototype CP2).
