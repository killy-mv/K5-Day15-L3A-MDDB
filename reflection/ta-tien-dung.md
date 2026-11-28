# Reflection — Tạ Tiến Dũng

<!-- Dũng đọc lại, điều chỉnh theo ý mình và điền câu 3 ngay sau khi có kết quả Run 1 thật. Xóa dòng chú thích này trước khi nộp bản cuối 23:59. -->

1. **Vai trò và phần mình làm:** Trong nhóm mình phụ trách Benchmark, Đánh giá (Evaluation) và Mô phỏng chi phí (`T3-01` đến `T3-11`, `T4-01` đến `T4-06`, `F-04`, `F-08`).
   - Mở rộng bộ câu thử `eval/benchmark.csv` từ 15 lên 24 câu (giữ nguyên `B01–B15`, bổ sung `B16–B24`), lập lưới độ phủ 5 chiều và khóa trước tập 12 case mong đợi kịch bản hoàn chỉnh trong `eval/README.md`, đồng bộ `data/DATA_CARD.md`.
   - Viết `eval/preclass_stats.py` tái lập các chỉ số lỗi KC và tỷ lệ bỏ qua bước thực hành từ `data/preclass/` để làm căn cứ `data_that` cho `B16–B18, B21`.
   - Xây dựng grader tự động `eval/auto_grader.py` kèm 23 unit test trong `tests/test_auto_grader.py` (tương thích `docs/interface-contract.md` v1.0, `data/lessons/oop_annotations.json` và module của Bảo), bộ rubric & phiếu chấm người `eval/human_rubric.md`, `eval/grading_sheet_template.csv`, cùng bộ hiệu chuẩn 2 người chấm `eval/calibration_kit.md`.
   - Chuẩn hóa `cost/personas.yaml` và `cost/cost-estimate.md` §1 với 3 persona đúng vai giảng viên/lab coach (`share = 1.00`), quy mô `22 / 84 / 168` người và 3 tầng giá model từ `further-reading/model-prices.md`.

2. **AI hỗ trợ mình thế nào:** Mình dùng Coding Agent để phân tích thống kê `data/preclass/` và `data/training-ops/`, soạn các câu thử bổ sung `B16–B24`, viết `eval/auto_grader.py`, unit test và tài liệu rubric.
   - Khi thống kê `data/preclass/events.csv`, lần đếm đầu tiên chỉ lấy hiệu số sự kiện thô (`602` lượt `lab_opened` trừ `453` lượt `lab_completed` = `149/602`), dễ bị lệch vì một học viên có thể mở cùng một bài lab nhiều lần. Mình phải sửa lại `eval/preclass_stats.py` để đếm theo đúng mẫu số là cặp duy nhất `(hv, lesson_id, lab_key)` (`96/538 = 17.8%` chưa hoàn thành) rồi mới đưa vào `B21`.
   - Khi nhóm cập nhật `docs/interface-contract.md` v1.0 và thêm bộ bài giảng `oop_annotations.json` (131 trang) cùng lọc `source_refs`, mình cập nhật lại `eval/auto_grader.py` để kiểm đúng tập `source_refs` được cấp thay vì chấp nhận mọi mã trong toàn bài, đồng thời gắn cờ phát hiện `generation_mode="mock"` để không bao giờ chấm nhầm output giả lập thành điểm eval thật.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:** *(Viết sau khi chạy Run 1 với model thật. Ghi rõ mã câu thử trượt trong `eval/run-1.csv`, input/output thực tế, nguyên nhân trượt đối chiếu `eval/metric_spec.yaml` và `traces/run-1.jsonl`, cùng bài học rút ra khi thiết kế tiêu chí chấm và cải tiến sang Run 2.)*
