# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | ChatGPT | HTML/CSS/JS mock, launcher, smoke tests | Test tự động đã chạy; nhóm cần review code và nội dung | Nhóm kỹ thuật |
| Code parser, guardrails, validator (B3) | Claude Code | Viết 3 module, 32 unit test, tài liệu bàn giao và bản nháp spec §9 theo interface contract | Đã chạy 32 test và 77 test của nhóm (model giả lập), tự đối chiếu 24 câu benchmark; cần đọc hiểu các mẫu chặn và mã lỗi trước khi demo | Hoàng Văn Bảo |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | Coding Agent (Antigravity) | Viết `eval/preclass_stats.py` tổng hợp tỷ lệ sai KC (`answers.csv`) và tỷ lệ skip/chưa hoàn thành mini-lab (`events.csv`), trích phân bố số ca dạy từ `data/training-ops/*.xlsx` | Kiểm tra lại mẫu số theo cặp `(hv, lesson_id, lab_key)` (538 cặp mở, 96 chưa hoàn thành) thay vì chỉ đếm sự kiện thô (602 sự kiện mở); chạy tái lập 100% | Tạ Tiến Dũng |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Coding Agent (Antigravity) | Mở rộng `eval/benchmark.csv` thêm 9 câu `B16–B24` (giữ nguyên `B01–B15`), lập lưới độ phủ 5 chiều trong `eval/README.md` | Kiểm từng `source` (`nguoi_dung` 7, `data_that` 4, `tu_viet` 13) và `pass_criterion` đo được; chạy `python run.py check` 0 cảnh báo | Tạ Tiến Dũng |
| Grader tự động, rubric & cấu hình chi phí (T3/T4) | Coding Agent (Antigravity) | Viết `eval/auto_grader.py`, `tests/test_auto_grader.py`, `eval/human_rubric.md`, `eval/grading_sheet_template.csv`, `eval/calibration_kit.md`, `cost/personas.yaml`, `cost/cost-estimate.md` §1 | Kiểm 23 unit test kết hợp `interface-contract.md` v1.0, `oop_annotations.json` và `parser/guardrails/validator`; tách rõ phần code kiểm cấu trúc với phần người chấm ngữ nghĩa | Tạ Tiến Dũng |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
