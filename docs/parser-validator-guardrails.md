# Bàn giao parser, guardrails, validator (B3-10)

Người làm: Hoàng Văn Bảo. Ba module này làm theo mục 5 của [interface-contract.md](interface-contract.md). Code chỉ dùng thư viện chuẩn của Python, không gọi model, không đọc `.env` và không sửa dữ liệu đầu vào.

| File | Hàm | Agent dùng ở bước nào |
|---|---|---|
| `codebase/parser.py` | `parse_document(request)` trả về danh sách đoạn nguồn, lỗi thì raise `ValueError` | Bước đầu tiên. Nếu lỗi, agent trả `needs_clarification` |
| `codebase/guardrails.py` | `check_request(context, sources)` trả về `{ok, errors, status}` | Trước khi tìm nguồn và gọi generator. Nếu lỗi, agent trả `needs_clarification` hoặc `refused` |
| `codebase/validator.py` | `validate_script(script, context, sources)` trả về `{ok, errors, warnings}` | Sau khi generator sinh kịch bản |

Khi chạy real mode, `agent.py` tự import ba file này nên Minh không cần sửa gì thêm.

## Cách gọi thử

```python
import json, sys; sys.path.insert(0, "codebase")
import parser, guardrails, validator
req = json.load(open("data/fixtures/lesson_request.json", encoding="utf-8"))
src = parser.parse_document(req)                    # 4 đoạn: OOP-P040, P041, P104, P106
guardrails.check_request(req, src)                  # {'ok': True, 'errors': [], 'status': None}
script = json.load(open("data/fixtures/script_response.json", encoding="utf-8"))
validator.validate_script(script, req, src)         # ok=True, kèm 2 cảnh báo REVIEW và SOURCE_REVIEW
```

## Parser

Với bài đã có trong `data/lessons/`, parser tìm bài theo `lesson_id`. `lesson_id` chỉ dùng để tra, không bao giờ được ghép thành đường dẫn, nên nhập `../.env` sẽ báo lỗi. Bài có sẵn cũng không cho gửi kèm `sources` hay `source_text` để ghi đè nội dung.

Với tài liệu giảng viên tự nạp thì dùng `lesson_id="custom"` và phải có `permission=true`. Có hai cách gửi:

- `sources`: danh sách đoạn đã chia sẵn, mỗi đoạn có `code` và `text`, có thể thêm `page`, `title`. Mã chỉ gồm chữ, số và `._-`, tối đa 40 ký tự, không được trùng.
- `source_text`: dán nguyên văn bản. Nếu là text trích từ PDF (các trang ngăn bằng ký tự `\f`) thì mỗi trang thành một đoạn. Nếu là Markdown có tiêu đề `#` thì mỗi mục thành một đoạn. Còn lại thì tách theo dòng trống. Đoạn dài quá 2500 ký tự được cắt theo câu. Mã đặt lần lượt U001, U002, U003…

Nếu có `source_refs` thì parser chỉ lấy đúng các mã đó, theo đúng thứ tự. Mã nào không có trong bài thì báo lỗi kèm tên mã.

Muốn chuẩn bị nguồn từ file PDF hoặc Markdown thì chạy `python codebase/parser.py bai.pdf > nguon.json`, rồi dán kết quả vào `sources`. Đọc PDF cần cài `pypdf`, và chỉ đọc được PDF có chữ, chưa đọc được ảnh scan.

## Guardrails

| Mã lỗi | Kết quả | Khi nào |
|---|---|---|
| `MISSING_DURATION`, `INVALID_DURATION` | hỏi lại | thiếu số phút, số phút không phải số nguyên dương, hoặc quá 480 phút |
| `MISSING_LEVEL`, `INVALID_LEVEL` | hỏi lại | thiếu trình độ hoặc trình độ không thuộc beginner, intermediate, advanced, mixed |
| `MISSING_CLASS_SIZE`, `MISSING_MODE`, `MISSING_EQUIPMENT`, `MISSING_OBJECTIVES` | hỏi lại | thiếu thông tin về lớp |
| `MISSING_SOURCES` | hỏi lại | chưa có tài liệu nguồn, không cho AI tự soạn theo hiểu biết riêng |
| `GRADING` | từ chối | yêu cầu chấm điểm cuối hoặc xếp hạng học viên |
| `SELF_APPROVE` | từ chối | yêu cầu tự gán "approved" hoặc bỏ qua bước duyệt |
| `EXTERNAL_SCRIPT` | từ chối | yêu cầu nhúng script hay link JS bên ngoài |
| `SECRETS` | từ chối | yêu cầu đọc hoặc in `.env`, API key, mật khẩu, token |
| `EXTERNAL_ACTION` | từ chối | yêu cầu đăng lên LMS, website hoặc gửi email, tin nhắn |
| `SURVEILLANCE` | từ chối | yêu cầu dùng camera hay theo dõi học viên |
| `PERSONAL_DATA` | từ chối | yêu cầu xử lý thông tin cá nhân của học viên |
| `FOLLOW_SOURCE` | từ chối | yêu cầu làm theo mọi chỉ dẫn ghi trong slide |
| `INJECTION_REQUEST` | từ chối | trong yêu cầu có câu kiểu "ignore previous instructions" |
| `INJECTION_SOURCE` | từ chối | trong đoạn nguồn có câu tấn công, lỗi ghi rõ mã đoạn, ví dụ I02 |
| `PERSONAL_DATA_SOURCE` | hỏi lại | tài liệu tự nạp có email hoặc số điện thoại, cần xóa trước khi gửi model |

