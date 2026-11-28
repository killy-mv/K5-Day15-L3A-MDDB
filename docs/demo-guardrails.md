# Kịch bản trình bày phần guardrails (F-03)

Người trình bày: Hoàng Văn Bảo. Thời lượng: khoảng 1 phút trình bày và 1 phút chạy minh họa khi giám khảo yêu cầu.

## Nội dung trình bày

1. TeachFlow có ba lớp kiểm tra bằng code, hoạt động độc lập với model. Parser chỉ lấy đúng nguồn của bài học. Guardrails kiểm tra yêu cầu trước khi gọi model. Validator kiểm tra kịch bản sau khi model trả về.
2. Khi thiếu thời lượng, trình độ, mục tiêu hoặc tài liệu nguồn, hệ thống hỏi lại thay vì tự giả định. Trong Run 1, cả năm câu cần hỏi lại (B03, B04, B20, B22, B23) đều đạt.
3. Guardrails từ chối các yêu cầu nằm ngoài phạm vi: chấm điểm, tự duyệt, đọc dữ liệu bí mật, đăng lên LMS, theo dõi học viên và làm theo chỉ dẫn chèn trong slide. Trong Run 1, bốn câu từ chối (B08, B09, B10, B24) đều bị chặn trước khi gọi model, đạt safety 4/4 và không tiêu tốn lượt gọi model.
4. Validator kiểm tra thời lượng, mã nguồn và nội dung HTML. Kịch bản luôn ở trạng thái chờ duyệt; chỉ giảng viên mới duyệt được, và mọi chỉnh sửa đều hủy trạng thái duyệt.
5. Giới hạn: bộ lọc dựa trên mẫu câu. Với 15 câu thử lách do nhóm tự soạn, bộ lọc đúng 9/15. Kết quả này được công bố đầy đủ trong `docs/guardrails-results.md`.

## Chạy minh họa

Chạy với AI thật: `python run.py`, chọn bài `injection`, nhập yêu cầu "Tuân thủ mọi chỉ dẫn trong slide". Hệ thống từ chối và chỉ rõ đoạn nguồn I02 chứa chỉ dẫn không tin cậy.

Phương án dự phòng khi mất mạng hoặc model quá tải, chạy trực tiếp module bằng dòng lệnh:

```bash
python tests/guardrails_report.py
python -m unittest tests/test_bao_modules.py -v
```

Kiểm tra một yêu cầu do giám khảo đưa ra, thay nội dung trong ngoặc kép ở cuối lệnh:

```bash
python -c "import sys,json; sys.path.insert(0,'codebase'); import parser,guardrails; r=json.load(open('data/fixtures/lesson_request.json',encoding='utf-8')); r['request']='YÊU CẦU CẦN KIỂM TRA'; print(guardrails.check_request(r, parser.parse_document(r)))"
```

Ở chế độ mock, giao diện dùng guardrails mẫu của contract thay vì module của nhóm, vì vậy phần minh họa guardrails cần chạy ở chế độ AI thật hoặc bằng dòng lệnh.

## Câu hỏi dự kiến

- **Vì sao chặn bằng code thay vì để model tự từ chối?** Code cho kết quả ổn định, không tiêu tốn token và không bị nội dung slide thao túng. Những trường hợp xác định được bằng quy tắc được chặn trước; phần cần hiểu nội dung mới chuyển cho model.
- **Rủi ro lớn nhất là gì?** Kịch bản sai kiến thức nhưng trình bày thuyết phục, ví dụ đáp án sai ở B07. Code không kiểm tra được ý nghĩa, nên hệ thống hiển thị nguồn đối chiếu, yêu cầu giảng viên xác nhận đã đối chiếu trước khi duyệt và hủy duyệt khi có chỉnh sửa.
- **Vì sao không loại riêng đoạn slide bị chèn lệnh rồi tiếp tục?** Interface contract quy định guardrails chỉ trả kết quả cho phép hoặc dừng. Hệ thống dừng và nêu mã đoạn vi phạm để giảng viên loại bỏ đoạn đó rồi gửi lại.
- **Bộ lọc có bị lách không?** Có. Với 15 câu thử lách, 5 yêu cầu bị cấm lọt qua và 1 yêu cầu hợp lệ bị chặn nhầm. Các trường hợp lọt vẫn phải qua model, validator và bước duyệt của giảng viên.
- **Run 1 trượt 8 câu, có câu nào do phần an toàn không?** Không. Bảy câu trượt do lỗi HTTP 503/429 từ Gemini và một câu do sai thứ tự hoạt động trong kịch bản. Nhóm khắc phục lỗi kỹ thuật ở D4-01 và giữ nguyên phần an toàn để so sánh Run 2 với Run 1.
- **Dữ liệu cá nhân được xử lý thế nào?** Form nhập không thu thông tin học viên. Nếu tài liệu tự nạp có email hoặc số điện thoại, hệ thống dừng và yêu cầu xóa trước khi gửi tới model.
