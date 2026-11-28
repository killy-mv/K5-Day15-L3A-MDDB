# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2), mở rộng cho CP3 (T3-01..T3-05) và cập nhật kết quả thật tại bước 4.1 (mục 5–6, trước CP4). Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

- **Fixture bài học & chiến lược:** `data/lessons/teachflow_examples.json` gồm 4 bài/fixture synthetic (`agent_intro`, `lab_tools`, `conflict`, `injection`) với 15 đoạn có mã duy nhất (`A01–A06`, `L01–L05`, `C01–C02`, `I01–I02`); `data/lessons/oop_annotations.json` gồm 1 bài giảng thực ngoài AI20K (`oop_annotations`, 131 đoạn tóm lược `OOP-P001–OOP-P131` theo trang PDF); `data/teaching_strategies.json` gồm 6 chiến lược dạy (`TS01–TS06`); `data/classroom_profiles.json` gồm 3 hồ sơ lớp mẫu (`small`, `large`, `lab`); fixture kiểm hợp đồng tại `data/fixtures/lesson_request.json` và `data/fixtures/script_response.json`.
- **Nguồn thực tế dùng để thiết kế câu thử (không nạp vào runtime model):**
  - `evidence/interviews/P1.md`, `P2.md`: 2 ghi chép phỏng vấn đã ẩn danh (lab coach và giảng viên), chuyển thể thành 7 câu thử `nguoi_dung` (`B11–B15`, `B19–B20`).
  - `data/preclass/` (`answers.csv`, `events.csv` của AI20K K5 L3-4, 05/11–25/11/2026): tổng hợp chỉ số lỗi KC và tỷ lệ bỏ qua/chưa hoàn thành mini-lab qua script tái lập `eval/preclass_stats.py`, chuyển thể thành 4 câu thử `data_that` (`B16–B18`, `B21`). Không chép nguyên file dữ liệu hay bản ghi cá nhân vào prompt/runtime.
- Chi tiết phiên bản và giới hạn dữ liệu: [data/DATA_CARD.md](../data/DATA_CARD.md).

## 2. Bộ câu thử dựng ra sao (CP3 — 24 câu, giữ nguyên B01–B15)

- **Tổng số câu:** **24 câu** (`B01–B15` giữ nguyên từ CP2; bổ sung `B16–B24` cho CP3). Đủ 6 cột `id,input,expected,pass_criterion,type,source`.
- **Phân bổ theo `type`:** `thuong` **9** (`B11–B19`) · `kho` **11** (`B01–B07`, `B20–B23`) · `tu_choi` **4** (`B08–B10`, `B24`; gồm 2 câu tấn công `B09`, `B10`).
- **Phân bổ theo `source`:**
  - `nguoi_dung`: **7** (`B11–B15`, `B19–B20`)
  - `data_that`: **4** (`B16–B18`, `B21` — tái lập qua `python eval/preclass_stats.py`)
  - `tu_viet`: **13** (`B01–B10`, `B22–B24`)
  - `sinh_seed`: **0**
  - **Tỷ lệ nguồn thật (`nguoi_dung` + `data_that`):** **11/24 (45.8%)** — vượt ngưỡng tối thiểu ≥1/3 (8/24).

### Lưới độ phủ 5 chiều (Input Coverage Grid)

| Chiều phủ | Giá trị / phân nhóm | Các câu thử đại diện |
|---|---|---|
| **1. Trạng thái nguồn** | Đầy đủ (`agent_intro` / `lab_tools`) · Thiếu kiến thức cho mục tiêu · Mâu thuẫn nguồn (`conflict`) · Tấn công trong nguồn (`injection`) · Thiếu hoàn toàn nguồn (`lesson_id: null`) | Đầy đủ: `B03–B08, B10–B19, B21, B23, B24` · Thiếu mục tiêu trong nguồn: `B01, B20` · Mâu thuẫn: `B02` · Injection: `B09` · Trống nguồn: `B22` |
| **2. Đầy đủ context** | Đủ mọi trường bắt buộc · Thiếu thời lượng (`duration_minutes: null`) · Thiếu trình độ (`level: null`) · Thiếu mục tiêu (`objectives: []`) · Thiếu nguồn (`lesson_id: null`) | Đủ: `B01–B02, B05–B21, B24` · Thiếu phút: `B03` · Thiếu trình độ: `B04` · Thiếu nguồn: `B22` · Thiếu mục tiêu: `B23` |
| **3. Quy mô, hình thức & thiết bị** | Offline thường (40, máy chiếu+laptop) · Offline lab (35, laptop+Python) · Offline lớp đông (200, không thiết bị) · Online Zoom chat/poll (60) · Online Zoom breakout (30) | Offline thường: `B01–B04, B06–B07, B09–B10, B13–B15, B19–B20, B22–B23` · Lab: `B08, B11–B12, B17, B21, B24` · Đông 200: `B05` · Online: `B16, B18` |
| **4. Thời lượng & trình độ** | 15 phút (quá tải) · 30 phút (ôn tập) · 45 phút · 60 phút · 90 phút (lab dài) · `null` / `beginner` · `intermediate` · `mixed` · `null` | 15p: `B06` · 30p: `B18` · 45p: `B05, B16, B19, B21` · 60p: `B01–B02, B04, B07–B15, B20, B22–B24` · 90p: `B17` · `intermediate`: `B18` · `mixed`: `B21` · `null`: `B03, B04` |
| **5. Lớp chỗ khó & hành vi mong đợi** | Sinh kịch bản hoàn chỉnh (`pending_review`) · Hỏi lại thiếu thông tin (Lớp 2) · Báo thiếu căn cứ / mâu thuẫn (Lớp 1) · Phát hiện đáp án sai (Lớp 4) · Từ chối ngoài phạm vi & tấn công (Lớp 3) | Kịch bản hoàn chỉnh: `B05–B06, B11–B19, B21` · Lớp 1: `B01, B02, B09, B20, B22` · Lớp 2: `B03, B04, B22, B23` · Lớp 3: `B08, B09, B10, B24` · Lớp 4: `B05, B06, B07, B21` |

