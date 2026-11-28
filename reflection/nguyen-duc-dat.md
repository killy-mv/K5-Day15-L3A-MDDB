# Reflection cá nhân — Nguyễn Đức Đạt

## 1. Vai trò và phần mình làm

- Mình phụ trách phần **AI Core** của bản chạy thử **TeachFlow AI**, gồm:
  - `codebase/ai.py`: kết nối API model thật (Gemini, OpenAI, Claude, Ollama) tuân thủ đúng hợp đồng `@model_call` và lấy số token thật từ trường `usage`/`usageMetadata` của API, tuyệt đối không ước lượng; đồng thời bổ sung cơ chế retry có giới hạn (`MAX_HTTP_RETRIES = 3`) với exponential backoff + jitter và tôn trọng `Retry-After` cho các lỗi tạm thời (`429`, `500`, `502`, `503`, `504`, `URLError`, `TimeoutError`).
  - `codebase/retrieval.py`: hàm `retrieve(query, documents, limit=12)` truy xuất đúng các đoạn trong nguồn bài học đã chọn, giữ nguyên toàn bộ ngữ cảnh cho bài ngắn và xếp hạng từ khóa/mã `code` theo thứ tự slide gốc cho bài dài.
  - `codebase/tools.py`: hai công cụ chỉ đọc có `@tool` (`get_slide_content`, `get_teaching_strategy`) phục vụ tra cứu mã slide và lọc chiến lược giảng dạy theo thời lượng/thiết bị, không có tác động ra ngoài.
  - `codebase/generator.py` & `tests/test_dat_ai_core.py`: xây dựng `SYSTEM_PROMPT`, vòng tự sửa lỗi schema/thời lượng (`MAX_REPAIRS = 2`), tích hợp cấu trúc kể chuyện đảo ngược cho `teacher_script` và hoàn thiện bộ unit test cho phần AI Core.
- Ngoài phần code lõi, mình cũng thiết kế lại bộ slide thuyết trình (`slides/AI_LLM_Foundation_Bahnschrift.pptx`) bám nguyên tắc một thông điệp chốt trên mỗi slide và đúc kết thành prompt sinh kịch bản nhất quán.

## 2. AI hỗ trợ mình thế nào

- AI coding agent giúp mình tăng tốc rõ rệt ở ba việc: rà soát hợp đồng giao diện giữa các module (`docs/interface-contract.md` với `agent.py` và `validator.py`), viết unit test giả lập response/HTTPError (`mock urllib.request.urlopen` và `call_model`), và tinh chỉnh prompt/công cụ trình bày.
- Cách dùng hiệu quả nhất là luôn giữ một **hợp đồng dữ liệu và bộ test làm điểm neo**: mỗi khi mình thêm quy tắc mới vào `SYSTEM_PROMPT` hoặc cơ chế retry trong `ai.py`, mình bắt buộc chạy lại toàn bộ `unittest`, `python run.py check` và gọi thử trực tiếp API thật trên từng case khó (như `B15`) thay vì chỉ nhìn code bằng mắt.

## 3. Một câu thử trượt của nhóm và mình học được gì

- **Sự cố thực tế gặp phải:** Ở Run 1 (`gemini-3.8-flash`), ngoài `7` ca lỗi kết nối `HTTP 503`/`429` do chưa có retry/backoff, có một ca trượt trực tiếp về logic sinh kịch bản là **`B15`** (`lac_context_lop_hoc`): người dùng yêu cầu tổ chức bài theo đúng 4 phần *giới thiệu kịch bản → trình bày kiến thức → ví dụ → câu hỏi tương tác*, nhưng model lại chia segment theo từng chủ đề slide (`Workflow vs Agent`, `Tool và Guardrail`...) nên làm sai cấu trúc yêu cầu; và khi sửa ở `_build_repair_prompt()`, phiên bản cũ lại chưa gửi kèm `<sources_data>` và `<user_request>` cho model.
- **Điều mình học được:**
  1. Model ngôn ngữ rất dễ trôi theo cấu trúc tài liệu nguồn (chia segment theo slide) thay vì cấu trúc sư phạm mà giảng viên đặt trong `<user_request>`, trừ khi `SYSTEM_PROMPT` chỉ rõ nguyên tắc ưu tiên trình tự hoạt động và cho phép gộp nhiều slide vào phần trình bày kiến thức.
  2. Mọi vòng tự sửa (`repair loop`) bắt buộc phải giữ đủ ngữ cảnh nguồn (`<sources_data>`) và yêu cầu gốc (`<user_request>`), nếu không model có thể sửa đúng thời lượng nhưng lại làm sai nội dung hoặc thứ tự.
  3. Độ tin cậy của AI App không chỉ nằm ở prompt: phần lớn lỗi Run 1 (`7/8`) đến từ hạ tầng API (`503`/`429`), nên xử lý lỗi tạm thời có giới hạn và chọn model dự phòng phù hợp (`gemini-3.1-flash-lite`) quan trọng ngang việc tối ưu câu chữ trong prompt.
