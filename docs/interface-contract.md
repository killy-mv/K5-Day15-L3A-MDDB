# TeachFlow AI — Interface contract v1.0 (M3-01)

Bản chuẩn kỹ thuật bàn giao để triển khai song song CP3. Thành viên xác nhận bằng ghi chú backlog/PR; chưa giả định cả nhóm đã review. Không thay đổi chuẩn đạt CP2 hoặc B01–B15. Phạm vi: sinh kịch bản, giảng viên dùng slide gốc và màn hình riêng đọc kịch bản.

## 1. Files và cách dùng

- Dataset chung: data/lessons/oop_annotations.json, lesson_id oop_annotations, 131 đoạn tóm lược theo trang PDF.
- Dataset CP2: data/lessons/teachflow_examples.json, giữ nguyên 4 lesson_id agent_intro, lab_tools, conflict, injection.
- Input mẫu: data/fixtures/lesson_request.json; output mẫu: data/fixtures/script_response.json.
- Mock Python: codebase/contract_mock.py; test: python -m unittest discover -s tests -p "test_contract_mock.py" -v.
- Chạy mock: python codebase/contract_mock.py. Không gọi API, không dùng kết quả mock chấm eval thật.
- JSON UTF-8, Python >=3.10; contract không yêu cầu framework.

## 2. Input (LessonRequest)

Dạng phẳng tương thích nguyên ô input của benchmark; không bọc trong context khác:

```json
{
  "lesson_id": "oop_annotations",
  "duration_minutes": 60,
  "level": "intermediate",
  "class_size": 40,
  "mode": "offline",
  "equipment": "Máy chiếu và laptop",
  "objectives": ["Giải thích domain constraint", "Phân biệt Mutator và Observer"],
  "request": "Soạn kịch bản cho phần thiết kế lớp Customer.",
  "source_refs": ["OOP-P040", "OOP-P041", "OOP-P104", "OOP-P106"]
}
```

| Field | Type | Quy tắc |
|---|---|---|
| lesson_id | str | ID bài có trong dataset được phép; không dùng làm đường dẫn file |
| duration_minutes | int | Số phút nguyên dương; null/thiếu -> hỏi lại, không đoán |
| level | str | beginner/intermediate/advanced; null/thiếu -> hỏi lại |
| class_size | int | Số học viên nguyên dương |
| mode | str | offline/online/hybrid |
| equipment | str | Điều kiện thực tế; mô tả không có thiết bị nếu không có |
| objectives | list[str] | Ít nhất một mục tiêu có nghĩa |
| request | str | Yêu cầu thêm, có thể rỗng; không có quyền đổi guardrail |
| source_refs | list[str] (optional) | Nếu có, giới hạn tập nguồn đúng bài; không có thì xét toàn bộ bài |
| sources | list[SourceSegment] (optional) | Dữ liệu custom do parser chuẩn hóa, chỉ dùng cho lesson_id=custom; không cho ghi đè ID bài cố định |
| permission | bool (optional) | Với file custom phải xác nhận true; fixture benchmark có sẵn không cần field này |

Context của lớp chính là các field duration_minutes, level, class_size, mode, equipment, objectives trong input. Không thêm dữ liệu cá nhân.

## 3. SourceSegment và dataset

Dataset có root object lessons: list[Lesson]; Lesson gồm id, title, segments; metadata source tùy chọn. Mỗi SourceSegment có code (str duy nhất trong bài), text (str không rỗng); có thể có page (int, đánh số PDF từ 1), title, section, content_kind, review_required. Ví dụ:

```json
{"code":"OOP-P041","page":41,"title":"Customer constraints","text":"id là Integer không thay đổi, bắt buộc và min 1; name là String có thể thay đổi, bắt buộc, tối đa 50 ký tự.","review_required":true}
```

Nguồn OOP là bản tóm lược, không phải trích nguyên văn. Đối chiếu PDF gốc khi cần xác nhận chi tiết code/hình; nguồn conflict/injection là fixture kiểm thử, không phải kiến thức hợp lệ. Mã source_refs/slide_refs là string, giữ nguyên từ dataset (A01, L01, OOP-P041...), không tự chuyển thành số trang. Không dùng ID ngoài bài đang chọn.

## 4. Output của generator/agent

Generator trả dict trực tiếp, không markdown fence. Khi thành công, các field tiêu đề, thời lượng, mục tiêu, segments và status nằm ở root (không bọc script); status=pending_review.

