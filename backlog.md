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
| D3-01 | Chuẩn bị key và chọn model | Nguyễn Đức Đạt | Key hợp lệ đặt local .env; ghi model/provider và quota thực tế; không commit key | ❌ | |
| D3-02 | Tích hợp API vào codebase/ai.py | Nguyễn Đức Đạt | call_model giữ @model_call, trả text/model/tokens_in/tokens_out từ usage thật; xử lý lỗi API rõ ràng | ❌ | |
| D3-03 | Smoke test LLM | Nguyễn Đức Đạt | Gọi thử thành công, có output và token thật; chia sẻ cách cấu hình .env.example không chứa key | ❌ | |
| D3-04 | Retrieval / RAG theo nguồn bài học | Nguyễn Đức Đạt | Chỉ đọc nguồn được chọn, trả đoạn có code/text; hỗ trợ tìm theo mục tiêu; nguồn thiếu thì báo không đủ, không bịa ID | ❌ | Có thể dùng full context với bài ngắn, keyword với bài dài; chưa cần vector DB |
| D3-05 | Tool tra cứu nguồn và chiến lược | Nguyễn Đức Đạt | get_slide_content, get_teaching_strategy trong tools.py (hoặc wrapper thống nhất) có @tool, input/output rõ, chỉ đọc, trace được | ❌ | Phối hợp Bảo về dữ liệu parser |
| D3-06 | System prompt bám context | Nguyễn Đức Đạt | Chỉ dùng nguồn cho kiến thức; phân biệt dữ liệu với lệnh; hỏi lại khi thiếu; không tự duyệt, chấm điểm cuối hay làm việc ngoài phạm vi | ❌ | |
| D3-07 | Generator kịch bản JSON | Nguyễn Đức Đạt | generate_script nhận context và sources; trả kịch bản theo schema CP2 hoặc trạng thái hỏi lại/từ chối; có lời dẫn, timeline, nguồn, hoạt động, quiz, fallback | ❌ | |
| D3-08 | Giới hạn vòng quyết định/sửa | Nguyễn Đức Đạt | Luồng agent chọn công cụ trong allowlist, tối đa 5 quyết định model và 2 lượt sửa; dừng có lý do nếu không đủ căn cứ | ❌ | Phối hợp Minh tích hợp validator |
| D3-09 | Kiểm thử AI Core | Nguyễn Đức Đạt | Có output thật cho case thường và case thiếu/mâu thuẫn nguồn, không dựa trí nhớ model; kiểm tra trace | ❌ | |
| D3-10 | Bàn giao module | Nguyễn Đức Đạt | PR code AI Core, cách gọi, input/output mẫu và giới hạn; Minh gọi được từ agent.py | ❌ | Phụ thuộc D3-02–09 |

## 2. CP3 — Hoàng Văn Bảo: Parser, Validator, Guardrails

Bàn giao module xử lý đầu vào và xác minh kịch bản; dùng fixture độc lập, không cần đợi API.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| B3-01 | Chuẩn hóa input | Hoàng Văn Bảo | Parser đọc text/Markdown và fixture theo lesson_id; hỗ trợ slide/PDF có text nếu khả thi; lỗi định dạng báo rõ | ❌ | Không cần OCR cho MVP |
| B3-02 | Chunk và mã nguồn | Hoàng Văn Bảo | Mỗi đoạn có code duy nhất, text và tham chiếu slide/trang nếu có; không trộn tài liệu khác | ❌ | |
| B3-03 | Kiểm tra context | Hoàng Văn Bảo | Phát hiện thiếu nguồn, thời lượng, trình độ, điều kiện lớp; yêu cầu bổ sung thay vì tự đoán | ❌ | |
| B3-04 | Validator schema | Hoàng Văn Bảo | Kiểm tất cả trường bắt buộc theo metric đã khóa; trả lỗi có mã và vị trí; không duyệt tự động | ❌ | |
| B3-05 | Validator timeline | Hoàng Văn Bảo | Phút nguyên dương, bắt đầu 0, liên tục, không trùng và tổng khớp yêu cầu; thiếu output tính fail | ❌ | |
| B3-06 | Validator tham chiếu | Hoàng Văn Bảo | Mã nguồn tồn tại trong tài liệu được chọn; cảnh báo kiểm ngữ nghĩa thủ công, không coi mã hợp lệ là đủ căn cứ | ❌ | |
| B3-07 | Guardrail input/tool | Hoàng Văn Bảo | Tách dữ liệu khỏi lệnh, chặn truy cập file bí mật/tool ngoài allowlist; xử lý injection và yêu cầu chấm điểm/xếp hạng | ❌ | RAG không thay guardrails |
| B3-08 | Kiểm soát duyệt và xuất | Hoàng Văn Bảo | Chỉ phiên bản hợp lệ và được duyệt rõ ràng mới xuất; sửa mất duyệt; escape nội dung, không thực thi script ngoài | ❌ | Phối hợp Minh nối UI |
| B3-09 | Unit test độc lập | Hoàng Văn Bảo | Test nguồn hợp lệ/sai, thiếu context, timeline lỗi, schema thiếu, injection, bypass duyệt; có lệnh chạy và kết quả thật | ❌ | |
| B3-10 | Bàn giao module và Data Card | Hoàng Văn Bảo | PR parser/validator/guardrails, ví dụ gọi hàm, cập nhật Data Card nếu thêm nguồn; không đổi dữ liệu benchmark cũ | ❌ | |

