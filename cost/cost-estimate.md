# Chi phí khi dùng thật — TeachFlow AI

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Chấm ở rubric R6.
> Số mô phỏng **KHÔNG điền tay**: chỉ điền mục 2 sau khi chạy `python run.py simulate --rate-from eval/run-2.csv` qua agent gọi AI thật và chép nguyên bảng từ `cost/simulate-N-summary.md`.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí chuẩn** (USD / 1M token).

## 1. Đầu vào (đã chuẩn hóa tại `cost/personas.yaml`)

- **Persona (`cost/personas.yaml` — tổng `share = 1.00`, đúng vai giảng viên & lab coach):**
  1. `giang_vien_thinh_giang` (`share = 0.40`): `3` phiên/tháng, `2` lượt hỏi/phiên — tham chiếu nhóm nhận `<=4` buổi/ca trong `data/training-ops/` (7/14 GV + 21/62 lab coach = 28/76 ≈ 37%, làm tròn 0.40); tần suất phiên và lượt hỏi *(tự ước tính)*.
  2. `lab_coach_chinh` (`share = 0.45`): `6` phiên/tháng, `2` lượt hỏi/phiên — tham chiếu nhóm nhận `5–8` buổi/ca trong `data/training-ops/` (trung vị 6 ca/khóa 21 ngày≈1 tháng; kết hợp ghi chép P1 muốn dùng kịch bản khi dạy lab); tỷ lệ chia & lượt hỏi *(tự ước tính)*.
  3. `giang_vien_chu_chot` (`share = 0.15`): `10` phiên/tháng, `3` lượt hỏi/phiên — tham chiếu nhóm nhận `>=9` buổi/ca trong `data/training-ops/` (3/14 GV nhận 10–11 buổi + 6/62 coach nhận 9–10 ca; kết hợp ghi chép P2 tốn công chuẩn bị ví dụ/câu hỏi); tỷ lệ chia & lượt hỏi *(tự ước tính)*.
  - *Lưu ý minh bạch:* `data/training-ops/` là bảng lịch giả lập theo cấu trúc khóa AI20K thật (`data/training-ops/README.md`).
- **Số người dùng thật đúng vai (3 kịch bản, KHÔNG lấy 700 học viên làm giảng viên):**
  - **Thấp:** `22` người (chỉ nhóm giảng viên đứng lớp chính của 1 khóa — tham chiếu `data/training-ops/README.md`, mức áp dụng thấp *(tự ước tính)*).
  - **Cơ sở:** `84` người (`22` giảng viên + `62` lab coach của 1 khóa AI20K theo cấu trúc `data/training-ops/README.md`).
  - **Cao:** `168` người (quy mô mở rộng 2 khóa song song / nhiều chương trình đào tạo cùng cỡ *(tự ước tính)*).
