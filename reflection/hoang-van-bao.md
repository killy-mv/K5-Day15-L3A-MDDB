# Reflection — Hoàng Văn Bảo

> BẢN NHÁP do AI soạn từ phần việc trong repo. Bảo cần đọc, sửa lại bằng lời của mình và điền câu 3 sau khi có Run 1, trước 23:59 ngày 28/11.

1. **Vai trò và phần mình làm:** Mình phụ trách lớp kiểm tra an toàn của TeachFlow: parser, guardrails và validator (B3-01 → B3-10, B4-02).
   - `codebase/parser.py` chuẩn hóa nguồn bài giảng thành các đoạn có mã.
   - `codebase/guardrails.py` hỏi lại khi thiếu context, và từ chối khi yêu cầu chấm điểm, tự duyệt, đọc bí mật, đăng LMS hoặc làm theo chỉ dẫn nằm trong slide. Phần này chạy trước khi gọi model.
   - `codebase/validator.py` kiểm schema, timeline, mã nguồn và HTML trong kịch bản mà model sinh ra.
   - Test nằm ở `tests/test_bao_modules.py`, tài liệu bàn giao ở `docs/parser-validator-guardrails.md`, và mình viết spec §9.
   - Commit: *(điền sau khi commit)*.

2. **AI hỗ trợ mình thế nào:** Mình dùng Claude Code để đọc interface contract và viết ba module cùng 32 unit test, rồi đối chiếu hành vi với 24 câu benchmark.
   - Bản đầu sửa lấn sang `tools.py`, `agent.py` và `app.py` của bạn khác. Khi nhóm chốt contract, mình phải cất bản đó vào stash và viết lại cho đúng phần mình phụ trách.
   - Regex chặn bí mật lúc đầu bắt nhầm câu vô hại "không dán API key vào code", nên phải thu hẹp lại.
   - Mình kiểm tra thêm để chắc 131 đoạn OOP không bị bắt nhầm là injection.
   - *(Bảo bổ sung chỗ tự sửa hoặc tự quyết định.)*

3. **Một câu thử trượt của nhóm và bài học:** *(Chờ Run 1. Ghi id câu trượt thật, output sai thế nào, lỗi nằm ở lớp nào: guardrail, generator hay validator, và đã sửa gì hoặc vì sao chưa sửa. Không bịa.)*
