# Chi phí khi dùng thật — TeachFlow AI

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Chấm ở rubric R6.
> Số mô phỏng **KHÔNG điền tay**: chỉ điền mục 2 sau khi chạy `python run.py simulate --rate-from eval/run-2.csv` qua agent gọi AI thật và chép nguyên bảng từ `cost/simulate-N-summary.md`.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí chuẩn** (USD / 1M token).

## 1. Đầu vào (đã chuẩn hóa tại `cost/personas.yaml`)

- **Persona (`cost/personas.yaml` — tổng `share = 1.00`, đúng vai giảng viên & lab coach):**
  1. `giang_vien_thinh_giang` (`share = 0.40`): `3` phiên/tháng, `2` lượt hỏi/phiên — tham chiếu nhóm nhận `<=4` buổi/ca trong `data/training-ops/` (7/14 GV + 21/62 lab coach = 28/76 ≈ 37%, làm tròn 0.40); tần suất phiên và lượt hỏi *(tự ước tính)*.
  2. `lab_coach_chinh` (`share = 0.45`): `6` phiên/tháng, `2` lượt hỏi/phiên — tham chiếu nhóm nhận `5–8` buổi/ca trong `data/training-ops/` (trung vị 6 ca/khóa 21 ngày≈1 tháng; kết hợp ghi chép P1 muốn dùng kịch bản khi dạy lab); tỷ lệ chia & lượt hỏi *(tự ước tính)*.
  3. `giang_vien_chu_chot` (`share = 0.15`): `10` phiên/tháng, `3` lượt hỏi/phiên — tham chiếu nhóm nhận `>=9` buổi/ca trong `data/training-ops/` (3/14 GV nhận 10–11 buổi + 6/62 coach nhận 9–10 ca; kết hợp ghi chép P2 tốn công chuẩn bị ví dụ/câu hỏi); tỷ lệ chia & lượt hỏi *(tự ước tính)*.
  - *Lưu ý minh bạch:* `data/training-ops/` là bảng lịch giả lập theo cấu trúc khóa AI20K thật (`data/training-ops/README.md`). Khi bảng impact ở `spec.md` §2 có thêm số liệu phỏng vấn mới từ `M3-07/M3-09`, cập nhật đồng bộ lại tần suất nếu cần.
- **Số người dùng thật đúng vai (3 kịch bản, KHÔNG lấy 700 học viên làm giảng viên):**
  - **Thấp:** `22` người (chỉ nhóm giảng viên đứng lớp chính của 1 khóa — tham chiếu `data/training-ops/README.md`, mức áp dụng thấp *(tự ước tính)*).
  - **Cơ sở:** `84` người (`22` giảng viên + `62` lab coach của 1 khóa AI20K theo cấu trúc `data/training-ops/README.md`).
  - **Cao:** `168` người (quy mô mở rộng 2 khóa song song / nhiều chương trình đào tạo cùng cỡ *(tự ước tính)*).