## 3. CP3 — Tạ Tiến Dũng: Benchmark và Evaluation

Chuẩn bị dữ liệu và cách chấm ngay; chỉ chạy chính thức khi tích hợp model thật xong.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| T3-01 | Mở rộng benchmark | Tạ Tiến Dũng | 20–30 case; giữ nguyên B01–B15, >=5 kho, >=2 tu_choi gồm 2 tấn công, >=1/3 nguồn thật có căn cứ; đủ 6 cột | ✅ | 28/11: 24 case (B01–B15 giữ nguyên, thêm B16–B24); 9 thuong/11 kho/4 tu_choi (2 tấn công B09–B10); 11/24=45.8% nguồn thật (7 nguoi_dung + 4 data_that tái lập qua eval/preclass_stats.py); python run.py check 0 cảnh báo |
| T3-02 | Lưới độ phủ và tập chấm | Tạ Tiến Dũng | eval/README.md cập nhật nguồn, độ phủ 3–5 chiều, danh sách case cần kịch bản hoàn chỉnh trước khi chạy | ✅ | 28/11: eval/README.md cập nhật nguồn, lưới độ phủ 5 chiều B01–B24, khóa 12 case kịch bản hoàn chỉnh (B05, B06, B11–B19, B21) trước Run 1; đồng bộ data/DATA_CARD.md |
| T3-03 | Chuẩn bị grader tự động | Tạ Tiến Dũng | Kiểm duration/schema/mã nguồn theo metric đã khóa; có test; phần ngữ nghĩa và context chấm người | ✅ | 28/11: eval/auto_grader.py + tests/test_auto_grader.py (21/21 unit test pass); giữ nguyên eval/metric_spec.yaml |
| T3-04 | Chuẩn bị rubric chấm người | Tạ Tiến Dũng | Phiếu chấm có từng metric, tử/mẫu, pass_criterion, ghi chú và đối chiếu nguồn/trace | ✅ | 28/11: eval/human_rubric.md + eval/grading_sheet_template.csv đủ 5 metric, tử/mẫu, 24 pass_criterion, danh mục nhãn lỗi và checklist trace |
| T3-05 | Chạy thử và hiệu chuẩn | Tạ Tiến Dũng | Ghi 10–20 output thử, lỗi thực; hai người chấm độc lập 5 output, khớp >=4/5 hoặc báo thật phần chưa đạt | ❌ | Đã chuẩn bị eval/calibration_kit.md, calibration_grader_a/b.csv và lệnh --agreement; BLOCKER: chờ output thật sau M3-04 và người chấm độc lập thứ 2 trong nhóm (không bịa người chấm) |
| T3-06 | Eval --try | Tạ Tiến Dũng | python run.py eval --try chạy 3 case, token/model thật, trace; ghi lỗi/quota nếu có | ❌ | BLOCKER: chờ M3-04 (codebase/ai.py và agent.py trên main vẫn ở chế độ fake, chưa nối API thật) |
| T3-07 | Eval Run 1 | Tạ Tiến Dũng | Chạy toàn bộ benchmark đã chốt, có eval/run-1.csv và traces/run-1.jsonl với run ID, token thật | ❌ | BLOCKER: chờ M3-04 và T3-06 |
| T3-08 | Chấm Run 1 | Tạ Tiến Dũng | Điền pass và ghi chú từng case theo tiêu chí; chạy score; tổng hợp 5 metric và kết quả thật | ❌ | BLOCKER: chờ T3-07; đã sẵn auto_grader.py + human_rubric.md + grading_sheet_template.csv |
| T3-09 | Hồ sơ Eval 1 | Tạ Tiến Dũng | eval/README.md và report.md có cấu hình, run ID, điểm, giới hạn và file trace; gửi Minh cập nhật §7 | ❌ | BLOCKER: chờ T3-08 |
| T3-10 | Persona sơ bộ | Tạ Tiến Dũng | >=3 persona phù hợp giảng viên/lab coach, share tổng 1, tần suất có nguồn hoặc ghi tự ước tính | ✅ | 28/11: cost/personas.yaml có 3 persona GV/lab coach (share 0.40+0.45+0.15=1.00), dẫn nguồn training-ops/P1/P2 và ghi rõ tự ước tính; load_config() 0 cảnh báo |
| T3-11 | Simulate thử 10 phiên | Tạ Tiến Dũng | python run.py simulate --try chạy qua agent thật, có token/call/latency và ghi lỗi nếu có | ❌ | BLOCKER: chờ M3-04; đã test cấu hình và plan_sessions trong tests/test_auto_grader.py |

