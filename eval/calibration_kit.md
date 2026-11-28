# Bộ Chạy Thử & Hiệu Chuẩn 2 Người Chấm Độc Lập (T3-05)

> Trạng thái hiện tại: **CHƯA THỰC HIỆN CHẤM THẬT** (chờ output thật từ prompt/agent sau `M3-04` và thành viên chấm độc lập thứ 2 trong nhóm). Không bịa kết quả hay giả lập người chấm thứ 2.
> Nguyên tắc khóa CP2: khi thấy chênh lệch giữa 2 người chấm, chỉ làm rõ **cách áp dụng** tiêu chí trong `eval/human_rubric.md`, **KHÔNG sửa** ngưỡng khóa tại `spec.md` §7 hay `eval/metric_spec.yaml`.

## 1. Ghi nhận 10–20 output thử (theo guide 2.4 bước 1)

Sau khi có model thật (`D3-03` / `M3-04`), chạy thử 10–15 input đại diện từ `eval/benchmark.csv` (ưu tiên phủ đủ 5 lớp: `B01, B02, B03, B05, B06, B07, B08, B09, B10, B11, B13, B16, B18, B20, B22`) và ghi lại đánh giá thô:

| STT | Mã case | Model / Prompt nháp | Mức dùng được (dùng được / sửa được / không chấp nhận) | Lỗi thực tế quan sát được | Nhóm lỗi dự kiến |
|---|---|---|---|---|---|
| 1 | *(chờ chạy thật)* | | | | |

## 2. Quy trình hiệu chuẩn 2 người chấm độc lập trên 5 output (mục tiêu đồng thuận ≥4/5)

- **5 case mẫu cố định cho vòng hiệu chuẩn** (phủ đủ 5 dạng khó/thường/từ chối):
  1. `B01` (`kho`, Lớp 1 — mục tiêu ngoài nguồn `backpropagation`)
  2. `B05` (`kho`, Lớp 4 — lớp đông 200 người không thiết bị, 45 phút)
  3. `B07` (`kho`, Lớp 4 — đáp án quiz sai nhưng trích `A06` có vẻ thuyết phục)
  4. `B09` (`tu_choi`, Tấn công 1 — prompt injection `I02` đọc `.env`)
  5. `B13` (`thuong` — kịch bản chuẩn 60 phút bám slide `A01–A06`)
- **Người chấm 1 (Grader A):** Tạ Tiến Dũng → điền độc lập `eval/calibration_grader_a.csv` (không trao đổi trước khi khóa phiếu).
- **Người chấm 2 (Grader B):** Thành viên khác trong nhóm (Nguyễn Văn Minh / Hoàng Văn Bảo / Nguyễn Đức Đạt) → điền độc lập `eval/calibration_grader_b.csv`.
- **Kiểm độ đồng thuận tự động bằng lệnh:**
  ```bash
  python eval/auto_grader.py --agreement eval/calibration_grader_a.csv eval/calibration_grader_b.csv
  ```

## 3. Nhật ký kết quả hiệu chuẩn & xử lý chênh lệch

- **Ngày thực hiện:** *(chưa thực hiện)*
- **Tên 2 người chấm:** Grader A = Tạ Tiến Dũng · Grader B = *(chưa xác nhận)*
- **Kết quả khớp:** `__ / 5` (ngưỡng mục tiêu `>= 4/5`)
- **Ghi chép từng câu lệch và quy ước áp dụng thống nhất (không đổi chuẩn khóa CP2):**

| Case lệch | Grader A (`pass` + lý do) | Grader B (`pass` + lý do) | Quy ước áp dụng thống nhất trong `human_rubric.md` |
|---|---|---|---|
| *(chưa có)* | | | |
