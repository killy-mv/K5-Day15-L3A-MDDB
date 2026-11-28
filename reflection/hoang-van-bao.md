# Reflection — Hoàng Văn Bảo

1. **Vai trò và phần tôi phụ trách**

   Tôi phụ trách lớp kiểm tra an toàn của TeachFlow AI, gồm parser, guardrails và validator (B3-01 đến B3-10, B4-01, B4-02). `codebase/parser.py` chuẩn hóa tài liệu bài giảng thành các đoạn nguồn có mã. `codebase/guardrails.py` kiểm tra yêu cầu trước khi gọi model: hỏi lại khi thiếu thông tin lớp, từ chối các yêu cầu ngoài phạm vi như chấm điểm, tự duyệt, đọc dữ liệu bí mật hay làm theo chỉ dẫn nằm trong slide. `codebase/validator.py` kiểm tra kịch bản do model sinh ra về cấu trúc, thời lượng, mã nguồn và nội dung HTML. Tôi viết bộ kiểm thử `tests/test_bao_modules.py`, công cụ `tests/guardrails_report.py`, tài liệu bàn giao `docs/parser-validator-guardrails.md`, báo cáo `docs/guardrails-results.md` và mục §9 của spec. Phần code CP3 đã được merge qua PR #5.

2. **AI hỗ trợ tôi như thế nào**

   Tôi dùng Claude Code để đọc interface contract, viết ba module cùng 32 unit test, chạy đối chiếu với 24 câu benchmark và với AI thật (Gemini). Tôi cũng dùng nó để viết công cụ báo cáo guardrails và một bộ 15 câu tự đặt nhằm thử lách bộ lọc; kết quả đúng 9/15 được ghi lại đầy đủ thay vì sửa để che lỗi. Mẫu chặn dữ liệu bí mật ban đầu chặn nhầm câu hợp lệ "không dán API key vào code", nên phải thu hẹp lại. Khi AI đề xuất dùng các agent đóng vai người dùng, tôi chỉ giữ kết quả đó như một bản rà soát giao diện có ghi rõ nguồn, không tính là người dùng thử thật.

3. **Một câu thử trượt của nhóm và bài học**

   Ở Run 1, câu B18 trượt dù logic xử lý không sai: Gemini trả lỗi HTTP 429 do hết hạn mức gọi miễn phí, output rỗng nên câu bị tính trượt. Cùng lượt, sáu câu khác (B01, B02, B05, B06, B11, B12) trượt vì lỗi HTTP 503 khi Gemini quá tải. Tôi đã gặp lỗi 503 khi tự chạy thử guardrails với AI thật trước đó, nhưng `ai.py` vẫn chưa có cơ chế tự thử lại khi nhóm chạy lượt chính thức. Bài học của tôi là khi phát hiện rủi ro, cần chuyển nó thành việc cụ thể cho người phụ trách và theo dõi đến khi được xử lý, không chỉ ghi nhận trong tài liệu. Run 1 cũng cho thấy lợi ích của việc chặn sớm bằng code: bốn câu cần từ chối (B08, B09, B10, B24) bị guardrails chặn trước khi gọi model, nên không tốn lượt gọi và không bị ảnh hưởng bởi lỗi 503/429.