## 4. CP3 — Nguyễn Văn Minh: Điều phối, Evidence, Integration, Demo

Ưu tiên nối AI thật; CLI đi hết lát cắt là phương án tối thiểu nếu web chưa kịp.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| M3-01 | Thống nhất interface | Nguyễn Văn Minh | Nhóm xác nhận schema input/context/source/output, hàm parser/retrieve/generate/validate, trạng thái hỏi lại/từ chối/chờ duyệt; ghi docs | ❌ | Contract v1.0, dataset OOP 131 trang, fixture và mock đã có; chờ thành viên xác nhận contract. Không đổi metric khóa. |
| M3-02 | Chuẩn bị backend local | Nguyễn Văn Minh | API/CLI nhận input và trả JSON theo contract, lỗi rõ, key chỉ ở server; có thể test bằng mock | ✅ | Backend local /api/health, /api/lessons, /api/generate; 12 API tests pass. |
| M3-03 | Tích hợp answer(text) | Nguyễn Văn Minh | agent.py nhận nguyên ô input benchmark, dùng parser/tool/LLM/validator; trả {"output": str}; ghi trace và giới hạn bước | ❌ | Agent orchestration chạy mock end-to-end; có đường real mode không fallback. Chờ module Đạt/Bảo và xác minh budget model/trace thật. |
| M3-04 | Chạy end-to-end AI thật | Nguyễn Văn Minh | python run.py dùng AI thật cho case thường và khó; eval/ simulate gọi cùng answer(), không bypass agent | ❌ | Điều kiện mở khóa eval |
| M3-05 | Kết nối giao diện | Nguyễn Văn Minh | Planning Mode gửi nội dung/context tới agent, nhận nháp thật, hiện lỗi, nguồn và cảnh báo; fallback CLI nếu gấp | ❌ | studio.html đã gọi Python API, browser smoke pass ở mock mode; chờ nháp LLM thật. |
| M3-06 | Teaching Mode đúng phạm vi | Nguyễn Văn Minh | Màn hình riêng đọc kịch bản đã duyệt; dùng slide gốc để chiếu; không tạo slide mới; HTML tùy chọn chỉ là định dạng đọc | ✅ | Cửa sổ riêng từ bản duyệt, timer, tiến độ, nguồn, đóng khi sửa; Edge smoke pass. Không tạo slide/HTML xuất mới. |
| M3-07 | Xác minh P1/P2 và phỏng vấn bổ sung | Nguyễn Văn Minh | >=3 người ngoài nhóm đúng vai, 10–15 phút/người, hỏi việc tháng qua, mỗi người 1 file; xác nhận lại P1/P2 hoặc thay bằng nguồn hợp lệ | ❌ | Nhờ cả nhóm hỗ trợ tìm người |
| M3-08 | Bằng chứng nguyên văn | Nguyễn Văn Minh | >=5 trích dẫn/ví dụ thật có nguồn, bỏ tên; summary có số đếm và kết luận giả thuyết, không bịa số | ❌ | |
| M3-09 | Impact và lựa chọn | Nguyễn Văn Minh | §2 so sánh >=3 hướng; người × lần × phút/tháng, nguồn hoặc tự ước tính từng số; ghi hướng loại và lý do | ❌ | |
| M3-10 | Luồng hiện tại và pain | Nguyễn Văn Minh | §0–§1 hoàn chỉnh, 3–5 bước, ảnh che thông tin nếu có, công cụ hiện tại và nguồn; canvas đồng bộ | ❌ | |
| M3-11 | Review sản phẩm tương tự | Nguyễn Văn Minh | Nhóm thử 2–3 giải pháp, ghi nhận quan sát thực tế và khác biệt trong §3; không giả trải nghiệm | ❌ | Mỗi thành viên hỗ trợ |
| M3-12 | Đồng bộ thiết kế và hồ sơ | Nguyễn Văn Minh | §4–§6 đúng code/phạm vi mới, §7 chỉ bổ sung số eval, README lệnh chạy, Data Card/AI usage đủ; changelog có thời điểm | ❌ | Không sửa chuẩn đạt |
| M3-13 | Video CP3 | Nguyễn Văn Minh | Video 30 giây gọi AI thật, Drive anyone-link hoặc YouTube unlisted; kiểm mở ẩn danh | ❌ | Chờ M3-04 |
| M3-14 | Kiểm tra và nộp CP3 | Nguyễn Văn Minh | Merge PR, check, đủ §0–§7, evidence, 20–30 case, Run 1 + run ID, video; nộp trước 10h, khai thật phần thiếu | ❌ | Chờ T3-09, M3-07–13 |

