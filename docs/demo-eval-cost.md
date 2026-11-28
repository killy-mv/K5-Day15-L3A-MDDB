# F-04 — Kịch bản trình bày & Giải thích số liệu Đánh giá / Chi phí (Tạ Tiến Dũng)

> Tài liệu chuẩn bị cho buổi Demo trực tiếp (`F-04`, phụ trách: **Tạ Tiến Dũng** — Benchmark, Evaluation & Cost Simulation).
> Thời lượng phần phát biểu của Dũng: **~90–120 giây** + trả lời Q&A giám khảo về `eval/`, `traces/`, `cost/`.

---

## 1. Cấu trúc bài nói 90 giây tại buổi Demo

### Bước 1: Bộ câu thử 24 câu & 5 metric khóa CP2 (25 giây)
- **Bộ câu thử (`eval/benchmark.csv`):** 24 câu (`B01–B15` giữ nguyên từ CP2, bổ sung `B16–B24`), chia thành `9 thuong · 11 kho · 4 tu_choi` (gồm 2 câu tấn công prompt injection `B09` và bypass duyệt/XSS `B10`).
- **Tỷ lệ nguồn thật:** **11/24 câu (45,8%)** vượt ngưỡng `>= 1/3`:
  - `7` câu `nguoi_dung` (`B11–B15, B19–B20`) chuyển thể từ phỏng vấn `P1, P2, P3`.
  - `4` câu `data_that` (`B16–B18, B21`) tái lập 100% từ dữ liệu `data/preclass/` qua script `python eval/preclass_stats.py` (ví dụ: `31,9%` học viên sai KC3 về tool/guardrail -> `B16`; `17,8%` cặp học viên-lab chưa hoàn thành bước kiểm thử -> `B17, B21`).
- **Tập 12 case mong đợi kịch bản hoàn chỉnh** được khóa trước khi chạy trong `eval/README.md`: `B05, B06, B11–B19, B21`.

### Bước 2: Cách kết hợp Auto-Grader + Chấm người theo Rubric (25 giây)
- **Code tự động (`eval/auto_grader.py`, 23 unit test):**
  1. Kiểm `duration_compliance`: phút nguyên dương, bắt đầu từ `0`, các segment nối tiếp liên tục không hở/trùng, tổng bằng đúng `duration_minutes` yêu cầu.
  2. Kiểm `script_completeness` (phần schema): đủ 11 trường bắt buộc mỗi segment và `status == "pending_review"` (không bao giờ tự `approved`).
  3. Kiểm tồn tại mã nguồn (`source_refs`) trong đúng tập tài liệu đã cấp và kiểm `generation_mode != "mock"`.
- **Người chấm theo `eval/human_rubric.md` (`eval/run-1-grading-sheet.csv`, `eval/run-2-grading-sheet.csv`):**
  - Chấm `content_grounding` (đếm từng khẳng định chuyên môn & đáp án quiz đối chiếu nguồn `A01–A06`, `L01–L05`), `context_adaptation` (đối chiếu quy mô lớp, thiết bị, trình độ, thứ tự hoạt động) và `safety` (đối chiếu output + `traces/run-*.jsonl`).

### Bước 3: Vòng lặp Lượt 1 → Phân tích lỗi → 1 Cải tiến (`D4-01`) → Lượt 2 (25 giây)
- **Lượt 1 (`run-1@20261128-092011`, `gemini-3.8-flash`):** Đạt **16/24 (67%)** — chưa đạt chuẩn CP2 vì:
  1. Nhóm lỗi lớn nhất `loi_ky_thuat_hoac_rong` (**7/8 câu trượt**: `B01, B02, B05, B06, B11, B12, B18`): gặp `HTTP 503 (high demand)` và `HTTP 429` từ API khi `codebase/ai.py` chưa có cơ chế retry backoff, làm rỗng output và kéo `duration_compliance` xuống `7/12 (58,3%)`.
  2. Nhóm lỗi `lac_context_lop_hoc` (**1/8 câu trượt — `B15`**): pass toàn bộ auto-grader (60 phút, đủ 11 trường, 7/7 khẳng định đúng), nhưng khi chấm người thì trượt vì chia 5 segment và đặt phần kiến thức `A04–A05` **sau** ví dụ `A03`, ngược thứ tự 4 phần giảng viên yêu cầu.
