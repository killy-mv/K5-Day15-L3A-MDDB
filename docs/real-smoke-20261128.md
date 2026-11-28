# Smoke tích hợp AI thật — 28/11/2026

- Người thực hiện: Nguyễn Văn Minh, với hỗ trợ ChatGPT chạy lệnh.
- Code cơ sở: main 4b2bc6f (AI Core PR #8 c987074), nhánh NguyenVanMinh.
- Cấu hình local: MODEL_PROVIDER=gemini, MODEL_NAME=gemini-3.8-flash, TEACHFLOW_MODE=real, API key riêng (không lưu key vào repo). Chưa ghi quota thực tế.
- Lệnh: `python tests/smoke_real_studio.py --run-real`.
- Thời lượng job gồm kiểm tra cấu hình và hai case: 82,527 giây; exit code 0.
- Smoke kiểm status pending_review, generation_mode real, validator, budget model calls, token dương, tool calls và không có lỗi trace. Đây không phải Evaluation Run 1 hoặc chấm grounding/ngữ nghĩa.

## Output stdout thực tế

```text
provider: gemini model: gemini-3.8-flash key configured: True mode: real
B11 model_calls= 1 tool_calls= 2 tokens_in= 1662 tokens_out= 2658
B05 model_calls= 1 tool_calls= 2 tokens_in= 1696 tokens_out= 3061
PASS: real normal/difficult structural smoke. Semantic quality and repair budget still require review.
```

Tổng 3.358 input tokens và 5.719 output tokens = 9.077 token, 2 model calls, 4 tool calls. B11 và B05 đều không cần repair. Lệnh chỉ in thống kê, không lưu bản nháp hoặc trace events ra file, không ghi run ID eval. Tên model ở trên là cấu hình local; không có modelVersion cụ thể trong stdout. Chưa kiểm thử qua browser với output LLM thật; chưa xác minh chất lượng nội dung. Không sửa chuẩn CP2 hoặc benchmark, không dùng kết quả này để chấm Run 1.

## Browser smoke thật M3-05 (lượt riêng sau PR #12)

Lệnh: `python tests/browser_studio_real.py --run-real`. Code cơ sở main 30277dd, nhánh NguyenVanMinh. Edge headless, backend Python local, nguồn lab_tools. Test sử dụng API thật, không thay model bằng fixture; chỉ bọc tracing.end để thu thống kê. Job exit 0, 30,785 giây toàn job.

Stdout thực tế:

```json
{"result": "PASS", "configured_model": "gemini-3.8-flash", "models": ["gemini-3.8-flash"], "segments": 5, "duration_minutes": 60, "sources": 5, "warnings": 4, "model_calls": 1, "tool_calls": 2, "tokens_in": 1666, "tokens_out": 2996, "missing_context_model_calls": 0, "elapsed_seconds": 28.6}
```

Kiểm UI nhận bản nháp pending_review, hiển thị 5 hoạt động và validation đạt, nguồn/cảnh báo, khóa duyệt trước checkbox, mở reader sau duyệt, JSON khớp segments, sửa làm mất duyệt/đóng reader, hỏi lại thiếu duration không gọi model, không lỗi JavaScript. Tổng 4.662 token. Phép thử xác nhận chức năng, thao tác duyệt tự động trong test không phải đánh giá chuyên môn của giảng viên. Không lưu output/trace events hoặc chấm Run 1. Không thay đổi benchmark hay metric.