## 5. CP4 — chỉ ưu tiên sau khi CP3 đã có kết quả thật

Deadline 14:30 ngày 28/11. Run 2 phải dùng đúng benchmark đã chạy Run 1 và cách chấm đã khóa.

| Mã việc | Mô tả | Người phụ trách | Tiêu chí hoàn thành | Trạng thái | Ghi chú |
|---|---|---|---|:---:|---|
| T4-01 | Phân tích lỗi Run 1 | Tạ Tiến Dũng | Nhóm lỗi có số case và >=3 ví dụ input/output/vì sao sai trong eval/report.md; cả nhóm chọn nhóm lỗi đau nhất | ❌ | BLOCKER: chờ T3-07 và T3-08 |
| D4-01 | Cải tiến AI Core | Nguyễn Đức Đạt | Cải tiến prompt/retrieval/generator nhắm nhóm lỗi đã chọn; ghi cấu hình và lý do; không sửa benchmark/metric | ❌ | Chờ T4-01 |
| B4-01 | Cải tiến kiểm tra an toàn | Hoàng Văn Bảo | Sửa parser/validator/guardrail nếu liên quan nhóm lỗi đã chọn; regression test và ghi rõ phạm vi | ❌ | Chờ T4-01 |
| M4-01 | Tích hợp bản cải tiến | Nguyễn Văn Minh | Merge thay đổi có chọn lọc, demo case thường/khó, test luồng thật; changelog mô tả một nhóm lỗi mục tiêu | ❌ | |
| T4-02 | Chạy Eval Run 2 | Tạ Tiến Dũng | Toàn bộ cùng benchmark, eval/run-2.csv và traces/run-2.jsonl, run ID/model/token thật | ❌ | BLOCKER: chờ M4-01 |
| T4-03 | Chấm và so sánh Run 2 | Tạ Tiến Dũng | Điền pass, ghi chú, chạy score; report và README có số lượt 1/2, đủ metric, nhóm lỗi cải thiện và lỗi còn lại/tệ đi | ❌ | BLOCKER: chờ T4-02 |
| T4-04 | Chốt personas và giá | Tạ Tiến Dũng | >=3 persona, share tổng 1, số người dùng/tần suất có nguồn hoặc ghi tự ước tính; >=2 mức model có nguồn giá/ngày | ✅ | 28/11: cost/personas.yaml & cost/cost-estimate.md §1 chốt users đúng vai 22/84/168 (GV+lab coach), 3 persona share=1.00, 3 tầng model từ further-reading/model-prices.md (25/11/2026); kiểm load_config() 0 cảnh báo |
| T4-05 | Mô phỏng >=50 phiên thật | Tạ Tiến Dũng | Seed cố định; qua answer thật; CSV và trace có token in/out, lượt gọi, latency, model; không tính mock | ❌ | BLOCKER: chờ M3-04/M4-01 và T4-03; đã kiểm plan_sessions 50 phiên seed=42 |
| T4-06 | Chi phí và quy mô | Tạ Tiến Dũng | cost-estimate.md có thấp/cơ sở/cao, >=2 mức model, chi phí/task thành công = trung bình phiên chia tỷ lệ đạt lượt 2; ghi giới hạn nếu giá ước tính | ❌ | Đã hoàn thiện §1 đầu vào; BLOCKER: chờ T4-05 và tỷ lệ đạt Run 2 (T4-03) để điền §2–§3 |
| M4-02 | Impact so với chi phí | Nguyễn Văn Minh | Spec §8 và cost-estimate có so sánh chi phí/người/tháng với impact cùng đơn vị hoặc giải thích quy đổi, kết luận go/iterate/stop có căn cứ | ❌ | Chờ T4-06 |
| B4-02 | Hồ sơ an toàn | Hoàng Văn Bảo | §9 mô tả ẩn danh, quyền, rủi ro, giới hạn; test guardrails có kết quả thật | ❌ | |
| B4-03 | Người dùng thử (bonus) | Hoàng Văn Bảo | 2–3 người ngoài nhóm đúng vai, khoảng 10 phút/người, log hành vi và trích dẫn thật, tổng hợp 4 ý | ❌ | Không thay thế evidence pain |
| D4-02 | Chuẩn bị demo AI Core | Nguyễn Đức Đạt | Case thường và khó chạy thật; giải thích quyết định, dữ liệu, tool, trace và giới hạn | ❌ | |
| M4-03 | Slide demo | Nguyễn Văn Minh | 8 phần theo guide §5.1, mỗi trang có số/trích dẫn có nguồn/kết quả; cả nhóm bổ sung nội dung phụ trách; file hoặc link mở được | ❌ | |
| M4-04 | Video dự phòng và phòng demo | Nguyễn Văn Minh | Video thật mở ẩn danh được; xác nhận phòng/zone; kịch bản demo có case thường và khó, phân vai phát biểu | ❌ | |
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
| F-08 | Reflection cá nhân | Tạ Tiến Dũng | reflection/ta-tien-dung.md có đủ nội dung theo guide | ❌ | BLOCKER: câu 3 yêu cầu 1 câu thử trượt thật của nhóm (chờ Run 1, không bịa lỗi) |
| F-09 | Xử lý phản hồi demo | Nguyễn Văn Minh | Điều phối sửa lỗi đã thống nhất, ghi giờ/đổi gì/vì sao vào §10; lượt chạy bổ sung ghi run mới | ❌ | Cả nhóm hỗ trợ |
| F-10 | Khóa bản nộp cuối | Nguyễn Văn Minh | Repo đủ hồ sơ, không secret/dữ liệu cá nhân, link công khai, main đã push trước 23:59; không sửa lịch sử eval | ❌ | |