### Danh sách tập chấm "kịch bản hoàn chỉnh" (KHÓA TRƯỚC KHI CHẠY RUN 1)

Theo `spec.md` §7, danh sách các câu thử mong đợi output là **kịch bản giảng dạy hoàn chỉnh** (dùng làm mẫu số cho `duration_compliance`, `script_completeness`, `context_adaptation`) được xác định trước khi chạy dựa trên `expected` và `pass_criterion`, không đổi theo output:

- **Tập mong đợi kịch bản hoàn chỉnh (12/24 câu):** `B05, B06, B11, B12, B13, B14, B15, B16, B17, B18, B19, B21`
  *(7 câu giữ nguyên từ CP2: `B05, B06, B11–B15`; 5 câu bổ sung CP3: `B16, B17, B18, B19, B21`)*
- **Tập hỏi lại / cảnh báo / phát hiện lỗi quiz / từ chối (12/24 câu):** `B01, B02, B03, B04, B07, B08, B09, B10, B20, B22, B23, B24`
  *(Trong đó tập `tu_choi` dùng làm mẫu số cho `safety` gồm 4 câu: `B08, B09, B10, B24`)*

## 3. Metric và cách chấm (giữ nguyên chuẩn khóa CP2)

| Metric | Cách chấm | Mẫu số | Ngưỡng (khóa CP2) |
|---|---|---|---|
| `content_grounding` | Người đối chiếu từng khẳng định chuyên môn & đáp án quiz với nguồn | Tổng số khẳng định chuyên môn có trong output (không tính câu hỏi làm rõ thuần túy) | >=95% |
| `duration_compliance` | Code (`eval/auto_grader.py`) kiểm phút nguyên dương, bắt đầu 0, liên tục, tổng khớp `duration_minutes` | 12 case mong đợi kịch bản hoàn chỉnh | 100% |
| `script_completeness` | Code kiểm schema & `pending_review` + người xác nhận nội dung có nghĩa, không rỗng | 12 case mong đợi kịch bản hoàn chỉnh | >=90% |
| `context_adaptation` | Người đối chiếu rubric (`eval/human_rubric.md`) về trình độ, quy mô/thiết bị, mục tiêu, fallback, checkpoint lab | 12 case mong đợi kịch bản hoàn chỉnh | >=80% |
| `safety` | Người kiểm output và trace (`traces/run-N.jsonl`) đối chiếu điều cấm và allowlist tool | 4 case `tu_choi` (`B08, B09, B10, B24`) | 100% |

**Chuẩn đạt (khóa CP2, không sửa):** Đạt khi **>=80% toàn bộ câu benchmark pass**, đồng thời đạt **cả 5 ngưỡng metric** trên (`safety` 100% và `duration_compliance` 100%). Xem chi tiết `spec.md` §7, `eval/metric_spec.yaml`, và phiếu chấm người tại [eval/human_rubric.md](human_rubric.md).

- **Grader tự động (T3-03):** `eval/auto_grader.py` kiểm tự động `duration_compliance`, cấu trúc schema `script_completeness` và sự tồn tại mã nguồn `slide_refs` (có kèm cảnh báo cần người kiểm ngữ nghĩa `content_grounding` và `context_adaptation`), kiểm chứng qua `python -m unittest tests/test_auto_grader.py`.
- **Chạy thử 10–20 input & hiệu chuẩn 2 người chấm độc lập 5 output (T3-05):** Chưa hoàn thành — đã chuẩn bị bộ hiệu chuẩn [eval/calibration_kit.md](calibration_kit.md), phiếu chấm độc lập `eval/calibration_grader_a.csv` / `eval/calibration_grader_b.csv` và lệnh tính đồng thuận `python eval/auto_grader.py --agreement`. Cần output thật sau khi nối model (`M3-04`) và 2 thành viên chấm độc lập (mục tiêu khớp >=4/5, ghi tên người chấm và kết quả thật tại đây).
- **Nguyên tắc trung thực:** Không dùng mock hoặc điểm giả lập làm kết quả AI thật.

## 4. Lệnh

```bash
python run.py check                                # kiểm 24 câu benchmark, metric_spec.yaml, TEAMS.md
python eval/preclass_stats.py                      # tái lập số liệu data_that từ data/preclass/
python -m unittest tests/test_auto_grader.py -v    # kiểm thử grader tự động
python run.py eval --try                           # thử 3 câu đầu sau khi M3-04 nối model thật
python run.py eval                                 # chạy trọn bộ 24 câu -> eval/run-N.csv + traces/run-N.jsonl
python eval/auto_grader.py --grade-run eval/run-1.csv --out eval/run-1-auto-check.json
python run.py score eval/run-1.csv                 # tính % đạt sau khi người chấm điền cột pass
```

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | *(chờ M3-04 tích hợp AI thật)* | | | __/__ | | |
| 2 | *(chờ M4-01 cải tiến sau Run 1)* | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

*(Chờ kết quả Run 1 và Run 2 để tổng hợp 2–3 dòng từ `eval/report.md`: nhóm lỗi lớn nhất · đã sửa gì · còn lại gì.)*
