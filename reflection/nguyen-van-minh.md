# Reflection — Nguyễn Văn Minh (2A202603551)

**1. Vai trò và phần mình làm**

Tôi là đội trưởng nhóm MDDB, phụ trách điều phối, kiến trúc và tích hợp TeachFlow AI.
Tôi xây dựng interface contract, backend Python và giao diện Planning/Teaching Mode, kết nối các module của Đạt và Bảo qua `agent.answer()`.
Tôi tổng hợp bằng chứng P1–P3, ước tính impact, cập nhật `spec.md`, kiểm tra PR, chạy smoke thật và quay video nộp CP3.
Các phần chính nằm ở `codebase/backend.py`, `codebase/agent.py`, `codebase/studio.html`, `docs/interface-contract.md`, `evidence/summary.md`; PR #12–#14 ghi nhận tích hợp và tiến độ.

**2. AI hỗ trợ mình thế nào**

Tôi dùng ChatGPT để soạn code, rà schema, viết test, tổng hợp tài liệu, chuẩn bị slide và bản nháp reflection.
Khi tích hợp, tôi yêu cầu bổ sung kiểm tra timeline, mã nguồn, trạng thái chờ duyệt và hủy duyệt khi người dùng sửa nội dung; không coi fixture là kết quả AI thật.
Phần evidence được đối chiếu với ghi chép và trích dẫn tôi cung cấp; số phút impact chỉ là ước tính, không phải số đo tiết kiệm.
Hai smoke thật B11/B05 và browser smoke được ghi riêng tại `docs/real-smoke-20261128.md`; không lấy chúng thay cho điểm benchmark.

**3. Một câu thử trượt của nhóm và bài học**

B11 yêu cầu kịch bản hướng dẫn lab 60 phút cho 35 học viên; Run 1 bị HTTP 503 từ Gemini, output rỗng dù smoke tích hợp riêng từng thành công.
Tôi nhận ra một demo chạy được không đồng nghĩa với hệ thống đủ tin cậy: lỗi nhà cung cấp vẫn làm người dạy không nhận được kịch bản trước giờ lên lớp.
Cần retry có giới hạn, phân biệt quota với lỗi tạm thời, báo lỗi rõ và kiểm thử lại toàn bộ 24 câu bằng cùng chuẩn CP2.
Kết quả Run 1 là 16/24; tôi giữ nguyên các câu trượt và trace thay vì bỏ lỗi để làm đẹp điểm (`eval/run-1.csv`, `eval/report.md`, `traces/run-1.jsonl`).
