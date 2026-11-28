# Kiểm thử AI Core với Gemini thật — 28/11/2026 (D3-01, D3-03, D3-09)

- Người thực hiện: Nguyễn Đức Đạt.
- Cấu hình local: `MODEL_PROVIDER=gemini`, API key riêng lưu tại `.env` local (`.gitignore` chặn commit, không lưu key vào repo), gói **Free tier** Google AI Studio.
- Model đã kiểm thử: `gemini-3.8-flash` (smoke test thành công, gặp HTTP 503 tạm thời do tải cao khi chạy sinh kịch bản) và `gemini-3.1-flash-lite` (chạy ổn định toàn bộ case thường, thiếu nguồn và mâu thuẫn nguồn).
- Lệnh chạy toàn bộ qua `codebase/agent.py` (`answer()` / `build_response()`) và `tests/smoke_real_studio.py --run-real`.

## Kết quả thực tế (không giả lập)

| Case | Đầu vào | Trạng thái trả về | Model | `model_calls` | `tool_calls` | `tokens_in` | `tokens_out` | Ghi chú |
|---|---|---|---|---:|---:|---:|---:|---|
| Smoke `D3-03` (`gemini-3.8-flash`) | `ai.call_model` câu chào ngắn | OK | `gemini-3.8-flash` | 1 | 0 | 20 | 196 | Có output và usage thật |
| Smoke `D3-03` (`gemini-3.1-flash-lite`) | `ai.call_model` câu chào ngắn | OK | `gemini-3.1-flash-lite` | 1 | 0 | 20 | 15 | Có output và usage thật |
| Case thường (`lesson_request.json`) | OOP 60 phút (`OOP-P040`, `P041`, `P104`, `P106`) | `pending_review` (3 segments, 60 phút) | `gemini-3.1-flash-lite` | 1 | 2 | 1890 | 1132 | Đạt validator ngay lượt đầu |
| Smoke tích hợp `B11` | Benchmark `B11` | `pending_review` | `gemini-3.1-flash-lite` | 1 | 2 | 1713 | 1053 | `tests/smoke_real_studio.py --run-real` PASS |
| Smoke tích hợp `B05` | Benchmark `B05` | `pending_review` | `gemini-3.1-flash-lite` | 1 | 2 | 1747 | 1151 | `tests/smoke_real_studio.py --run-real` PASS |
| Case mâu thuẫn nguồn (`conflict`) | `C01` vs `C02` mâu thuẫn trực tiếp | `needs_clarification` | `gemini-3.1-flash-lite` | 1 | 2 | 1544 | 114 | Chỉ rõ mâu thuẫn giữa `C01` và `C02`, không tự chọn một bên |
| Case thiếu nguồn | Yêu cầu Spring Security JWT chỉ cấp `OOP-P040` | `needs_clarification` | `gemini-3.1-flash-lite` | 1 | 2 | 1576 | 92 | Báo nguồn không chứa thông tin Spring Security/JWT |

## Kết quả kiểm thử tự động

- `python3 -m unittest discover -s tests`: **87/87 pass**.
- `python3 run.py check`: **0 cảnh báo**.
- Không commit `.env` hay bất kỳ API key nào vào repository.
