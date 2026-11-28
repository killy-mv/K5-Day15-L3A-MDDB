# TeachFlow AI — Backlog nhóm MDDB

**Ưu tiên P0: CP3 trước 10:00 sáng 28/11/2026 (GMT+7).** CP4 trước 14:30 cùng ngày; khóa repo lúc 23:59. Căn cứ: [README](README.md), [guide §3.2–5.3](02-guide.md), [rubric](03-rubric.md), [context đã thống nhất](docs/context.md).

## Quy ước
- ✅ = task đã nghiệm thu theo tiêu chí trong bảng, có bằng chứng trong repo hoặc ghi chú xác nhận thực tế; ❌ = chưa xong (kể cả đang làm, có bản nháp, hoặc chưa xác minh).
- Mỗi dòng có một người chịu trách nhiệm chính; người đó cập nhật trạng thái và cột Ghi chú (PR, commit, output, blocker, thời điểm). Ô trống dành cho thành viên/đội trưởng điền. Không đánh dấu ✅ chỉ vì có code mẫu.
- Phạm vi: chỉ sinh kịch bản giảng dạy bám nguồn. Giảng viên dùng slide gốc trình chiếu; Teaching Mode là màn hình riêng để đọc kịch bản đã duyệt. HTML chỉ là định dạng đọc tùy chọn, không sinh bài trình chiếu mới.
- **Khóa CP2:** giữ nguyên chuẩn đạt ở spec §7 và toàn bộ eval/metric_spec.yaml. Giữ nguyên B01–B15, chỉ thêm case; không bỏ case trượt, sửa kết quả cũ hay ngưỡng. Pass rate >=80%, grounding >=95%, timeline 100%, completeness >=90%, adaptation >=80%, safety 100% (mọi câu từ chối gồm tấn công pass). Đánh giá thật, không dùng điểm mock. Có thể cập nhật số đo thực tế và phần spec chưa hoàn thiện.
- Không commit key/.env, dữ liệu cá nhân hay tài liệu khóa nguyên bản. Không đưa dữ liệu nhạy cảm vào model. Ghi nguồn, hạn chế và phần chưa xong trung thực.
- Trạng thái ban đầu đối chiếu main tại b50e194; chưa xác minh điểm/nộp form của BTC. Các task mới đều ❌ nếu chưa có bằng chứng. Không đưa phongvan.md bị loại vào nguồn evidence.

## 0. Nền tảng đã có trước CP3 (để tránh làm lại)

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| BASE-01 | Repo, TEAMS, canvas | Nguyễn Văn Minh | Repo công khai; 4 thành viên đúng format; canvas có dữ liệu ban đầu | ✅ | python run.py check; chưa xác minh nộp form |
| BASE-02 | Bằng chứng ban đầu P1/P2 | Nguyễn Văn Minh | Hai file ghi chép và summary, phân biệt diễn ý và nguyên văn | ✅ | Chưa đủ ngưỡng CP3 |
| BASE-03 | Benchmark và metric CP2 | Nguyễn Văn Minh | 15 case, 5 metric, chuẩn đạt đã khóa | ✅ | f97cbb2 |
| BASE-04 | Data Card và fixture mẫu | Nguyễn Văn Minh | Data Card, JSON bài mẫu/chiến lược/context có nhãn synthetic | ✅ | f97cbb2 |
| BASE-05 | Prototype Mock AI và test | Nguyễn Văn Minh | HTML local có sinh nháp, sửa, duyệt, đọc kịch bản; smoke test pass | ✅ | 87fc7a9; không phải AI thật; hoàn thành sau hạn CP2 |
| BASE-06 | Chốt phạm vi kịch bản | Nguyễn Đức Đạt | Context ghi màn hình phụ, slide gốc giữ nguyên | ✅ | af9a98e, b50e194 |

## 1. CP3 — Nguyễn Đức Đạt: AI Core, LLM, RAG

