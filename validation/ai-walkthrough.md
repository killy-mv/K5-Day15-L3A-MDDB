# Rà soát giao diện bằng AI đóng vai người dùng (28/11/2026)

> Đây **không phải** phiên người dùng thử thật và không tính cho B4-03. Ba agent AI (Claude Code) đóng ba vai, điều khiển giao diện `codebase/studio.html` bằng Playwright trên Edge, ở mock mode (chưa có AI thật). Không có câu nói nào của người thật trong file này; phần trích dẫn chỉ là chữ trên giao diện. Mục đích: tìm lỗi giao diện trước demo và chuẩn bị việc giao cho phiên thử thật (`validation/kich-ban-phien-thu.md`).

| Vai AI đóng | Việc giao |
|---|---|
| Giảng viên OOP lâu năm, hơi nghi ngờ AI; lớp 40 người, offline, 45 phút | Soạn kịch bản phần lớp Customer, duyệt, rồi sửa lời dẫn |
| Lab coach đang vội; lớp online 60 người, 30 phút | Sinh và duyệt thật nhanh; đòi công cụ chấm điểm và xếp hạng lớp |
| Giảng viên dùng tài liệu riêng; lớp 35 người, 60 phút | Nạp file Markdown tự soạn có cài một email giả và một câu ra lệnh cho AI |

## Lỗi tìm được

| # | Lỗi | Mức | Vai phát hiện | Ai sửa |
|---|---|---|---|---|
| 1 | Ở mock mode, web dùng guardrails mẫu của contract nên **không chặn** yêu cầu "Chấm điểm luôn bài lab và xếp hạng cả lớp", không phát hiện email và câu "bỏ qua mọi hướng dẫn trước đó" trong tài liệu tự nạp. Module `guardrails.py` chạy cùng dữ liệu bằng dòng lệnh thì chặn đúng (`GRADING`, `INJECTION_SOURCE`, `PERSONAL_DATA_SOURCE`) | Cao khi demo | lab coach, tài liệu riêng | Hết khi chạy real mode; demo mock thì dùng dòng lệnh (`docs/demo-guardrails.md`) |
| 2 | Sửa nội dung sau khi duyệt: trạng thái đã về "Chờ duyệt" nhưng dòng "Phiên bản đã được giảng viên duyệt." vẫn còn | Cao | giảng viên OOP, lab coach | Minh (`studio.html`) |
| 3 | Sửa nội dung thì màn hình riêng tự đóng, không báo; đổi một ô thông tin lớp là mất cả bản nháp đã sửa tay, không hỏi xác nhận | Cao | giảng viên OOP | Minh |
| 4 | Thông báo thiếu thông tin dùng tên trường tiếng Anh (`duration_minutes, class_size, objectives`) trong khi nhãn form là "Phút", "Số học viên", "Mục tiêu học tập"; ô thiếu không được tô đỏ | Vừa | cả ba | Minh |
| 5 | Form điền sẵn 60 phút, 40 người, offline, "Máy chiếu và laptop"; người vội không sửa thì kịch bản sai bối cảnh | Vừa | cả ba | Minh |
| 6 | Nút Duyệt bị khóa nhưng không ghi lý do; không có câu nào nói "đã sửa thì phải duyệt lại"; có thể tick "đã đối chiếu" mà không mở phần nguồn | Vừa | giảng viên OOP, lab coach | Minh |
| 7 | Phải chọn "Nội dung tự nhập" mới tải được file, nhưng giao diện không nói; lựa chọn này nằm cuối danh sách | Vừa | tài liệu riêng | Minh |
| 8 | Mock cắt còn 12 đoạn nguồn mà không báo, và mỗi dòng thành một đoạn kể cả tiêu đề | Vừa (chỉ mock) | tài liệu riêng | Hết khi chạy real mode với `parser.py` |
| 9 | Khung kiểm timeline cập nhật chậm: đang sửa phút vẫn ghi "đạt", rời ô mới hiện "Tổng 50 phút, cần 45 phút." | Vừa | giảng viên OOP | Minh |
| 10 | Cảnh báo lẫn tiếng Anh ("Structural check only; human must check meaning and grounding.") | Thấp | cả ba | Minh (mock) |
| 11 | Đoạn nguồn vừa có câu ra lệnh vừa có email thì `guardrails.py` chỉ báo câu ra lệnh, giảng viên phải gửi lại lần hai mới biết còn email | Thấp | tài liệu riêng | Bảo (B4-01) |

## Phần chạy đúng

- Chưa tick ô quyền thì không sinh được, thông báo rõ: "Xác nhận quyền sử dụng nguồn trước."
- Chưa tick "đã đối chiếu" thì không duyệt được; sửa nội dung thì mất duyệt thật, các nút xuất bị khóa lại.
- Đổi thông tin lớp thì bản nháp cũ bị bỏ: "Context đã thay đổi. Sinh lại kịch bản trước khi duyệt."
- Màn hình riêng ghi rõ không trình chiếu cho học viên; giao diện nói thật là đang chạy mock.
- Không có lỗi JavaScript; mọi API trả 200.
- `parser.py` chia đúng 6 đoạn theo tiêu đề cho file Markdown tự nạp.

## Gợi ý cho phiên thử thật

Giao việc vào đúng các chỗ trên để xem người thật có vướng không: nhập thiếu thông tin (lỗi 4), sửa sau khi duyệt (lỗi 2, 3, 6), nạp tài liệu riêng (lỗi 7).

Ảnh chụp và script nằm ở thư mục tạm của phiên làm việc, không đưa vào repo.
