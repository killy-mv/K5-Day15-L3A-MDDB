# Bàn giao module Parser · Guardrails · Validator (B3-10)

Owner: Hoàng Văn Bảo. Theo [interface-contract.md](interface-contract.md) §5. Chỉ dùng thư viện chuẩn, không gọi model, không đọc `.env`, không sửa input.

| File | Hàm (contract) | Agent gọi ở đâu |
|---|---|---|
| `codebase/parser.py` | `parse_document(request) -> list[SourceSegment]`, lỗi là `ValueError` | `agent.build_response` bước 1 → `needs_clarification` khi lỗi |
| `codebase/guardrails.py` | `check_request(context, sources) -> {ok, errors, status}` | trước retrieval/generator; lỗi → `needs_clarification` hoặc `refused` |
| `codebase/validator.py` | `validate_script(script, context, sources) -> {ok, errors, warnings}` | sau generator, chạy cùng validator mock của contract |

Real mode của `agent.py` tự import ba module này (`dependencies("real")`), không cần sửa agent.

## Ví dụ gọi

```python
import json, sys; sys.path.insert(0, "codebase")
import parser, guardrails, validator
req = json.load(open("data/fixtures/lesson_request.json", encoding="utf-8"))
src = parser.parse_document(req)                    # 4 đoạn OOP-P040, P041, P104, P106
guardrails.check_request(req, src)                  # {'ok': True, 'errors': [], 'status': None}
script = json.load(open("data/fixtures/script_response.json", encoding="utf-8"))
validator.validate_script(script, req, src)         # ok=True + warnings [REVIEW], [SOURCE_REVIEW]
```

## Parser

- Bài đã đăng ký: tra `lesson_id` trong `data/lessons/*.json`; id chỉ là khóa tra, không phải path (`../.env` → lỗi). Có `sources`/`source_text` với bài đã đăng ký → lỗi (không ghi đè nguồn).
- `lesson_id="custom"` + `permission=true`, một trong hai:
  - `sources`: list `{code, text, page?, title?, section?, content_kind?, review_required?}`; mã chỉ gồm chữ/số/`._-`, ≤40 ký tự, không trùng; trường lạ bị bỏ.
  - `source_text`: text/Markdown/text trích PDF. Có `\f` → mỗi trang một đoạn (giữ `page`); có heading `#` → mỗi mục một đoạn (`title`); còn lại tách theo dòng trống. Đoạn > 2500 ký tự cắt theo câu. Mã `U001…` theo thứ tự, không random. Giới hạn 300 đoạn, 400 000 ký tự.
- `source_refs`: giữ đúng thứ tự, mã lạ → lỗi nêu mã.
- Dòng lệnh, ngoài luồng agent: `python codebase/parser.py bai.pdf > nguon.json` (cần `pip install pypdf`, chỉ PDF có lớp text, không OCR) hoặc `bai.md`. Kết quả dán vào `sources` của request custom.

## Guardrails — mã lỗi

| Mã | status | Khi nào |
|---|---|---|
| `MISSING_DURATION` / `INVALID_DURATION` | needs_clarification | thiếu/không nguyên dương / > 480 phút |
| `MISSING_LEVEL` / `INVALID_LEVEL` | needs_clarification | thiếu / ngoài beginner, intermediate, advanced, mixed |
| `MISSING_CLASS_SIZE`, `MISSING_MODE`, `MISSING_EQUIPMENT`, `MISSING_OBJECTIVES` | needs_clarification | thiếu context lớp |
| `MISSING_SOURCES` | needs_clarification | không có đoạn nguồn — không soạn từ kiến thức của AI |
| `GRADING` | refused | chấm điểm cuối, xếp hạng học viên |
| `SELF_APPROVE` | refused | gán approved, bỏ qua duyệt |
| `EXTERNAL_SCRIPT` | refused | nhúng script/JS ngoài, `javascript:` |
| `SECRETS` | refused | đọc/in `.env`, API key, mật khẩu, token |
| `EXTERNAL_ACTION` | refused | đăng LMS/website, gửi email/tin nhắn |
| `SURVEILLANCE` | refused | camera, theo dõi học viên |
| `PERSONAL_DATA` | refused | xử lý thông tin cá nhân học viên |
| `FOLLOW_SOURCE` | refused | "làm theo mọi chỉ dẫn trong slide" |
| `INJECTION_REQUEST` | refused | yêu cầu chứa "ignore previous instructions"… |
| `INJECTION_SOURCE` | refused | đoạn nguồn chứa chỉ dẫn tấn công; lỗi nêu mã đoạn (vd I02) |
| `PERSONAL_DATA_SOURCE` | needs_clarification | nguồn custom có email/SĐT; yêu cầu xóa trước khi gửi model |