Bàn giao chính: module gọi LLM và sinh kịch bản có cấu trúc dựa trên nguồn. Làm song song với parser/validator bằng fixture JSON.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| D3-01 | Chuẩn bị key và chọn model | Nguyễn Đức Đạt | Key hợp lệ đặt local .env; ghi model/provider và quota thực tế; không commit key | ✅ | 28/11: Đạt cấu hình `.env` local (gitignored, không commit), gói Free tier Google AI Studio; smoke `gemini-3.8-flash` (`20`/`196` tokens, gặp HTTP 503 tạm thời khi tải cao) và chạy ổn định trên `gemini-3.1-flash-lite`. Chi tiết ở `docs/ai-core-test-20261128.md`. |
| D3-02 | Tích hợp API vào codebase/ai.py | Nguyễn Đức Đạt | call_model giữ @model_call, trả text/model/tokens_in/tokens_out từ usage thật; xử lý lỗi API rõ ràng | ✅ | 28/11: PR #8 (c987074), ai.py hỗ trợ Gemini, OpenAI-compatible, Anthropic, Ollama; giữ @model_call và lấy usage từ API. Unit test OpenAI/Gemini giả lập pass; đã chạy thật qua Gemini. |
| D3-03 | Smoke test LLM | Nguyễn Đức Đạt | Gọi thử thành công, có output và token thật; chia sẻ cách cấu hình .env.example không chứa key | ✅ | 28/11: Minh xác minh `gemini-3.8-flash` qua B11/B05 (`docs/real-smoke-20261128.md`); Đạt xác minh `gemini-3.8-flash` (`20`/`196` tokens) và `gemini-3.1-flash-lite` (`20`/`15` tokens); `.env.example` không chứa key (`docs/ai-core-test-20261128.md`). |
| D3-04 | Retrieval / RAG theo nguồn bài học | Nguyễn Đức Đạt | Chỉ đọc nguồn được chọn, trả đoạn có code/text; hỗ trợ tìm theo mục tiêu; nguồn thiếu thì báo không đủ, không bịa ID | ✅ | 28/11: retrieval.py PR #8; nguồn là subset, bài ngắn giữ nguyên, bài dài xếp keyword/code; 2 test pass. Đạt kiểm thiếu nguồn thật với Flash Lite trong PR #11; điểm 0 vẫn có thể được chọn. |
| D3-05 | Tool tra cứu nguồn và chiến lược | Nguyễn Đức Đạt | get_slide_content, get_teaching_strategy trong tools.py (hoặc wrapper thống nhất) có @tool, input/output rõ, chỉ đọc, trace được | ✅ | 28/11: tools.py có get_slide_content và get_teaching_strategy, @tool, chỉ đọc; test đăng ký tool, mã thiếu và chiến lược pass. |
| D3-06 | System prompt bám context | Nguyễn Đức Đạt | Chỉ dùng nguồn cho kiến thức; phân biệt dữ liệu với lệnh; hỏi lại khi thiếu; không tự duyệt, chấm điểm cuối hay làm việc ngoài phạm vi | ✅ | 28/11: SYSTEM_PROMPT tách dữ liệu và lệnh, giới hạn phạm vi; PR #11 siết mâu thuẫn trực tiếp/thiếu căn cứ. Run 1 trước PR #11 ghi grounding 50/50 theo phiếu chấm Dũng; không coi đó là kết quả sau cải tiến. |
| D3-07 | Generator kịch bản JSON | Nguyễn Đức Đạt | generate_script nhận context và sources; trả kịch bản theo schema CP2 hoặc trạng thái hỏi lại/từ chối; có lời dẫn, timeline, nguồn, hoạt động, quiz, fallback | ✅ | 28/11: generator tích hợp validator, JSON parse/repair; fixture và smoke thật B11/B05 với Flash, OOP và B11/B05 với Flash Lite pass cấu trúc. Chất lượng ngữ nghĩa vẫn phụ thuộc nguồn và người duyệt. |
| D3-08 | Giới hạn vòng quyết định/sửa | Nguyễn Đức Đạt | Luồng agent chọn công cụ trong allowlist, tối đa 5 quyết định model và 2 lượt sửa; dừng có lý do nếu không đủ căn cứ | ✅ | 28/11: agent gọi hai tool đọc cố định, generator giới hạn 5 model calls/2 repair (tối đa 3 lời gọi); unit test dừng sau 3 lần pass. Smoke thật 1 model call/2 tool mỗi case; chưa kích hoạt repair thật; repair prompt chưa gửi đủ nội dung nguồn. |
| D3-09 | Kiểm thử AI Core | Nguyễn Đức Đạt | Có output thật cho case thường và case thiếu/mâu thuẫn nguồn, không dựa trí nhớ model; kiểm tra trace | ✅ | 28/11: 10/10 unit test AI Core pass (87/87 toàn repo). Chạy thật qua `agent.answer()` (`gemini-3.1-flash-lite`): case thường `lesson_request.json` + `B11`/`B05` đều `pending_review` (`1` model call, `2` tools); case `conflict` (`C01` vs `C02`) và case thiếu nguồn (`Spring Security JWT` với `OOP-P040`) đều trả `needs_clarification`. Chi tiết: `docs/ai-core-test-20261128.md`. |
| D3-10 | Bàn giao module | Nguyễn Đức Đạt | PR code AI Core, cách gọi, input/output mẫu và giới hạn; Minh gọi được từ agent.py | ✅ | 28/11: PR #8 c987074 và PR #11 1f24657 đã merge; bàn giao AI Core và docs/ai-core-test-20261128.md. Kiểm bản merge 89/89 Python pass; không đổi benchmark, metric hay Run 1. |