- **Giá 4 mức model (nguồn: `further-reading/model-prices.md`, BTC kiểm tra trên trang chính thức ngày `25/11/2026`, đơn vị USD / 1M token, giá standard):**
  - **Tầng Nhỏ (model đo thật Lượt 2 & Simulate 50 phiên):** `gemini-3.1-flash-lite` — vào `$0.25`, ra `$1.50` ([Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing), xem 25/11/2026).
  - **Tầng Vừa (model đo thật Lượt 1):** `gemini-3.8-flash` — vào `$1.50`, ra `$7.50` ([Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing), xem 25/11/2026; dùng giá từ 01/01/2027 theo đúng chỉ dẫn ở `further-reading/model-prices.md`).
  - **Tầng Vừa (đối chiếu liên hãng):** `gpt-6.1-terra` — vào `$1.00`, ra `$5.00` ([OpenAI Pricing](https://developers.openai.com/api/docs/pricing), xem 25/11/2026).
  - **Tầng Lớn:** `gemini-4-hydrogen` — vào `$1.50`, ra `$7.50` ([Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing), xem 25/11/2026).
- **Tỉ lệ đạt dùng để tính:** **`22/24 (92% / 91,7%)`** từ kết quả chấm thực tế Lượt 2 `eval/run-2.csv` (`run-2@20261128-135219` — **KHÔNG mặc định 100%**).
- **Ghi chú đo token:** Token được **đo thực tế trên `gemini-3.1-flash-lite`** (qua `cost/simulate-1.csv`, `traces/simulate-1.jsonl`), sau đó áp bảng giá của từng model (`gemini-3.1-flash-lite`, `gemini-3.8-flash`, `gpt-6.1-terra`, `gemini-4-hydrogen`); lưu ý model khác hãng (`gpt-6.1-terra`) có bộ tách token khác nên số token thực tế có thể lệch nhẹ.

## 2. Kết quả mô phỏng

### 2.1 Kết quả chạy thử 10 phiên ở CP3 (`T3-11` — `python run.py simulate --try --wait 12 --rate-from eval/run-1.csv`)

- **Run ID:** `simulate-try@20261128-100812` · **Số phiên:** `10/10` phiên thành công (`0/10` phiên lỗi) · **Seed:** `42` · **Rate limit:** `--wait 12` · **Model đo token:** `gemini-3.1-flash-lite` (`17` lần gọi model, `34` lần gọi công cụ, tổng `29.267` token vào / `18.251` token ra, độ trễ TB `15,6 giây/phiên`).
- Bảng ước tính sơ bộ 10 phiên thử (dùng tỷ lệ đạt Lượt 1 `16/24 = 67%`): `gemini-3.1-flash-lite` `$0.0035`/phiên · `$0.0052`/task thành công · `$1.57`/tháng (cơ sở 84 người, `$0.0187`/người/tháng); `gemini-3.8-flash` `$0.0181`/phiên · `$0.0271`/task thành công · `$8.19`/tháng (`$0.0975`/người/tháng).

### 2.2 Kết quả mô phỏng chính thức 50 phiên cho CP4 (`T4-05` & `T4-06` — chép nguyên từ `cost/simulate-1-summary.md`)

- **Lượt mô phỏng:** [cost/simulate-1.csv](simulate-1.csv) · **Tóm tắt:** [cost/simulate-1-summary.md](simulate-1-summary.md) · **Trace:** [traces/simulate-1.jsonl](../traces/simulate-1.jsonl)
- **Run ID:** `simulate-1@20261128-140657` · **Số phiên:** `50/50` phiên thành công (`0/50` phiên lỗi) · **Seed:** `42` · **Rate limit:** `--wait 6`
- **Tổng hợp 50 phiên (`S001–S050`, 106 lượt hỏi qua `agent.answer()` thật trên `gemini-3.1-flash-lite`):** tổng **`85` lần gọi model**, **`170` lần gọi công cụ** (`get_slide_content`, `get_teaching_strategy`), tổng **`187.421` token vào** (`TB 3.748,4 token/phiên`) và **`99.924` token ra** (`TB 1.998,5 token/phiên`), độ trễ trung bình **`26,53 giây/phiên`**.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| giang_vien_thinh_giang | 19 | 2 | 3484 | 1948 | 1.6 | 3.2 |
| lab_coach_chinh | 25 | 2 | 3427 | 1771 | 1.6 | 3.1 |
| giang_vien_chu_chot | 6 | 3 | 5922 | 3104 | 2.7 | 5.3 |

Tỉ lệ đạt dùng để tính: **22/24 (92%)** — lượt `run-2@20261128-135219` (`eval/run-2.csv`, `--rate-from`).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (22 người) | Chi phí / tháng — cơ sở (84 người) | Chi phí / tháng — cao (168 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gemini-3.1-flash-lite` (vào 0.25 · ra 1.5 $/1M) | $0.0039 | $0.0043 | $0.0020 | $0.5114 | $1.95 | $3.91 | $0.0232 |
| `gemini-3.8-flash` (vào 1.5 · ra 7.5 $/1M) | $0.0206 | $0.0225 | $0.0106 | $2.68 | $10.23 | $20.46 | $0.1218 |
| `gpt-6.1-terra` (vào 1.0 · ra 5.0 $/1M) | $0.0137 | $0.0150 | $0.0071 | $1.79 | $6.82 | $13.64 | $0.0812 |
| `gemini-4-hydrogen` (vào 1.5 · ra 7.5 $/1M) | $0.0206 | $0.0225 | $0.0106 | $2.68 | $10.23 | $20.46 | $0.1218 |

- **Chi phí / task thành công** = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt thật của Run 2 (`22/24 = 91,67%`) — **không coi như đạt 100%**. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (`2,1`) ÷ tỉ lệ đạt.
- **Token đo trên model:** `gemini-3.1-flash-lite`. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; đã ghi rõ *"đo trên model `gemini-3.1-flash-lite`, tính giá model Y"*.
- **Phiên lỗi (không tính vào trung bình):** `0/50`.

## 3. So với impact — M4-02 & T4-06 (chốt theo số chính thức 50 phiên `simulate-1@20261128-140657` và Lượt 2 `22/24 = 92%`)

**Nguồn:** `spec.md` §2 (impact), `cost/personas.yaml` (tần suất/quy mô), §2.2 ([cost/simulate-1.csv](simulate-1.csv), [cost/simulate-1-summary.md](simulate-1-summary.md), [traces/simulate-1.jsonl](../traces/simulate-1.jsonl), `50/50` phiên không lỗi, phủ đủ cả 3 persona `19 + 25 + 6 = 50` phiên) và tỷ lệ đạt Lượt 2 `22/24 (91,7%)` trên cùng model `gemini-3.1-flash-lite` ([eval/run-2.csv](../eval/run-2.csv)).

| Quy mô | Phiên/tháng (ước tính) | Impact tiềm năng (giờ/tháng) | `gemini-3.1-flash-lite` USD/tháng | `gemini-3.8-flash` USD/tháng (quy đổi) | `gpt-6.1-terra` USD/tháng (quy đổi) |
|---|---:|---:|---:|---:|---:|
| **Thấp: 22 người** | 118,8 | 39,6 | **$0.5114** | $2.68 | $1.79 |
| **Cơ sở: 84 người** | 453,6 | 151,2 | **$1.95** | $10.23 | $6.82 |
| **Cao: 168 người** | 907,2 | 302,4 | **$3.91** | $20.46 | $13.64 |

Tần suất bình quân `0,40 × 3 + 0,45 × 6 + 0,15 × 10 = 5,4` phiên/người/tháng. Impact tiềm năng `5,4 × 20 = 108` phút/người/tháng (`1,8` giờ), chưa đo thực nghiệm; số người là quy mô giả định dựa trên `training-ops` giả lập.

### Quy đổi cùng đơn vị và độ nhạy (cập nhật theo chi phí cơ sở 50 phiên: Lite `$0.0232`/người/tháng · Flash `$0.1218`/người/tháng)

So sánh chi phí AI với giá trị giờ công tiết kiệm ròng, không quy 108 phút tiềm năng thành tiền thực thu. Gọi `S` là phút tiết kiệm ròng bình quân mỗi phiên (tính cả phiên lỗi, công nạp nguồn, chờ, đọc, sửa, duyệt và chuẩn bị thủ công nếu cần; chất lượng phải tương đương), `W` là giá trị giờ công USD/giờ.

Giá trị tiết kiệm/người/tháng = `5,4 × S / 60 × W`. Hòa vốn riêng chi phí token khi giá trị này >= chi phí model/người/tháng:

| Giả định S (phút/phiên, chưa đo) | Giờ tiết kiệm/người/tháng | W hòa vốn Lite (`$0.0232`/người/tháng, USD/giờ) | W hòa vốn Flash (`$0.1218`/người/tháng, USD/giờ) |
|---|---:|---:|---:|
| 0 | 0 | Không hòa vốn | Không hòa vốn |
| 5 | 0,45 | **0,0516** | **0,2707** |
| 10 | 0,90 | **0,0258** | **0,1353** |
| 20 | 1,80 | **0,0129** | **0,0677** |

- Công thức `W hòa vốn = chi phí model/người/tháng ÷ số giờ tiết kiệm/người/tháng`. Với kết quả 50 phiên chính thức (`simulate-1@20261128-140657`) và tỷ lệ đạt Lượt 2 (`22/24 = 91,7%`), chi phí/task thành công của `gemini-3.1-flash-lite` giảm từ `$0.0052` (sơ bộ 10 phiên) xuống **`$0.0043`/task thành công** (và của `gemini-3.8-flash` giảm từ `$0.0271` xuống **`$0.0225`/task thành công**), trong khi chi phí/người/tháng ở kịch bản cơ sở (84 người) là **`$0.0232`/người/tháng** (Lite, tổng **`$1.95`/tháng** cho cả khóa 84 GV & lab coach) do 50 phiên đã bao gồm cả 6 phiên của nhóm `giang_vien_chu_chot` (3 lượt hỏi/phiên).
- **Kết luận — GO CHO PILOT CÓ KIỂM SOÁT / ITERATE ĐO THỜI GIAN THỰC TẾ:** Lượt 2 đã đạt chuẩn CP2 (`22/24 = 92%`, cả 5/5 metric đều đạt ngưỡng) và mô phỏng 50 phiên thực tế đạt `50/50` không lỗi với chi phí token rất thấp (`$1.95/tháng` cho 84 giảng viên & lab coach trên `gemini-3.1-flash-lite`, hoặc `$10.23/tháng` trên `gemini-3.8-flash`). Tuy nhiên nhóm vẫn giữ thái độ thận trọng: chỉ cần tiết kiệm ròng `S >= 5 phút/phiên` thì ngưỡng hòa vốn token chỉ là `$0.0516/giờ` (Lite), nhưng trước khi mở rộng quy mô lớn cần đo thực nghiệm thời gian soạn + duyệt kịch bản thực tế của giảng viên và xử lý nốt 2 case ngữ nghĩa `B01, B06`.

## 4. Giới hạn và ghi chú mở rộng

- Giá tính bằng USD theo bảng giá chuẩn công bố ngày 25/11/2026 (`further-reading/model-prices.md`); chưa tính giảm giá batch/cache, chi phí hosting/vận hành và chưa cộng chi phí giờ công giảng viên duyệt kịch bản.
- Khi đo token trên `gemini-3.1-flash-lite` và áp bảng giá model khác (`gemini-3.8-flash`, `gpt-6.1-terra`, `gemini-4-hydrogen`), kết quả là ước lượng quy đổi trên cùng số token đo được (bộ tách token tiếng Việt giữa các hãng có thể lệch nhau).
