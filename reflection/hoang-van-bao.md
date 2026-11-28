# Reflection — Hoàng Văn Bảo

<!-- Bảo đọc lại, sửa theo ý mình và viết câu 3 sau khi có Run 1. Xóa dòng này trước khi nộp. -->

1. **Vai trò và phần mình làm:** Trong nhóm mình lo phần kiểm tra an toàn, gồm parser, guardrails và validator (B3-01 đến B3-10, B4-02).
   - Parser (`codebase/parser.py`) đọc tài liệu bài giảng và chia thành các đoạn có mã.
   - Guardrails (`codebase/guardrails.py`) chạy trước khi gọi model. Thiếu thông tin lớp thì hỏi lại. Nếu bị yêu cầu chấm điểm, tự duyệt, đọc file bí mật, đăng lên LMS hay làm theo chỉ dẫn trong slide thì từ chối.
   - Validator (`codebase/validator.py`) kiểm lại kịch bản model trả về: đủ trường chưa, thời gian có khớp không, mã nguồn có thật không, có chèn HTML không.
   - Mình viết test trong `tests/test_bao_modules.py`, tài liệu bàn giao `docs/parser-validator-guardrails.md` và phần §9 trong spec. Code nằm trong PR #5.

2. **AI hỗ trợ mình thế nào:** Mình dùng Claude Code để đọc interface contract, viết ba module và 32 test, rồi chạy thử với 24 câu benchmark.
   - Lần đầu AI sửa lấn sang `tools.py`, `agent.py` và `app.py` của các bạn khác. Khi nhóm chốt contract, mình phải cất bản đó đi và làm lại cho đúng phần của mình.
   - Mẫu chặn bí mật lúc đầu bắt nhầm cả câu bình thường "không dán API key vào code", nên phải sửa cho hẹp lại.
   - Mình cũng kiểm tra để chắc 131 đoạn của bài OOP không bị bắt nhầm là tấn công.
   - *(Thêm chỗ mình tự sửa hoặc tự quyết định.)*

3. **Một câu thử trượt của nhóm và mình học được gì:** *(Viết sau Run 1. Ghi mã câu trượt thật, output sai ra sao, lỗi nằm ở guardrail, generator hay validator, và đã sửa gì hoặc vì sao chưa sửa.)*