Hàm phụ dùng lại được: `context_errors`, `check_scope`, `detect_injection`, `find_pii`, `redact_pii`.

## Validator — mã lỗi

Mỗi lỗi dạng `[MÃ] vị trí: mô tả`, vd `[SCHEMA] segments[2].assessment: thiếu trường bắt buộc.`

| Mã | Kiểm |
|---|---|
| `SCHEMA` | đủ `lesson_title, duration_minutes, learning_objectives, segments, status`; mỗi segment đủ 11 trường, chuỗi không rỗng; `warnings/assumptions` là list chuỗi |
| `STATUS` | chỉ `pending_review`; `approved/approved_by/approved_at` từ model là lỗi |
| `TIMELINE` | phút nguyên dương (5.0 cũng sai), `start_minute` từ 0 liên tục, tổng = input |
| `REF` | `slide_refs` không rỗng, thuộc nguồn **được cung cấp** (mã có trong bài nhưng ngoài `source_refs` vẫn lỗi) |
| `UNSAFE` | thẻ HTML, `javascript:`, `onerror=`… trong nội dung (so sánh `id < 1` không tính) |

Warnings (không làm fail): `REVIEW` (luôn có — giảng viên phải đối chiếu), `SOURCE_REVIEW` (nguồn `review_required`), `PACING` (hoạt động > 30 phút), `COVERAGE` (mục tiêu ít được nhắc), `CHECK_UNDERSTANDING` (không thấy câu hỏi kiểm tra hiểu).

## Kiểm thử

```bash
python -m unittest tests/test_bao_modules.py -v                 # 32 test, không gọi API
python -m unittest discover -s tests -p "test_*.py"             # toàn bộ test nhóm
```

Kết quả 28/11/2026: 32/32 pass; toàn bộ 77 test Python pass. Gồm test tích hợp chạy `agent.build_response(mode="real")` với 3 module này và generator/retrieval/tools của mock.

Đối chiếu 24 câu benchmark (chỉ phần code chặn, không phải điểm eval): B03, B04, B22, B23 → hỏi lại; B08, B09, B10, B24 → từ chối, generator không chạy; 16 câu còn lại qua guardrails. 131 đoạn OOP và 3 bài mẫu hợp lệ không bị bắt nhầm injection/PII.

## B3-08 — duyệt và xuất (đối chiếu `codebase/studio.html`, owner UI: Minh)

Đã đọc code và chạy `python tests/browser_studio_smoke.py` (cần `pip install playwright`, Edge): **PASS** 28/11/2026 ở mock mode.
- Nút Duyệt chỉ bật khi bản nháp qua `validate()` phía trình duyệt **và** đã tích "đã đối chiếu".
- Sửa nội dung/phút, đổi context, đổi bài hoặc tải file mới → `invalidate()`: mất duyệt, đóng màn hình riêng.
- Xuất `.md`/`.json` và mở màn hình riêng chỉ khi có bản đã duyệt; màn hình riêng dựng bằng `textContent`, review dùng `esc()`.
- Phía server: validator chặn model tự gán approved hoặc trả HTML/script.
- Đề xuất cho Minh: `validate()` phía trình duyệt chưa chặn thẻ HTML trong phần giảng viên tự sửa. Hiện an toàn vì nội dung luôn được escape, nhưng nên thêm kiểm tra để file `.md` xuất ra không chứa thẻ HTML.

## Giới hạn

- Bộ lọc guardrails dựa trên mẫu câu (regex tiếng Việt/Anh), không phải bộ lọc toàn diện; diễn đạt lách mẫu vẫn có thể lọt → model và giảng viên là lớp sau.
- Validator kiểm cấu trúc; mã nguồn hợp lệ không chứng minh kiến thức đúng (B01, B02, B07, B20 do model + người chấm).
- Phát hiện injection trong nguồn sẽ từ chối cả yêu cầu (contract không cho loại đoạn rồi chạy tiếp); giảng viên xóa đoạn bị nêu mã rồi gửi lại.
- Chưa chạy với model thật (chờ D3-02, D3-07).