- **Giá 4 mức model (nguồn: `further-reading/model-prices.md`, BTC kiểm tra trên trang chính thức ngày `25/11/2026`, đơn vị USD / 1M token, giá standard):**
  - **Tầng Nhỏ:** `gemini-3.1-flash-lite` — vào `$0.25`, ra `$1.50` ([Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing), xem 25/11/2026).
  - **Tầng Vừa (model đang đo thật):** `gemini-3.8-flash` — vào `$1.50`, ra `$7.50` ([Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing), xem 25/11/2026; dùng giá từ 01/01/2027 theo đúng chỉ dẫn ở `further-reading/model-prices.md`).
  - **Tầng Vừa (đối chiếu liên hãng):** `gpt-6.1-terra` — vào `$1.00`, ra `$5.00` ([OpenAI Pricing](https://developers.openai.com/api/docs/pricing), xem 25/11/2026).
  - **Tầng Lớn:** `gemini-4-hydrogen` — vào `$1.50`, ra `$7.50` ([Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing), xem 25/11/2026).
- **Tỉ lệ đạt dùng để tính:** *(chờ kết quả chấm Run 2 `eval/run-2.csv` — KHÔNG mặc định 100%)*.
- **Ghi chú đo token:** *(chờ chạy `simulate` thật để ghi rõ "đo token trên model X, tính giá model Y"; lưu ý khác hãng có thể khác bộ tách token)*.

## 2. Kết quả mô phỏng

### 2.1 Kết quả chạy thử 10 phiên (`T3-11` — `python run.py simulate --try --wait 12 --rate-from eval/run-1.csv`)

- **Run ID:** `simulate-try@20261128-100812` · **Số phiên:** `10/10` phiên thành công (`0/10` phiên lỗi) · **Seed:** `42` · **Rate limit:** `--wait 12` (nghỉ 12 giây giữa 2 lượt gọi).
- **Model đo token thực tế:** `gemini-3.1-flash-lite` (do `gemini-3.8-flash` trong cùng Google Cloud Project đã chạm trần `GenerateRequestsPerDayPerProjectPerModel-FreeTier = 20 requests/ngày` sau khi chạy `eval --try` và `eval` Run 1; lần thử trước `simulate-error@20261128-093722` trên `gemini-3.8-flash` đã ghi nhận rõ lỗi `HTTP 429` này).
- **Tổng hợp 10 phiên (`S001–S010`, 20 lượt hỏi qua `agent.answer()` thật):** tổng `17` lần gọi model, `34` lần gọi công cụ (`get_slide_content`, `get_teaching_strategy`), tổng `29.267` token vào (`TB 2.926,7 token/phiên`) và `18.251` token ra (`TB 1.825,1 token/phiên`), độ trễ trung bình `15,6 giây/phiên` (9/10 phiên từ `5,0–9,8 giây`, riêng `S005` `89,95 giây`).

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| `giang_vien_thinh_giang` | 3 | 2 | 2314 | 1509 | 1.3 | 2.7 |
| `lab_coach_chinh` | 7 | 2 | 3189 | 1960 | 1.9 | 3.7 |
| `giang_vien_chu_chot` | 0 | 3 | — | — | — | — |

**Bảng ước tính sơ bộ từ 10 phiên thử `simulate-try@20261128-100812` (dùng tạm tỷ lệ đạt Lượt 1 `16/24 = 67%` của `run-1@20261128-092011`; bản chính thức CP4 sẽ chạy đủ 50 phiên và dùng tỷ lệ đạt Lượt 2 cùng model):**

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (22 người) | Chi phí / tháng — cơ sở (84 người) | Chi phí / tháng — cao (168 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gemini-3.1-flash-lite` (vào 0.25 · ra 1.5 $/1M) | $0.0035 | $0.0052 | $0.0026 | $0.4116 | $1.57 | $3.14 | $0.0187 |
| `gemini-3.8-flash` (vào 1.5 · ra 7.5 $/1M) | $0.0181 | $0.0271 | $0.0136 | $2.14 | $8.19 | $16.38 | $0.0975 |
| `gpt-6.1-terra` (vào 1.0 · ra 5.0 $/1M) | $0.0121 | $0.0181 | $0.0090 | $1.43 | $5.46 | $10.92 | $0.0650 |
| `gemini-4-hydrogen` (vào 1.5 · ra 7.5 $/1M) | $0.0181 | $0.0271 | $0.0136 | $2.14 | $8.19 | $16.38 | $0.0975 |

- *Lưu ý minh bạch:* Token trong bảng thử 10 phiên trên được **đo thật trên `gemini-3.1-flash-lite`**, sau đó nhân với đơn giá của `gemini-3.1-flash-lite`, `gemini-3.8-flash`, `gpt-6.1-terra`, `gemini-4-hydrogen`. Tỷ lệ đạt `16/24 (67%)` tạm lấy từ `eval/run-1.csv` (`gemini-3.8-flash`). Đây là lượt chạy thử `T3-11` (`--try 10`), **không tính là lượt 50 phiên CP4 (`T4-05`)**.

### 2.2 Kết quả mô phỏng chính thức ≥50 phiên cho CP4 (`T4-05`)

*(Chờ hoàn tất cải tiến `D4-01`/`M4-01` và chấm xong Lượt 2 `eval/run-2.csv` để chạy `python run.py simulate --rate-from eval/run-2.csv` đủ 50 phiên và dán bảng từ `cost/simulate-1-summary.md` vào đây.)*

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt thật của Run 2 — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): *(chờ `M3-09` & `M4-02` hoàn thiện bảng impact có số)*
- Chi phí / người / tháng (cơ sở, model __): *(chờ mục 2)*
- **Kết luận một dòng — đáng làm không:** *(chờ kết quả đo thật mục 2 và impact §2)*

## 4. Giới hạn và ghi chú mở rộng

- Giá tính bằng USD theo bảng giá chuẩn công bố ngày 25/11/2026; chưa tính giảm giá batch/cache và chưa cộng chi phí giờ công giảng viên duyệt kịch bản.
- Khi đo token trên một model (ví dụ họ Gemini) và áp bảng giá model khác hãng (ví dụ OpenAI `gpt-6.1-terra`), kết quả là ước lượng quy đổi cùng số token đo được do bộ tách token tiếng Việt giữa các hãng có thể lệch nhau.