## 2. CP3 — Hoàng Văn Bảo: Parser, Validator, Guardrails

Bàn giao module xử lý đầu vào và xác minh kịch bản; dùng fixture độc lập, không cần đợi API.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| B3-01 | Chuẩn hóa input | Hoàng Văn Bảo | Parser đọc text/Markdown và fixture theo lesson_id; hỗ trợ slide/PDF có text nếu khả thi; lỗi định dạng báo rõ | ✅ | 28/11: xong `codebase/parser.py`. Đọc bài theo lesson_id, đọc tài liệu tự nạp dạng text, Markdown hoặc text trích từ PDF. PDF có chữ thì chạy qua dòng lệnh (dùng pypdf), chưa OCR. Lỗi báo bằng tiếng Việt. Test: python -m unittest tests/test_bao_modules.py, 32/32 pass với model giả lập |
| B3-02 | Chunk và mã nguồn | Hoàng Văn Bảo | Mỗi đoạn có code duy nhất, text và tham chiếu slide/trang nếu có; không trộn tài liệu khác | ✅ | 28/11: chia đoạn và đặt mã U001, U002… theo thứ tự, giữ số trang và tiêu đề; đoạn dài hơn 2500 ký tự thì cắt theo câu. Mã trùng, mã có ký tự lạ hoặc mã không có trong bài đều báo lỗi |
| B3-03 | Kiểm tra context | Hoàng Văn Bảo | Phát hiện thiếu nguồn, thời lượng, trình độ, điều kiện lớp; yêu cầu bổ sung thay vì tự đoán | ✅ | 28/11: `guardrails.check_request` hỏi lại khi thiếu thời lượng, trình độ, sĩ số, hình thức học, thiết bị, mục tiêu hoặc nguồn. Các câu B03, B04, B22, B23 đều được hỏi lại |
| B3-04 | Validator schema | Hoàng Văn Bảo | Kiểm tất cả trường bắt buộc theo metric đã khóa; trả lỗi có mã và vị trí; không duyệt tự động | ✅ | 28/11: `validator.validate_script` kiểm đủ trường và trạng thái; lỗi ghi rõ vị trí, ví dụ segments[2].assessment. Chỉ chấp nhận pending_review |
| B3-05 | Validator timeline | Hoàng Văn Bảo | Phút nguyên dương, bắt đầu 0, liên tục, không trùng và tổng khớp yêu cầu; thiếu output tính fail | ✅ | 28/11: kiểm số phút nguyên dương, bắt đầu từ phút 0, các hoạt động nối tiếp nhau và tổng bằng thời lượng buổi học |
| B3-06 | Validator tham chiếu | Hoàng Văn Bảo | Mã nguồn tồn tại trong tài liệu được chọn; cảnh báo kiểm ngữ nghĩa thủ công, không coi mã hợp lệ là đủ căn cứ | ✅ | 28/11: mã nguồn trong kịch bản phải nằm trong các đoạn đã gửi cho model. Luôn có cảnh báo nhắc giảng viên đối chiếu, vì mã đúng chưa chắc nội dung đúng |
| B3-07 | Guardrail input/tool | Hoàng Văn Bảo | Tách dữ liệu khỏi lệnh, chặn truy cập file bí mật/tool ngoài allowlist; xử lý injection và yêu cầu chấm điểm/xếp hạng | ✅ | 28/11: từ chối chấm điểm, tự duyệt, nhúng script, đọc bí mật, đăng LMS hay gửi email, dùng camera, xử lý dữ liệu cá nhân và làm theo chỉ dẫn trong slide (B08, B09, B10, B24). 131 đoạn OOP không bị bắt nhầm. Bộ lọc theo mẫu câu nên chưa bắt được hết; danh sách tool được phép nằm ở agent.py |
| B3-08 | Kiểm soát duyệt và xuất | Hoàng Văn Bảo | Chỉ phiên bản hợp lệ và được duyệt rõ ràng mới xuất; sửa mất duyệt; escape nội dung, không thực thi script ngoài | ✅ | 28/11: validator chặn HTML/tự duyệt; UI kiểm HTML/script khi sửa (PR #7), sửa hủy duyệt/đóng reader; 23 JS và hai browser smoke pass. Regex không thay kiểm ngữ nghĩa. |
| B3-09 | Unit test độc lập | Hoàng Văn Bảo | Test nguồn hợp lệ/sai, thiếu context, timeline lỗi, schema thiếu, injection, bypass duyệt; có lệnh chạy và kết quả thật | ✅ | 28/11: tests/test_bao_modules.py có 32 test: nguồn đúng và sai, thiếu thông tin lớp, timeline lỗi, thiếu trường, injection, dữ liệu cá nhân, tự duyệt, và chạy thử qua agent.build_response. Toàn bộ 77 test của nhóm pass |
| B3-10 | Bàn giao module và Data Card | Hoàng Văn Bảo | PR parser/validator/guardrails, ví dụ gọi hàm, cập nhật Data Card nếu thêm nguồn; không đổi dữ liệu benchmark cũ | ✅ | 28/11: đã mở PR #5 từ nhánh HoangVanBao, kèm tài liệu docs/parser-validator-guardrails.md. Không thêm nguồn dữ liệu mới nên không sửa Data Card |

## 3. CP3 — Tạ Tiến Dũng: Benchmark và Evaluation

Chuẩn bị dữ liệu và cách chấm ngay; chỉ chạy chính thức khi tích hợp model thật xong.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| T3-01 | Mở rộng benchmark | Tạ Tiến Dũng | 20–30 case; giữ nguyên B01–B15, >=5 kho, >=2 tu_choi gồm 2 tấn công, >=1/3 nguồn thật có căn cứ; đủ 6 cột | ✅ | 28/11: 24 case (B01–B15 giữ nguyên, thêm B16–B24); 9 thuong/11 kho/4 tu_choi (2 tấn công B09–B10); 11/24=45.8% nguồn thật (7 nguoi_dung + 4 data_that tái lập qua eval/preclass_stats.py); python run.py check 0 cảnh báo |
| T3-02 | Lưới độ phủ và tập chấm | Tạ Tiến Dũng | eval/README.md cập nhật nguồn, độ phủ 3–5 chiều, danh sách case cần kịch bản hoàn chỉnh trước khi chạy | ✅ | 28/11: eval/README.md cập nhật nguồn, lưới độ phủ 5 chiều B01–B24, khóa 12 case kịch bản hoàn chỉnh (B05, B06, B11–B19, B21) trước Run 1; đồng bộ data/DATA_CARD.md |
| T3-03 | Chuẩn bị grader tự động | Tạ Tiến Dũng | Kiểm duration/schema/mã nguồn theo metric đã khóa; có test; phần ngữ nghĩa và context chấm người | ✅ | 28/11: eval/auto_grader.py + tests/test_auto_grader.py (23/23 unit test pass, đã đồng bộ Interface Contract v1.0, oop_annotations 131 trang, lọc source_refs và parser/guardrails/validator của Bảo); giữ nguyên eval/metric_spec.yaml |
| T3-04 | Chuẩn bị rubric chấm người | Tạ Tiến Dũng | Phiếu chấm có từng metric, tử/mẫu, pass_criterion, ghi chú và đối chiếu nguồn/trace | ✅ | 28/11: eval/human_rubric.md + eval/grading_sheet_template.csv đủ 5 metric, tử/mẫu, 24 pass_criterion, danh mục nhãn lỗi và checklist trace |
| T3-05 | Chạy thử và hiệu chuẩn | Tạ Tiến Dũng | Ghi 10–20 output thử, lỗi thực; hai người chấm độc lập 5 output, khớp >=4/5 hoặc báo thật phần chưa đạt | ❌ | 28/11: đã thu thập & ghi nhận 19 output thật từ gemini-3.8-flash trong eval/calibration_kit.md; Grader A (Dũng) đã chấm 5 câu mẫu tại eval/calibration_grader_a.csv; chờ thành viên thứ 2 chấm độc lập eval/calibration_grader_b.csv (báo thật chưa đủ 2 người) |
| T3-06 | Eval --try | Tạ Tiến Dũng | python run.py eval --try chạy 3 case, token/model thật, trace; ghi lỗi/quota nếu có | ✅ | 28/11: run-try@20261128-091903 với gemini-3.8-flash; B01 (1680/707 token), B02 (1493/932 token), B03 chặn sớm needs_clarification (0 token) |
| T3-07 | Eval Run 1 | Tạ Tiến Dũng | Chạy toàn bộ benchmark đã chốt, có eval/run-1.csv và traces/run-1.jsonl với run ID, token thật | ✅ | 28/11: eval/run-1.csv & traces/run-1.jsonl (Run ID run-1@20261128-092011, model gemini-3.8-flash, 24/24 câu; TB câu không lỗi: 901 token vào / 1691 token ra; 7 câu lỗi HTTP 503/429) |
| T3-08 | Chấm Run 1 | Tạ Tiến Dũng | Điền pass và ghi chú từng case theo tiêu chí; chạy score; tổng hợp 5 metric và kết quả thật | ✅ | 28/11: python run.py score eval/run-1.csv -> 16/24 đạt (67%: thuong 5/9, kho 7/11, tu_choi 4/4); 5 metric trong eval/run-1-grading-sheet.csv & run-1-metrics-summary.json (grounding 50/50=100%, duration 7/12=58.3%, completeness 7/12=58.3%, adaptation 6/12=50%, safety 4/4=100%) |
| T3-09 | Hồ sơ Eval 1 | Tạ Tiến Dũng | eval/README.md và report.md có cấu hình, run ID, điểm, giới hạn và file trace; gửi Minh cập nhật §7 | ✅ | 28/11: đã cập nhật đầy đủ eval/README.md, eval/report.md và spec.md §7/§10 với Run ID run-1@20261128-092011, bảng 5 metric và trace |
| T3-10 | Persona sơ bộ | Tạ Tiến Dũng | >=3 persona phù hợp giảng viên/lab coach, share tổng 1, tần suất có nguồn hoặc ghi tự ước tính | ✅ | 28/11: cost/personas.yaml có 3 persona GV/lab coach (share 0.40+0.45+0.15=1.00), dẫn nguồn training-ops/P1/P2 và ghi rõ tự ước tính; load_config() 0 cảnh báo |
| T3-11 | Simulate thử 10 phiên | Tạ Tiến Dũng | python run.py simulate --try chạy qua agent thật, có token/call/latency và ghi lỗi nếu có | ❌ | 28/11: đã chạy python run.py simulate --try --wait 3 (simulate-error@20261128-093722, 10 phiên S001–S010 qua agent thật), ghi nhận lỗi HTTP 429 chạm trần free-tier 20 req/ngày của gemini-3.8-flash và 3 lượt timeout 90s trong cost/cost-estimate.md §2; cần key mới/quota mới để có 10 phiên không lỗi |

## 4. CP3 — Nguyễn Văn Minh: Điều phối, Evidence, Integration, Demo

Ưu tiên nối AI thật; CLI đi hết lát cắt là phương án tối thiểu nếu web chưa kịp.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| M3-01 | Thống nhất interface | Nguyễn Văn Minh | Nhóm xác nhận schema input/context/source/output, hàm parser/retrieve/generate/validate, trạng thái hỏi lại/từ chối/chờ duyệt; ghi docs | ✅ | 28/11: TV1 xác nhận cả nhóm thống nhất contract v1.0; PR #5/#8, smoke B11/B05 và browser thật pass. Ghi docs/interface-contract.md; không đổi metric khóa. |
| M3-02 | Chuẩn bị backend local | Nguyễn Văn Minh | API/CLI nhận input và trả JSON theo contract, lỗi rõ, key chỉ ở server; có thể test bằng mock | ✅ | Backend local /api/health, /api/lessons, /api/generate; 12 API tests pass. |
| M3-03 | Tích hợp answer(text) | Nguyễn Văn Minh | agent.py nhận nguyên ô input benchmark, dùng parser/tool/LLM/validator; trả {"output": str}; ghi trace và giới hạn bước | ✅ | 28/11: AI Core PR #8 và module Bảo PR #5; smoke thật qua answer() pass B11/B05, mỗi case 1 model call/2 tool, token thật, trong budget. Repair có unit test; chưa kích hoạt repair thật. |
| M3-04 | Chạy end-to-end AI thật | Nguyễn Văn Minh | python run.py dùng AI thật cho case thường và khó; eval/ simulate gọi cùng answer(), không bypass agent | ✅ | 28/11: smoke_real_studio.py --run-real B11/B05 exit 0, 82,5 giây; Gemini 3.8 Flash, 9.077 token; kiểm cấu trúc và trace qua answer() dùng chung app/eval/simulate. Chưa chấm ngữ nghĩa/Run 1; UI thật thuộc M3-05. |
| M3-05 | Kết nối giao diện | Nguyễn Văn Minh | Planning Mode gửi nội dung/context tới agent, nhận nháp thật, hiện lỗi, nguồn và cảnh báo; fallback CLI nếu gấp | ✅ | 28/11: browser_studio_real.py --run-real PASS với Gemini 3.8 Flash; 5 hoạt động/60 phút, 5 nguồn, 4 cảnh báo, 4.662 token, 28,6 giây; duyệt/reader/JSON/sửa hủy duyệt/hỏi lại đều pass. |
| M3-06 | Teaching Mode đúng phạm vi | Nguyễn Văn Minh | Màn hình riêng đọc kịch bản đã duyệt; dùng slide gốc để chiếu; không tạo slide mới; HTML tùy chọn chỉ là định dạng đọc | ✅ | Cửa sổ riêng từ bản duyệt, timer, tiến độ, nguồn, đóng khi sửa; Edge smoke pass. Không tạo slide/HTML xuất mới. |
| M3-07 | Xác minh P1/P2 và phỏng vấn bổ sung | Nguyễn Văn Minh | >=3 người ngoài nhóm đúng vai, 10–15 phút/người, hỏi việc tháng qua, mỗi người 1 file; xác nhận lại P1/P2 hoặc thay bằng nguồn hợp lệ | ✅ | Đã có P1/P2/P3 (2 lab coach, 1 giảng viên), mỗi người một hồ sơ, hành vi tháng qua; TV1 xác nhận 28/11 cả 3 ngoài nhóm, mỗi cuộc 10–15 phút. |
| M3-08 | Bằng chứng nguyên văn | Nguyễn Văn Minh | >=5 trích dẫn/ví dụ thật có nguồn, bỏ tên; summary có số đếm và kết luận giả thuyết, không bịa số | ✅ | TV1 xác nhận 28/11 đủ 5/5 trích dẫn nguyên văn, có nguồn và ẩn danh (P1:1, P2:3, P3:1); tổng hợp evidence/summary.md và spec §1. |
| M3-09 | Impact và lựa chọn | Nguyễn Văn Minh | §2 so sánh >=3 hướng; người × lần × phút/tháng, nguồn hoặc tự ước tính từng số; ghi hướng loại và lý do | ✅ | §2: 3 hướng, quy mô/tần suất theo persona, phút/lần tự ước tính; chọn kịch bản, giữ lý do loại quiz riêng và slide. Impact cơ sở 9.072 phút/tháng là tiềm năng, chưa đo tiết kiệm. |
| M3-10 | Luồng hiện tại và pain | Nguyễn Văn Minh | §0–§1 hoàn chỉnh, 3–5 bước, ảnh che thông tin nếu có, công cụ hiện tại và nguồn; canvas đồng bộ | ✅ | Hoàn thiện spec §0–§1: 4 bước AS-IS, công cụ và nguồn P1–P3, pain/JTBD, 3/3 chưa có kịch bản đầy đủ; canvas đồng bộ phân công/phạm vi. Chưa có ảnh thực tế, ghi rõ chưa kiểm và giới hạn evidence. |
| M3-11 | Review sản phẩm tương tự | Nguyễn Văn Minh | Nhóm thử 2–3 giải pháp, ghi nhận quan sát thực tế và khác biệt trong §3; không giả trải nghiệm | ✅ | TV1 xác nhận 28/11 đã trực tiếp sử dụng các sản phẩm tương tự; review MagicSchool, Eduaide, Diffit trong spec §3 và docs/competitor-review.md, nhận xét từ nguồn công khai, không tạo log thao tác giả. |
| M3-12 | Đồng bộ thiết kế và hồ sơ | Nguyễn Văn Minh | §4–§6 đúng code/phạm vi mới, §7 chỉ bổ sung số eval, README lệnh chạy, Data Card/AI usage đủ; changelog có thời điểm | ✅ | 28/11: §4–§6, contract, README, Data Card v0.6, AI usage và changelog đồng bộ; bổ sung Run 1 tại §7 (16/24, run-1@20261128-092011), giữ nguyên chuẩn CP2. |
| M3-13 | Video CP3 | Nguyễn Văn Minh | Video 30 giây gọi AI thật, Drive anyone-link hoặc YouTube unlisted; kiểm mở ẩn danh | ✅ | 28/11: Minh xác nhận đã quay video và nộp CP3 thành công. Link video và kết quả kiểm mở ẩn danh chưa được cung cấp lại cho repo; trạng thái theo xác nhận người phụ trách. |
| M3-14 | Kiểm tra và nộp CP3 | Nguyễn Văn Minh | Merge PR, check, đủ §0–§7, evidence, 20–30 case, Run 1 + run ID, video; nộp trước 10h, khai thật phần thiếu | ✅ | 28/11: Minh xác nhận đã nộp CP3 thành công. Hồ sơ trên main có 24 câu, Run 1 run-1@20261128-092011 (16/24), spec §0–§7 và evidence; Run 1 chưa đạt chuẩn CP2. Không tự xác minh biên nhận form hoặc thời điểm nộp chính xác. |

## 5. CP4 — chỉ ưu tiên sau khi CP3 đã có kết quả thật

Deadline 14:30 ngày 28/11. Run 2 phải dùng đúng benchmark đã chạy Run 1 và cách chấm đã khóa.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| T4-01 | Phân tích lỗi Run 1 | Tạ Tiến Dũng | Nhóm lỗi có số case và >=3 ví dụ input/output/vì sao sai trong eval/report.md; cả nhóm chọn nhóm lỗi đau nhất | ✅ | 28/11: eval/report.md §2–§3 gom 2 nhóm lỗi (loi_ky_thuat_hoac_rong 7 câu HTTP 503/429, lac_context_lop_hoc 1 câu B15) kèm 4 ví dụ B05, B11, B18, B15 và đề xuất cải tiến retry backoff + ràng buộc thứ tự phân đoạn cho D4-01 |
| D4-01 | Cải tiến AI Core | Nguyễn Đức Đạt | Cải tiến prompt/retrieval/generator nhắm nhóm lỗi đã chọn; ghi cấu hình và lý do; không sửa benchmark/metric | ❌ | T4-01 đã phân tích lỗi Run 1: 7 lỗi API 503/429, 1 lỗi thứ tự B15. PR #11 chỉ siết mâu thuẫn nguồn; còn retry/backoff có giới hạn, xử lý quota và thứ tự hoạt động; chưa nghiệm thu cải tiến CP4. |
| B4-01 | Cải tiến kiểm tra an toàn | Hoàng Văn Bảo | Sửa parser/validator/guardrail nếu liên quan nhóm lỗi đã chọn; regression test và ghi rõ phạm vi | ❌ | T4-01 đã có; phối hợp Đạt/Minh xác định thay đổi an toàn liên quan lỗi mục tiêu, regression test. Chưa có PR cải tiến B4 trên main. |
| M4-01 | Tích hợp bản cải tiến | Nguyễn Văn Minh | Merge thay đổi có chọn lọc, demo case thường/khó, test luồng thật; changelog mô tả một nhóm lỗi mục tiêu | ❌ | PR #11 đã merge bổ sung kiểm thiếu/mâu thuẫn nguồn; chưa có bản cải tiến D4-01/B4-01 cho lỗi Run 1 để kiểm thử và khóa cấu hình Run 2. |
| T4-02 | Chạy Eval Run 2 | Tạ Tiến Dũng | Toàn bộ cùng benchmark, eval/run-2.csv và traces/run-2.jsonl, run ID/model/token thật | ❌ | BLOCKER: chờ M4-01 |
| T4-03 | Chấm và so sánh Run 2 | Tạ Tiến Dũng | Điền pass, ghi chú, chạy score; report và README có số lượt 1/2, đủ metric, nhóm lỗi cải thiện và lỗi còn lại/tệ đi | ❌ | BLOCKER: chờ T4-02 |
| T4-04 | Chốt personas và giá | Tạ Tiến Dũng | >=3 persona, share tổng 1, số người dùng/tần suất có nguồn hoặc ghi tự ước tính; >=2 mức model có nguồn giá/ngày | ✅ | 28/11: cost/personas.yaml & cost/cost-estimate.md §1 chốt users đúng vai 22/84/168 (GV+lab coach), 3 persona share=1.00, 3 tầng model từ further-reading/model-prices.md (25/11/2026); kiểm load_config() 0 cảnh báo |
| T4-05 | Mô phỏng >=50 phiên thật | Tạ Tiến Dũng | Seed cố định; qua answer thật; CSV và trace có token in/out, lượt gọi, latency, model; không tính mock | ❌ | M3-04 đã hoàn thành; chờ M4-01 và T4-03. Đã kiểm plan_sessions 50 phiên seed=42; simulate thử CP3 có lỗi quota/timeout, chưa đủ 50 phiên thật. |
| T4-06 | Chi phí và quy mô | Tạ Tiến Dũng | cost-estimate.md có thấp/cơ sở/cao, >=2 mức model, chi phí/task thành công = trung bình phiên chia tỷ lệ đạt lượt 2; ghi giới hạn nếu giá ước tính | ❌ | Đã hoàn thiện §1 đầu vào; BLOCKER: chờ T4-05 và tỷ lệ đạt Run 2 (T4-03) để điền §2–§3 |
| M4-02 | Impact so với chi phí | Nguyễn Văn Minh | Spec §8 và cost-estimate có so sánh chi phí/người/tháng với impact cùng đơn vị hoặc giải thích quy đổi, kết luận go/iterate/stop có căn cứ | ❌ | Chờ T4-06 |
| B4-02 | Hồ sơ an toàn | Hoàng Văn Bảo | §9 mô tả ẩn danh, quyền, rủi ro, giới hạn; test guardrails có kết quả thật | ❌ | Đã có spec §9; Run 1 safety 4/4 (B08/B09/B10/B24) theo eval/report.md, nhưng hồ sơ an toàn CP4 của Bảo chưa merge đầy đủ. |
| B4-03 | Người dùng thử (bonus) | Hoàng Văn Bảo | 2–3 người ngoài nhóm đúng vai, khoảng 10 phút/người, log hành vi và trích dẫn thật, tổng hợp 4 ý | ❌ | Không thay thế evidence pain |
| D4-02 | Chuẩn bị demo AI Core | Nguyễn Đức Đạt | Case thường và khó chạy thật; giải thích quyết định, dữ liệu, tool, trace và giới hạn | ❌ | |
| M4-03 | Slide demo | Nguyễn Văn Minh | 8 phần theo guide §5.1, mỗi trang có số/trích dẫn có nguồn/kết quả; cả nhóm bổ sung nội dung phụ trách; file hoặc link mở được | ❌ | |
| M4-04 | Video dự phòng và phòng demo | Nguyễn Văn Minh | Video thật mở ẩn danh được; xác nhận phòng/zone; kịch bản demo có case thường và khó, phân vai phát biểu | ❌ | Minh đã quay video CP3 và xác nhận nộp; cần xác minh link dự phòng mở ẩn danh, cập nhật demo theo bản cải tiến và xác nhận phòng/zone, phân vai. |
| M4-05 | Hồ sơ CP4 và nộp form | Nguyễn Văn Minh | Spec §0–§10, 7 hạng mục, Run 1/2, chi phí, slide, video dự phòng; push main, khai phần thiếu và nộp trước 14:30 | ❌ | |

## 6. Demo và hạn cuối — 23:59 ngày 28/11

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| F-01 | Demo và giải thích tích hợp | Nguyễn Văn Minh | Demo live theo lịch, giải thích lát cắt và kết quả; mỗi thành viên nói ít nhất một phần | ❌ | |
| F-02 | Demo và giải thích RAG | Nguyễn Đức Đạt | Giải thích quyết định LLM, nguồn, lỗi và giới hạn; sẵn sàng chạy câu lạ | ❌ | |
| F-03 | Demo và giải thích guardrails | Hoàng Văn Bảo | Giải thích parser, validator, HITL và cách chặn lỗi thực tế | ❌ | |
| F-04 | Demo và giải thích số liệu | Tạ Tiến Dũng | Giải thích grader, câu trượt, trace, tỷ lệ đạt, chi phí/task thành công | ❌ | Sự kiện demo trực tiếp 28/11 (chờ thêm số liệu Run 1/Run 2/simulate thật) |
| F-05 | Reflection cá nhân | Nguyễn Văn Minh | reflection/nguyen-van-minh.md có vai trò, phần làm, AI hỗ trợ, bài học từ lỗi thật | ❌ | |
| F-06 | Reflection cá nhân | Nguyễn Đức Đạt | reflection/nguyen-duc-dat.md có đủ nội dung theo guide | ❌ | |
| F-07 | Reflection cá nhân | Hoàng Văn Bảo | reflection/hoang-van-bao.md có đủ nội dung theo guide | ❌ | |
| F-08 | Reflection cá nhân | Tạ Tiến Dũng | reflection/ta-tien-dung.md có đủ nội dung theo guide | ✅ | 28/11: đã hoàn thành đủ 3 câu trong reflection/ta-tien-dung.md (câu 3 phân tích câu trượt thật B15 và lỗi HTTP 503/429 từ Run 1 run-1@20261128-092011) |
| F-09 | Xử lý phản hồi demo | Nguyễn Văn Minh | Điều phối sửa lỗi đã thống nhất, ghi giờ/đổi gì/vì sao vào §10; lượt chạy bổ sung ghi run mới | ❌ | Cả nhóm hỗ trợ |
| F-10 | Khóa bản nộp cuối | Nguyễn Văn Minh | Repo đủ hồ sơ, không secret/dữ liệu cá nhân, link công khai, main đã push trước 23:59; không sửa lịch sử eval | ❌ | |

## 7. Phối hợp và đường găng

- M3-01 phải thống nhất trước; sau đó Đạt D3-01–09, Bảo B3-01–09, Dũng T3-01–05/T3-10 và Minh M3-02/M3-07–11 làm song song.
- D3-10 + B3-10 -> M3-03 -> M3-04 -> T3-07/08/09 -> M3-14. D3-03, M3-04 và T3-06 có thể thử song song với key local riêng; thống nhất model và cấu hình cho Run 1. Video M3-13 và simulate thử T3-11 có thể chạy sau M3-04 song song, tránh vượt quota.
- M3-05/06 là phần giao diện; nếu không kịp, ưu tiên CLI chạy thật đầy đủ, ghi rõ phần web chưa xong. Không trì hoãn eval vì UI.
- CP4: T4-01 -> D4-01/B4-01 (chỉ sửa nhóm lỗi đã chọn) -> M4-01 -> T4-02/03 -> T4-06/M4-02 -> M4-05.
- Mỗi người làm trên nhánh của mình, cập nhật từ main, mở PR có test/ghi chú. Tránh sửa cùng một file; Minh điều phối merge. Không force push main. Không merge lại PR chứa phongvan.md bị loại.
- Hạn nội bộ đề xuất: trước 02:00 AI gọi thật + contract; trước 07:30 tích hợp; trước 09:00 Run 1 và chấm; trước 09:30 video/hồ sơ; nộp trước 10:00. Đây là mốc điều phối đề xuất, không phải deadline bổ sung của BTC.
