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

- **Kết quả chạy thử 10 phiên trước CP3 (`T3-11` — `python run.py simulate --try --wait 3`, Run ID `simulate-error@20261128-093722`, seed `42`):**
  - Đã chạy thật 10 phiên (`S001–S010`, tổng 20 lượt hỏi) qua `agent.answer()` ở chế độ `real` với `gemini-3.8-flash` ngay sau khi hoàn tất `eval --try` và `eval` Run 1 (`run-1@20261128-092011`).
  - **Phát hiện quan trọng về quota & latency:** Sau khi tiêu thụ đủ 20 lượt gọi LLM ở `eval --try` và `eval` Run 1, toàn bộ 10 phiên `simulate --try` chạm trần quota ngày của gói Google AI Studio Free Tier cho `gemini-3.8-flash` (`HTTP 429: Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3-flash`), và 3 lượt (`S001-T1`, `S004-T1`, `S008-T2`) bị timeout ở mốc 90 giây (`RuntimeError: Hết thời gian chờ phản hồi từ API model.`).
  - **Tham chiếu token thực tế đo được từ Lượt 1 (`eval/run-1.csv`, `run-1@20261128-092011`, model `gemini-3.8-flash`):** Trên 9 câu gọi LLM thành công (`B07, B13–B17, B19–B21`), trung bình mỗi lượt gọi model tiêu thụ **`1.702` token vào** và **`3.193` token ra** (tổng trên 17 câu không lỗi gồm cả 8 câu guardrail chặn sớm 0 token là trung bình **`901` token vào** và **`1.691` token ra** mỗi câu).
  - **Hành động cho CP4 (`T4-05` — 50 phiên chính thức):** Cần nạp API key có quota trả phí / key mới (hoặc chuyển sang model có hạn mức RPD cao hơn như `gemini-3.1-flash-lite`) trước khi chạy `python run.py simulate --rate-from eval/run-2.csv`.

*(Bảng chính thức 50 phiên CP4 dưới đây sẽ được dán nguyên văn từ `cost/simulate-1-summary.md` sau khi chạy `python run.py simulate --rate-from eval/run-2.csv`.)*

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · 50 phiên · seed 42

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (22 người) | / tháng — cơ sở (84 người) | / tháng — cao (168 người) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `gemini-3.1-flash-lite` | *(chờ simulate 50 phiên CP4)* | | | | | |
| `gemini-3.8-flash` | *(chờ simulate 50 phiên CP4)* | | | | | |
| `gpt-6.1-terra` | *(chờ simulate 50 phiên CP4)* | | | | | |
| `gemini-4-hydrogen` | *(chờ simulate 50 phiên CP4)* | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt thật của Run 2 — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): *(chờ `M3-09` & `M4-02` hoàn thiện bảng impact có số)*
- Chi phí / người / tháng (cơ sở, model __): *(chờ mục 2)*
- **Kết luận một dòng — đáng làm không:** *(chờ kết quả đo thật mục 2 và impact §2)*

## 4. Giới hạn và ghi chú mở rộng

- Giá tính bằng USD theo bảng giá chuẩn công bố ngày 25/11/2026; chưa tính giảm giá batch/cache và chưa cộng chi phí giờ công giảng viên duyệt kịch bản.
- Khi đo token trên một model (ví dụ họ Gemini) và áp bảng giá model khác hãng (ví dụ OpenAI `gpt-6.1-terra`), kết quả là ước lượng quy đổi cùng số token đo được do bộ tách token tiếng Việt giữa các hãng có thể lệch nhau.
