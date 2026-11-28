# TeachFlow AI — Studio local CP3

Chạy `python run.py` từ repo; mở http://127.0.0.1:8765/ nếu trình duyệt không tự mở. Ctrl+C để tắt. Có thể đổi port bằng TEACHFLOW_PORT; TEACHFLOW_NO_BROWSER=1 chỉ tắt tự mở trình duyệt, không tắt server. CLI: `python codebase/app.py --cli`, nhập LessonRequest JSON.

Studio mới (codebase/studio.html) gọi GET /api/health, GET /api/lessons và POST /api/generate trên cùng origin. Backend chỉ bind 127.0.0.1, không cần framework, không gửi key sang browser. Chọn OOP hoặc fixture cũ; nguồn cố định chỉ đọc, chọn mã nguồn nếu cần. Custom chỉ đọc TXT/MD hoặc dán text; xác nhận quyền sử dụng. UI chưa đọc trực tiếp PDF/PPTX; parser của Bảo hỗ trợ PDF có text qua CLI tùy chọn pypdf (không OCR), xem docs/parser-validator-guardrails.md.

Giảng viên sửa và duyệt bản nháp, xuất Markdown/JSON hoặc mở cửa sổ riêng đọc kịch bản đã duyệt. Cửa sổ có timer, tiến độ, điều hướng, lời dẫn, tham chiếu và đáp án; sửa kịch bản đóng cửa sổ và hủy duyệt. Nếu popup bị chặn thì đọc tại chỗ. Slide gốc vẫn chiếu cho học viên, không tạo slide mới. Prototype HTML offline CP2 cũ giữ nguyên để tái lập mốc, không phải luồng sản phẩm hiện tại.

Agent dùng contract_mock khi TEACHFLOW_MODE=mock (mặc định nếu MODEL_PROVIDER=fake), dùng module thật khi TEACHFLOW_MODE=real hoặc provider khác fake. Parser/guardrails/validator của Bảo đã có trên main; còn thiếu AI Core của Đạt; real mode sẽ báo lỗi thay vì tự chuyển mock. Một lần gọi generator, không repair ở orchestration hiện tại; cần kiểm chứng giới hạn 5 quyết định/2 repair và trace token sau tích hợp. Mock chỉ sinh khung đơn giản, không có chấm ngữ nghĩa hoặc kết quả eval thật.

Kiểm thử:
- python -m unittest discover -s tests -p "test_local_studio.py" -v (12/12 pass).
- python tests/browser_studio_smoke.py (Playwright + Edge cài local; tùy chọn, đã pass luồng API/duyệt/popup/timer/export/sửa hủy duyệt/hỏi lại).
- python -m unittest discover -s tests -p "test_contract_mock.py" -v
- node tests/test_prototype.js (prototype CP2).

M3-05: loading có thời gian chờ và khóa gửi trùng; kết quả cũ bị bỏ khi đổi context. UI kiểm schema, timeline khớp yêu cầu, nguồn đúng phạm vi, mẫu HTML/script và metadata tự duyệt; lỗi hiện ngay khi sửa. Regex không thay kiểm ngữ nghĩa.

- node tests/test_studio.js: 23 case kiểm validation studio.
- python tests/browser_studio_complex.py: fixture giả lập 4 hoạt động dài, popup/navigation, JSON, sửa không an toàn, response lỗi/thiếu metadata, provider 503 và response cũ.
- python tests/smoke_real_studio.py --run-real: chỉ chạy sau khi AI Core và .env sẵn sàng; 2 case B11/B05 qua answer(), yêu cầu trace model/token/tool thật, tối đa 5 call/case; không ghi Run 1, không mock fallback. Chưa chạy real; repair và ngữ nghĩa cần đối chiếu riêng.
