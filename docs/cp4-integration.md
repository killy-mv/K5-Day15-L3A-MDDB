# M4-01 — Nghiệm thu tích hợp CP4 (28/11/2026)

Bản code chung: main `87172d3`, gồm PR #15 (Đạt, e503cdf), #16 (Bảo, bd2fcf2), #17 (Dũng, 87172d3). Người phụ trách: Nguyễn Văn Minh, ChatGPT hỗ trợ chạy kiểm thử và tổng hợp.

## Nhóm lỗi mục tiêu
Run 1 trượt 8/24 câu: 7 lỗi thực thi HTTP 503/429 và B15 sai thứ tự hoạt động. PR #15 bổ sung retry tối đa 3 lần sau lần gọi đầu, exponential backoff/jitter, quy tắc giữ cấu trúc yêu cầu và gửi lại nguồn khi repair. PR #16 giữ nguyên lớp an toàn, bổ sung regression và hồ sơ; PR #17 bổ sung báo cáo mô phỏng thử. Conflict backlog đã giải quyết, giữ các dòng của từng thành viên. Benchmark, metric, kết quả và trace Run 1, harness không thay đổi.

## Kết quả kiểm thử
Bản Đạt+Bảo: 94/94 Python unit test pass, 23/23 studio JS và 15/15 prototype JS pass trên bản Đạt trước merge Bảo; run.py check pass cả sau PR #17.

Smoke trên bản tích hợp cuối, override MODEL_NAME=gemini-3.1-flash-lite và TEACHFLOW_MODE=real cho từng tiến trình, không đổi .env. Key local không ghi vào repo.

```bash
MODEL_NAME=gemini-3.1-flash-lite TEACHFLOW_MODE=real python tests/smoke_real_studio.py --run-real
MODEL_NAME=gemini-3.1-flash-lite TEACHFLOW_MODE=real python tests/browser_studio_real.py --run-real
```

| Case | Kết quả | Model calls | Tool calls | Input token | Output token |
|---|---|---:|---:|---:|---:|
| B11 thường | pending_review, validator pass | 1 | 2 | 2184 | 1324 |
| B05 khó | pending_review, validator pass | 1 | 2 | 2218 | 1209 |
| Browser lab_tools 60 phút | PASS | 1 | 2 | 2188 | 1389 |

CLI job exit 0, tổng 9,033 giây; browser job exit 0, tổng 9,369 giây (xử lý UI 6,35 giây). Browser: 4 hoạt động/60 phút, 5 nguồn, 5 cảnh báo; kiểm duyệt, reader, export JSON, sửa hủy duyệt, hỏi lại thiếu thời lượng (0 model calls), không lỗi JavaScript. Browser dùng yêu cầu tương tự B11, không phải input benchmark nguyên vẹn. 404 favicon không ảnh hưởng luồng. Không lưu output thô/trace mới hoặc chấm ngữ nghĩa; không dùng smoke làm Run 2.

## Bàn giao Run 2
Đề xuất cấu hình cố định cho lượt 2: Gemini, gemini-3.1-flash-lite, real, code main 87172d3, cùng 24 câu và rubric CP2. Dũng cần xác nhận quota/project và model trước chạy; đây là cấu hình đề xuất đã kiểm smoke, chưa có xác nhận cả nhóm. Run 1 dùng 3.8 Flash nên phải ghi rõ thay đổi model, không quy toàn bộ chênh lệch cho prompt/retry.

```bash
MODEL_PROVIDER=gemini MODEL_NAME=gemini-3.1-flash-lite TEACHFLOW_MODE=real python run.py eval --wait 12
python run.py score eval/run-2.csv
MODEL_PROVIDER=gemini MODEL_NAME=gemini-3.1-flash-lite TEACHFLOW_MODE=real python run.py simulate --wait 12 --rate-from eval/run-2.csv
```

Chỉ chạy score sau khi điền pass/ghi_chu theo rubric; simulate sau khi Run 2 đã chấm. Xác nhận tên file/run ID thực tế, không ghi đè lượt cũ. Không tự chuyển mock hoặc bỏ case trượt. Retry hiện vẫn thử lại mọi 429, chưa phân biệt quota ngày; timeout mỗi HTTP attempt 90 giây, tổng có thể dài. Không chứng minh đã khắc phục hết 503/429. Hạn chế số lần gọi theo quota thật và ghi lỗi nếu thiếu. T3-11 có báo cáo 10 phiên, chưa có CSV/trace thử trên repo; không thay cho 50 phiên.
