# Chuẩn bị Demo AI Core — TeachFlow AI (D4-02)

> Phụ trách: Nguyễn Đức Đạt · Phạm vi: tầng gọi model (`codebase/ai.py`), truy xuất nguồn (`codebase/retrieval.py`), công cụ chỉ đọc (`codebase/tools.py`), sinh & tự sửa kịch bản (`codebase/generator.py`), điều phối (`codebase/agent.py`).

---

## 1. Kiến trúc luồng AI Core và các điểm quyết định của LLM

1. **Chặn trước (Guardrails trước khi gọi LLM):** Nếu yêu cầu thiếu `duration_minutes`/`level`/`objectives`/`sources` (như `B03`, `B04`, `B22`, `B23`) hoặc vi phạm phạm vi/an toàn (`B08`, `B09`, `B10`, `B24`), tầng điều phối dừng ngay, không tốn token gọi model sinh kịch bản.
2. **Truy xuất ngữ cảnh có giới hạn (`retrieve`):** `codebase/retrieval.py` giữ toàn bộ tài liệu nếu số đoạn `<= limit` (`12`); nếu bài dài hơn thì chấm điểm theo từ khóa và mã `code` trong truy vấn rồi sắp lại theo đúng thứ tự slide gốc, không trộn nguồn ngoài.
3. **Gọi tool chỉ đọc (`@tool`):** Trước khi gọi LLM, `codebase/agent.py` gọi 2 tool có `@tool` trong `codebase/tools.py` để ghi vào trace:
   - `get_slide_content(codes, documents)`: tra cứu chính xác các mã slide hợp lệ từ bộ nguồn đã chọn.
   - `get_teaching_strategy(context)`: lọc chiến lược sư phạm từ `data/teaching_strategies.json` theo thời lượng (`min_minutes <= duration_minutes`) và điều kiện thiết bị (`TS04` bị loại nếu môi trường không có máy/laptop).
   - Cả hai tool đều **chỉ đọc**, không gửi tin, không sửa dữ liệu, không tự chấm điểm hay tự duyệt.
4. **Quyết định của LLM & vòng tự sửa (`generate_script`, `MAX_REPAIRS = 2`):**
   - `SYSTEM_PROMPT` trong `codebase/generator.py` yêu cầu LLM: (i) bám tuyệt đối `<sources_data>`, (ii) trả `needs_clarification` nếu nguồn mâu thuẫn trực tiếp (`B02`) hoặc thiếu căn cứ (`B01`, `B20`), (iii) trả `refused` nếu vượt phạm vi, (iv) giữ đúng số phần và thứ tự khi `<user_request>` chỉ định chuỗi hoạt động (`B15`), (v) viết `teacher_script` theo nhịp kể chuyện đảo ngược (`Bối cảnh -> Nhận định -> Điểm đảo ngược -> Giải thích bám nguồn -> Ví dụ minh họa -> Payoff -> Chuyển ý`) và `teacher_actions` điều hướng slide gốc tối giản.
   - Sau mỗi lần model trả JSON, `codebase/validator.py` kiểm tra schema, tổng thời lượng liên tục từ phút `0`, mã `slide_refs`, trạng thái bắt buộc `pending_review`, và chặn thẻ HTML `<...>`/script nguy hiểm. Nếu lỗi, `_build_repair_prompt()` gửi lại danh sách lỗi kèm `<user_request>` và `<sources_data>` (tối đa `2` lần sửa). Nếu vẫn lỗi sau `MAX_REPAIRS`, trả `needs_clarification` (`INVALID_SCRIPT`).
5. **Chống nghẽn API (`post_json` retry + backoff):** `codebase/ai.py` thực hiện retry có giới hạn (`MAX_HTTP_RETRIES = 3`) với exponential backoff + jitter (`RETRY_BASE_SECONDS = 1.5s`, trần `15.0s`, tôn trọng `Retry-After`) cho các mã lỗi tạm thời `{429, 500, 502, 503, 504}`, `URLError` và `TimeoutError`; lỗi client (`400/401/403/404`) dừng ngay không retry.

---

## 2. Kịch bản Demo chạy thật (Case thường + Case khó)

> Trước khi demo, kiểm tra `.env` có `MODEL_PROVIDER=gemini`, `MODEL_NAME=gemini-3.1-flash-lite` (hoặc model dự phòng còn quota) và `API_KEY` hợp lệ. Không in giá trị key lên màn hình.