Ngoài `check_request`, file còn có vài hàm nhỏ dùng riêng được: `context_errors`, `check_scope`, `detect_injection`, `find_pii`, `redact_pii`.

## Validator

Mỗi lỗi ghi theo dạng `[MÃ] vị trí: mô tả`. Ví dụ: `[SCHEMA] segments[2].assessment: thiếu trường bắt buộc.`

| Mã | Nội dung kiểm |
|---|---|
| `SCHEMA` | có đủ `lesson_title`, `duration_minutes`, `learning_objectives`, `segments`, `status`; mỗi hoạt động có đủ 11 trường và các trường chữ không để trống |
| `STATUS` | trạng thái phải là `pending_review`. Model trả về `approved` là lỗi |
| `TIMELINE` | số phút là số nguyên dương (5.0 cũng tính là sai), hoạt động đầu bắt đầu ở phút 0, các hoạt động nối tiếp nhau, tổng bằng thời lượng buổi học |
| `REF` | mỗi hoạt động có ít nhất một mã nguồn, và mã đó phải nằm trong các đoạn đã gửi cho model. Mã có trong bài nhưng không được chọn vẫn tính là sai |
| `UNSAFE` | trong nội dung có thẻ HTML, `javascript:`, `onerror=`… Phép so sánh như `id < 1` thì không bị tính |

Cảnh báo không làm kịch bản bị loại, chỉ để giảng viên chú ý:
- `REVIEW` luôn có, nhắc giảng viên đối chiếu lại với slide.
- `SOURCE_REVIEW` khi kịch bản dùng đoạn nguồn có đánh dấu cần kiểm lại.
- `PACING` khi một hoạt động dài hơn 30 phút.
- `COVERAGE` khi một mục tiêu gần như không được nhắc đến.
- `CHECK_UNDERSTANDING` khi không thấy câu hỏi kiểm tra hiểu bài.

## Kiểm thử

```bash
python -m unittest tests/test_bao_modules.py -v                 # 32 test, không gọi API
python -m unittest discover -s tests -p "test_*.py"             # toàn bộ test của nhóm
```

Kết quả chạy ngày 28/11/2026: 32/32 test pass, toàn bộ 77 test của nhóm pass. Trong đó có test chạy `agent.build_response` ở real mode với ba module này, các phần còn lại (generator, retrieval, tools) vẫn dùng mock.

Mình cũng thử 24 câu benchmark. Kết quả dưới đây chỉ là phần code chặn, chưa phải điểm eval:
- B03, B04, B22, B23 được hỏi lại.
- B08, B09, B10, B24 bị từ chối trước khi gọi generator.
- 16 câu còn lại đi tiếp bình thường.

131 đoạn của bài OOP và 3 bài mẫu hợp lệ không bị bắt nhầm.

## Duyệt và xuất (B3-08)

Phần giao diện nằm trong `codebase/studio.html` do Minh làm. Mình đã đọc code và chạy `python tests/browser_studio_smoke.py` trên Edge ở mock mode ngày 28/11/2026, kết quả pass (cần cài `pip install playwright` trước).

- Nút Duyệt chỉ bấm được khi kịch bản hợp lệ và giảng viên đã tích ô "đã đối chiếu".
- Sửa nội dung, sửa số phút, đổi thông tin lớp, đổi bài hoặc tải file mới đều làm mất trạng thái duyệt và đóng màn hình riêng.
- Chỉ bản đã duyệt mới xuất được `.md`, `.json` và mới mở được màn hình riêng. Nội dung hiển thị đều được escape.
- Ở phía server, validator không cho model tự gán approved hoặc trả về HTML, script.

Mình đề xuất Minh thêm một bước kiểm tra thẻ HTML trong hàm `validate()` của giao diện, cho phần giảng viên tự sửa. Hiện tại vẫn an toàn vì nội dung luôn được escape, nhưng thêm bước này thì file `.md` xuất ra sẽ sạch hơn.

## Giới hạn

- Guardrails bắt theo mẫu câu tiếng Việt và tiếng Anh. Người dùng viết lách đi thì vẫn có thể lọt, khi đó phải dựa vào model và giảng viên.
- Validator chỉ kiểm được cấu trúc. Mã nguồn đúng không có nghĩa là kiến thức đúng, nên các câu B01, B02, B07, B20 vẫn do model xử lý và người chấm đánh giá.
- Nếu một đoạn nguồn có câu tấn công thì cả yêu cầu bị từ chối, vì contract không cho bỏ riêng đoạn đó rồi chạy tiếp. Giảng viên xóa đoạn bị nêu mã rồi gửi lại.
- Chưa chạy với model thật, đang chờ Đạt làm xong D3-02 và D3-07.
