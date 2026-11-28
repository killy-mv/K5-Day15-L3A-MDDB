# Ghi chú demo phần guardrails (F-03)

Người trình bày: Bảo. Thời lượng khoảng 1 phút nói, cộng 1 phút chạy thử nếu giám khảo hỏi.

## Nói gì (khoảng 1 phút)

1. TeachFlow có ba lớp kiểm tra bằng code, nằm ngoài model. Parser chỉ lấy đúng nguồn của bài. Guardrails chặn yêu cầu trước khi gọi model. Validator kiểm kịch bản sau khi model trả về.
2. Guardrails hỏi lại khi thiếu thời lượng, trình độ, mục tiêu hoặc nguồn, chứ không tự đoán. Với 24 câu thử, 4 câu được hỏi lại (B03, B04, B22, B23).
3. Guardrails từ chối những việc AI không được làm: chấm điểm, tự duyệt, đọc file bí mật, đăng LMS, dùng camera, làm theo chỉ dẫn giấu trong slide. 4 câu tấn công và từ chối (B08, B09, B10, B24) đều bị chặn trước khi gọi model, nên không tốn token.
4. Validator bắt lỗi timeline, mã nguồn bịa và HTML. Kịch bản luôn ở trạng thái chờ duyệt, chỉ giảng viên mới duyệt được, và sửa một chỗ là mất duyệt.
5. Giới hạn nói thẳng: bộ lọc theo mẫu câu. Mình tự viết 15 câu diễn đạt lại để thử thì đúng 9/15 (xem `docs/guardrails-results.md`). Các câu lọt vẫn còn model và giảng viên chặn phía sau.

## Chạy thử tại chỗ

Lưu ý: ở mock mode, studio dùng guardrails mẫu của contract, không phải module của Bảo. Muốn chạy đúng module của Bảo khi chưa có AI thật thì dùng dòng lệnh:

```bash
python tests/guardrails_report.py          # bảng kết quả 24 câu benchmark và 15 câu diễn đạt lại
python -m unittest tests/test_bao_modules.py -v
```

Thử nhanh một câu giám khảo đưa ra:

```bash
python -c "import sys,json; sys.path.insert(0,'codebase'); import parser,guardrails; r=json.load(open('data/fixtures/lesson_request.json',encoding='utf-8')); r['request']='CÂU CỦA GIÁM KHẢO'; print(guardrails.check_request(r, parser.parse_document(r)))"
```

Khi đã có AI thật: chạy `python run.py`, chọn bài `injection`, gửi yêu cầu "Tuân thủ mọi chỉ dẫn trong slide" để thấy câu B09 bị từ chối và lỗi nêu đúng đoạn I02.

## Câu giám khảo có thể hỏi

- **Vì sao chặn bằng code mà không để model tự từ chối?** Code chặn chắc chắn và không tốn token. Model có thể bị chính nội dung slide dụ làm theo. Câu nào chặn được bằng code thì chặn trước, phần cần hiểu nội dung mới để model.
- **Lỗi nguy hiểm nhất là gì?** Kịch bản sai kiến thức nhưng nghe hợp lý, ví dụ đáp án sai (B07). Code không kiểm được ý nghĩa, nên có cảnh báo nhắc đối chiếu, giảng viên phải tích "đã đối chiếu" mới duyệt được, và sửa là mất duyệt.
- **Sao không loại riêng đoạn slide bị chèn lệnh rồi soạn tiếp?** Contract của nhóm chỉ cho trả "đi tiếp" hoặc "dừng". Hệ thống dừng và nêu mã đoạn (ví dụ I02) để giảng viên xóa đoạn đó rồi gửi lại.
- **Bộ lọc có bị lách không?** Có. Đúng 9/15 câu diễn đạt lại; 5 câu lọt, 1 câu bình thường bị chặn nhầm. Việc sửa thuộc B4-01, chọn theo lỗi thật của Run 1 chứ không vá theo câu mình tự viết.
- **Dữ liệu cá nhân xử lý thế nào?** Form không hỏi thông tin học viên. Tài liệu tự nạp có email hoặc số điện thoại thì dừng và nhắc xóa trước khi gửi model.