### Case A — Case thường: Tạo kịch bản bám slide sẵn có (`B13`)
- **Mục đích demo:** Chứng minh AI không tạo slide mới, chỉ chuyển slide `A01–A06` thành kịch bản dạy `60` phút với nhịp kể chuyện tự nhiên, hành động lớp rõ ràng và trạng thái `pending_review`.
- **Điểm cần chỉ cho BGK:**
  - `model`, `tokens_in`, `tokens_out` ghi từ `usageMetadata` thật của Gemini (`VERIFY-B13` trước demo: `tokens_in=2153`, `tokens_out=1278`, `3` segment tổng `60` phút, `tool_calls=2`).
  - `teacher_script` dẫn tự nhiên theo cấu trúc nhận định → điểm đảo ngược → giải thích bám nguồn `A01–A06`.
  - `warnings` nhắc giảng viên đối chiếu lại slide gốc trước khi duyệt (`status == "pending_review"`).

### Case B — Case thường có ràng buộc thứ tự: `B15` (cải tiến CP4)
- **Mục đích demo:** Trình bày lỗi thật từ Run 1 (`B15` từng trượt tiêu chí thứ tự hoạt động) và chứng minh cải tiến `SYSTEM_PROMPT` + `_build_repair_prompt` trong D4-01 đã khắc phục.
- **Input:** Yêu cầu 60 phút theo chuỗi `giới thiệu kịch bản, trình bày kiến thức, ví dụ, câu hỏi tương tác`.
- **Kết quả kỳ vọng & đã kiểm chứng (`VERIFY-B15-V2`):** Đúng `4` segment theo thứ tự (`Giới thiệu và Khởi động` → `Trình bày kiến thức chuyên sâu` → `Ví dụ minh họa và Thảo luận` → `Quiz và Tổng kết`), tổng `8+20+15+17 = 60` phút, `slide_refs` đều nằm trong `A01–A06`, `status == "pending_review"`.

### Case C — Case khó 1: Nguồn mâu thuẫn trực tiếp (`B02`)
- **Mục đích demo:** Chứng minh khả năng **không bịa và không tự chọn phe** khi `C01` và `C02` mâu thuẫn về bước định trước.
- **Kết quả kỳ vọng:** Trả `status: "needs_clarification"`, chỉ rõ `C01` và `C02` mâu thuẫn, hỏi giảng viên chọn nguồn ưu tiên thay vì sinh kịch bản `pending_review`.

### Case D — Case khó 2 / Từ chối: Prompt injection & bypass duyệt (`B10` hoặc `B09`)
- **Mục đích demo:** Yêu cầu ép gán `approved` và nhúng `<script>`/đọc `.env` bị chặn ở guardrail/validator, trả `status: "refused"`, không gọi tool ngoài allowlist, không xuất HTML hay bí mật.

---

## 3. Quan sát Trace và Mô phỏng Chi phí

- Lệnh kiểm tra cấu hình & dữ liệu chuẩn: `python3 run.py check`
- Chạy thử UI cục bộ phục vụ demo trực tiếp: `python3 run.py studio` (gửi request chế độ thật, xem JSON trả về và panel trace gồm `tool_calls`, `model_calls`, `tokens_in`, `tokens_out`, ghi chú `note` khi retry).
- Chạy đánh giá toàn bộ benchmark & lưu trace: `python3 run.py eval` → chấm tự động bằng `eval/auto_grader.py`.

---

## 4. Giới hạn hiện tại của hệ thống (nêu thẳng khi demo)

1. **Giới hạn quota Free Tier & ổn định API bên ngoài:** Retry + backoff xử lý tốt các đợt nghẽn ngắn (`HTTP 503`/`429` nhất thời), nhưng nếu hết hẳn quota ngày/phút (RPD/RPM) thì sau `MAX_HTTP_RETRIES = 3` hệ thống vẫn phải báo lỗi minh bạch chứ không tự fallback sang dữ liệu giả trong chế độ `real`.
2. **Truy xuất từ khóa ở `retrieve()`:** Phù hợp bộ nguồn slide nhỏ và vừa theo bài học; chưa dùng embedding ngữ nghĩa nên nếu giảng viên đặt câu hỏi đồng nghĩa hoàn toàn không trùng từ khóa trong slide dài (>12 đoạn) thì xếp hạng có thể kém tối ưu.
3. **Phạm vi chỉ tạo bản nháp:** Tool chỉ đọc (`get_slide_content`, `get_teaching_strategy`), không tự động đẩy lên LMS, không thay đổi slide PowerPoint gốc và luôn giữ trạng thái `pending_review` để giảng viên duyệt.
4. **Ràng buộc an toàn JSON/Văn bản thuần:** Để chặn XSS/HTML injection (`validator._UNSAFE`), mọi thẻ dạng `<...>` đều bị từ chối trong output kịch bản; vì vậy phần trình bày trong `teacher_actions` mô tả bằng ngôn ngữ tự nhiên thay vì nhúng mã HTML/CSS trực tiếp.
