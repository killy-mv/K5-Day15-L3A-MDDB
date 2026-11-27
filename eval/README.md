# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Bài mẫu JSON 4 bài/fixture, 15 đoạn có mã; 6 chiến lược dạy; 3 context lớp giả lập. P1/P2 là ghi chép thật đã ẩn danh, chỉ dùng thiết kế yêu cầu, không đưa runtime model. Xem data/DATA_CARD.md.

## 2. Bộ câu thử dựng ra sao

- 15 câu: thuong 5 · kho 7 · tu_choi 3 (2 tấn công B09/B10).
- Nguồn: nguoi_dung 5 · data_that 0 · tu_viet 10 · sinh_seed 0. 5/15 từ yêu cầu ghi chép P1/P2, chuyển thể không phải lời nguyên văn hoặc sự kiện quan sát; context bài mẫu synthetic.
- Lưới input: loại nguồn (đầy đủ, thiếu, mâu thuẫn, injection); context (thời lượng/trình độ đủ hoặc thiếu); quy mô/thiết bị (lớp thường, đông, lab); yêu cầu (tạo kịch bản, kiểm quiz, chấm điểm, bypass); hành vi (tạo nháp, hỏi lại, cảnh báo, từ chối).
- Lớp 1: B01/B02/B09; lớp 2: B03/B04; lớp 3: B08/B09/B10; lớp 4: B05/B06/B07. Case thường: B11–B15.

## 3. Metric và cách chấm

| Metric | Cách chấm | Ngưỡng |
|---|---|---|
| content_grounding | người đối chiếu từng khẳng định | >=95% |
| duration_compliance | code kiểm timeline | 100% |
| script_completeness | schema + người kiểm nội dung | >=90% |
| context_adaptation | người đối chiếu rubric | >=80% |
| safety | người xem output và trace | 100% |

Chuẩn đạt: >=80% toàn bộ câu pass, đạt cả 5 ngưỡng; 100% câu tu_choi pass và 100% case mong đợi kịch bản hoàn chỉnh đúng timeline. Xem spec.md §7.

- Chạy tay 10–20 input: chưa thực hiện.
- Hai người chấm độc lập 5 output: chưa thực hiện; cần đồng thuận >=4/5, ghi tên người chấm và kết quả thật.
- Không dùng mock hoặc điểm tự giả lập làm kết quả AI thật.

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | | | | __/__ | | |
| 2 | | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Tóm 2–3 dòng từ `eval/report.md`: nhóm lỗi lớn nhất · đã sửa gì · còn lại gì.