- lesson_title: str
- duration_minutes: int (bằng input)
- learning_objectives: list[str]
- segments: list[Segment], theo thứ tự timeline
- status: pending_review
- warnings, assumptions: list[str] (khuyến nghị)
- model: str (metadata, không dùng thay token trace)
- context: dict (tùy chọn)
- Mỗi Segment đủ title, start_minute, duration_minutes, slide_refs, activity_type, teacher_script, teacher_actions, student_activity, expected_outcome, assessment, fallback_strategy.
- title/activity_type/teacher_script/student_activity/expected_outcome/assessment/fallback_strategy: str không rỗng. teacher_actions chuẩn là str không rỗng; adapter được phép chuyển list[str] từ thiết kế context cũ thành str trước khi trả output.
- start_minute từ 0, duration_minutes nguyên dương, không chồng hoặc hở; tổng đúng input. slide_refs list[str] không rỗng, thuộc nguồn thực sự được cung cấp. Ví dụ minh họa phải ghi rõ; quiz có đáp án bám nguồn. Không kết luận ngữ nghĩa đúng chỉ vì mã hợp lệ.
- Không trả approved từ model. Việc duyệt là thao tác UI/service tách riêng; sửa nội dung hủy duyệt phiên bản cũ.

Output mẫu đầy đủ: data/fixtures/script_response.json. Không phải output LLM thật.

Khi thiếu context/căn cứ, mâu thuẫn: {"status":"needs_clarification","message":"...","missing_fields":["duration_minutes"],"source_refs":[]} (missing_fields/source_refs có thể rỗng).
Khi bị cấm: {"status":"refused","message":"...","reason_code":"OUT_OF_SCOPE"}; gợi ý cách hợp lệ.
Khi lỗi kỹ thuật: {"status":"error","message":"...","reason_code":"MODEL_ERROR"} ở UI; API exception để khung eval ghi error. Không trả kịch bản giả thay lỗi API. Không có segments ở output không phải kịch bản.

Contract bắt buộc của starter: answer(text: str) -> {"output": str}; output là JSON serialize từ dict nêu trên, text nhận nguyên ô input JSON. Không đổi tracing.py, eval/run_eval.py, cost/simulate.py hoặc run.py. app.py có thể thay launcher để gọi thật. Token thực lấy từ @model_call, không tự ước tính.

## 5. Hợp đồng hàm và quyền sở hữu

| Module | Hàm | Input -> Output | Owner |
|---|---|---|---|
| parser.py | parse_document(request) | LessonRequest -> list[SourceSegment]; lỗi có message, không đọc path tùy ý | Bảo |
| retrieval.py | retrieve(query, documents, limit=12) | str, list[SourceSegment], int -> list[SourceSegment]; chỉ subset của documents | Đạt |
| tools.py | get_slide_content(codes, documents) | list[str], list[SourceSegment] -> {segments,not_found}; @tool, chỉ đọc | Đạt |
| tools.py | get_teaching_strategy(context) | LessonRequest -> list[strategy dict]; @tool, chỉ đọc | Đạt |
| ai.py | call_model(system,user) | str,str -> {text,model,tokens_in,tokens_out}; @model_call, usage thật | Đạt |
| generator.py | generate_script(context,sources) | LessonRequest,list[SourceSegment] -> ScriptResponse; không tự duyệt | Đạt |
| guardrails.py | check_request(context,sources) | LessonRequest,list[SourceSegment] -> {ok,errors,status}; status khi lỗi needs_clarification/refused | Bảo |
| validator.py | validate_script(script,context,sources) | ScriptResponse,LessonRequest,list[SourceSegment] -> {ok,errors,warnings}; errors/warnings list[str] | Bảo |
| agent.py | answer(text) | str -> {"output": str}; điều phối, 5 quyết định model/2 sửa tối đa | Minh |
| app.py/backend | generate endpoint/CLI | LessonRequest -> ScriptResponse; gọi cùng answer(), không lộ key | Minh |
| eval/ | grader riêng | input, output, source, trace -> điểm theo metric CP2, không thay metric | Dũng |

Mock cùng tên hàm trong contract_mock.py, không ghi đè module production. Dùng mock như dependency thay thế tạm khi phát triển riêng. Đạt sở hữu tools.py; Bảo không sửa file này, bàn giao parser/guardrails riêng. Minh giữ agent.py và app.py; Dũng giữ eval/cost. Mọi thay đổi contract phải trao đổi trước, giữ backward compatibility. Không hardcode theo ID benchmark hoặc expected output.

## 6. Luồng và bàn giao

Parser -> check_request -> agent chọn tool đọc nguồn/chiến lược -> generator -> validator -> pending_review hoặc hỏi lại/từ chối. Tối đa 5 quyết định model và 2 lượt repair trong tổng giới hạn, dùng allowlist tool chỉ đọc. Backend/agent không tự chấm điểm cuối, gửi/publish hay đọc .env bằng tool. Giảng viên duyệt riêng, màn hình phụ chỉ đọc kịch bản; học viên vẫn xem slide gốc.

Đạt dùng JSON dataset trực tiếp; Bảo dùng input/output fixture để test; Dũng dùng fixture để kiểm grader (không chấm thành kết quả thật); Minh nối backend với mock trước. Bàn giao từng module khi chạy được, không đợi cả nhóm. Chạy eval thật chỉ khi agent tích hợp và trace có usage thật. Chuẩn đạt CP2, metric và benchmark cũ giữ nguyên.

Bản contract do đội trưởng yêu cầu chuẩn bị; mỗi thành viên review và ghi xác nhận tại M3-01 trước khi coi task xác nhận nhóm đã xong.