## 7. Phối hợp và đường găng

- M3-01 phải thống nhất trước; sau đó Đạt D3-01–09, Bảo B3-01–09, Dũng T3-01–05/T3-10 và Minh M3-02/M3-07–11 làm song song.
- D3-10 + B3-10 -> M3-03 -> M3-04 -> T3-06/07/08/09 -> M3-14. Video M3-13 và simulate thử T3-11 có thể chạy sau M3-04 song song, tránh vượt quota.
- M3-05/06 là phần giao diện; nếu không kịp, ưu tiên CLI chạy thật đầy đủ, ghi rõ phần web chưa xong. Không trì hoãn eval vì UI.
- CP4: T4-01 -> D4-01/B4-01 (chỉ sửa nhóm lỗi đã chọn) -> M4-01 -> T4-02/03 -> T4-06/M4-02 -> M4-05.
- Mỗi người làm trên nhánh của mình, cập nhật từ main, mở PR có test/ghi chú. Tránh sửa cùng một file; Minh điều phối merge. Không force push main. Không merge lại PR chứa phongvan.md bị loại.
- Hạn nội bộ đề xuất: trước 02:00 AI gọi thật + contract; trước 07:30 tích hợp; trước 09:00 Run 1 và chấm; trước 09:30 video/hồ sơ; nộp trước 10:00. Đây là mốc điều phối đề xuất, không phải deadline bổ sung của BTC.