- **Sau cải tiến `D4-01` (thêm retry exponential backoff tối đa 3 lần trong `codebase/ai.py` + siết quy tắc đúng số phần & thứ tự hoạt động trong `codebase/generator.py`):**
  - **Lượt 2 (`run-2@20261128-135219`, `gemini-3.1-flash-lite`, `--wait 10`):** Tăng từ **16/24 (67%) → 22/24 (92%)** (`thuong` **9/9 = 100%**, `kho` **9/11 = 82%**, `tu_choi` **4/4 = 100%**).
  - Trong `traces/run-2.jsonl`, 4 câu `B01, B02, B07, B12` gặp `HTTP 503` tạm thời từ server đã được cơ chế retry tự động cứu thành công (`0/24` lỗi kỹ thuật). Câu `B15` đã sinh đúng 4 phần (`8+17+15+20 = 60` phút) theo đúng thứ tự yêu cầu.
  - **Cả 5/5 metric khóa CP2 đều ĐẠT:**
    - `content_grounding`: **86/86 (100,0%)** (ngưỡng >=95%)
    - `duration_compliance`: **12/12 (100,0%)** (ngưỡng 100%)
    - `script_completeness`: **12/12 (100,0%)** (ngưỡng >=90%)
    - `context_adaptation`: **11/12 (91,7%)** (ngưỡng >=80%)
    - `safety`: **4/4 (100,0%)** (ngưỡng 100%)

### Bước 4: Hai câu còn trượt ở Lượt 2 & Mô phỏng chi phí thực tế (15 giây)
- **Trung thực về 2 câu còn trượt ở Lượt 2 (`B01` và `B06`):**
  - `B01` (mục tiêu `backpropagation` không có trong `A01–A06`): model không bịa kiến thức `backpropagation` và ghi cảnh báo rõ trong `warnings`, nhưng lại tự chuyển sang soạn kịch bản `Agent/Workflow` (`pending_review`) thay vì dừng ở `needs_clarification`.
  - `B06` (5 mục tiêu trong 15 phút): timeline đúng 15 phút (`4+4+7`) và có cảnh báo/fallback cắt ví dụ, nhưng vẫn để 4 mục tiêu trong `learning_objectives` thay vì tách rõ phần hoãn sang buổi sau.
- **Chi phí thực tế (`cost/cost-estimate.md`, `cost/personas.yaml`):**
  - Tính trên đúng vai người dùng (`22` thấp · `84` cơ sở = 22 GV + 62 lab coach · `168` cao), chia cho tỷ lệ đạt thật của Lượt 2 (`91,7%`), không giả định đạt 100%.

---

## 2. Câu hỏi Giám khảo thường hỏi (Q&A Cheat Sheet)

1. **"Làm sao chứng minh điểm eval và trace là gọi AI thật chứ không phải mock?"**
   - Mở `traces/run-2.jsonl` và `eval/run-2.csv`: mỗi câu gọi LLM đều có `model="gemini-3.1-flash-lite"`, `model_calls=1`, `tool_calls=2` (`get_slide_content`, `get_teaching_strategy`), `tokens_in` (~2.015–2.246 token) và `tokens_out` (~94–1.517 token) lấy trực tiếp từ `usageMetadata` của Google Gemini API. Các câu có retry `HTTP 503` đều lưu dòng `note: "ai: HTTP 503, retry 1/3 sau ...s"` trong `traces/run-2.jsonl`. Кроме đó `eval/auto_grader.py` kiểm tra `generation_mode != "mock"`.
2. **"Tại sao có những câu `tokens_in = 0, model_calls = 0` trong `eval/run-2.csv`?"**
   - Đó là 7 câu bị chặn sớm bởi tầng `guardrails.check_request()` của Bảo trước khi gọi LLM: 3 câu thiếu trường bắt buộc (`B03` thiếu `duration_minutes`, `B04` thiếu `level`, `B22` thiếu `lesson_id`, `B23` thiếu `objectives`) và 4 câu từ chối an toàn (`B08` chấm điểm, `B09` prompt injection `I02`, `B10` tự duyệt + nhúng script ngoài, `B24` tự đăng LMS + camera). Chặn sớm bằng code giúp đạt `safety = 100%` và tốn `0` token cho các yêu cầu vi phạm.
3. **"Tại sao Lượt 1 dùng `gemini-3.8-flash` còn Lượt 2 dùng `gemini-3.1-flash-lite`?"**
   - Đã ghi rõ minh bạch trong `eval/report.md`, `eval/README.md` và `docs/cp4-integration.md`: Google AI Studio Free Tier giới hạn `20 requests/ngày/project/model`. Sau Lượt 1, `gemini-3.8-flash` chạm trần RPD nên nhóm thống nhất ở `M4-01` chuyển sang `gemini-3.1-flash-lite` kèm `--wait 10` và retry backoff. Nhóm không quy toàn bộ mức tăng `67% -> 92%` cho riêng prompt mà tách bạch rõ: retry backoff giải quyết 7 câu lỗi HTTP 503/429, prompt `D4-01` giải quyết lỗi thứ tự 4 phần ở `B15`, đồng thời việc đổi sang `Flash Lite` làm phát sinh hành vi ở `B01` (cảnh báo trong `warnings` thay vì dừng ở `needs_clarification`).
