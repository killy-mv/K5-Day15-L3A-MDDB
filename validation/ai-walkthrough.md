# Rà soát giao diện bằng AI đóng vai người dùng

Ngày thực hiện: 28/11/2026. Người tổng hợp: Hoàng Văn Bảo.

## Phạm vi và phương pháp

Đây là bản rà soát giao diện do AI thực hiện, **không phải phiên người dùng thử** và không được tính cho B4-03. Ba agent Claude Code đóng ba vai người dùng, điều khiển giao diện `codebase/studio.html` bằng Playwright trên Microsoft Edge ở chế độ mock. Phiên bản được kiểm tra là commit `6b40822`, trước khi PR #7 (`fd4d698`) cập nhật `studio.html`; vì vậy các lỗi giao diện cần được kiểm tra lại trên phiên bản hiện tại. Tài liệu không chứa câu nói của người thật; mọi trích dẫn là chữ hiển thị trên giao diện.

Mục đích: phát hiện lỗi giao diện trước demo và xác định các điểm cần quan sát trong phiên người dùng thử thật (`validation/kich-ban-phien-thu.md`).

| Vai | Nhiệm vụ |
|---|---|
| Giảng viên OOP nhiều kinh nghiệm, thận trọng với AI; lớp 40 người, offline, 45 phút | Soạn kịch bản phần lớp Customer, duyệt, sau đó chỉnh sửa lời dẫn |
| Lab coach cần làm nhanh; lớp online 60 người, 30 phút | Sinh và duyệt kịch bản nhanh; yêu cầu công cụ chấm điểm và xếp hạng lớp |
| Giảng viên dùng tài liệu riêng; lớp 35 người, 60 phút | Nạp file Markdown có chèn một email giả và một câu ra lệnh cho AI |

## Lỗi phát hiện

| # | Mô tả | Mức độ | Vai phát hiện | Phụ trách |
|---|---|---|---|---|
| 1 | Ở chế độ mock, giao diện dùng guardrails mẫu của contract nên không chặn yêu cầu "Chấm điểm luôn bài lab và xếp hạng cả lớp", không phát hiện email và câu "bỏ qua mọi hướng dẫn trước đó" trong tài liệu tự nạp. Với cùng dữ liệu, `codebase/guardrails.py` chặn đúng (`GRADING`, `INJECTION_SOURCE`, `PERSONAL_DATA_SOURCE`). | Cao khi demo ở chế độ mock | Lab coach, tài liệu riêng | Khắc phục khi chạy chế độ AI thật; phương án demo trong `docs/demo-guardrails.md` |
| 2 | Sau khi chỉnh sửa bản đã duyệt, trạng thái chuyển về "Chờ duyệt" nhưng thông báo "Phiên bản đã được giảng viên duyệt." vẫn hiển thị. Lỗi vẫn còn trong mã hiện tại: hàm `invalidate()` không xóa thông báo cũ. | Cao | Giảng viên OOP, lab coach | Nguyễn Văn Minh (`studio.html`) |
| 3 | Khi chỉnh sửa, màn hình riêng tự đóng mà không thông báo; thay đổi một trường thông tin lớp làm mất toàn bộ bản nháp đã chỉnh sửa mà không hỏi xác nhận. | Cao | Giảng viên OOP | Nguyễn Văn Minh |
| 4 | Thông báo thiếu thông tin dùng tên trường kỹ thuật (`duration_minutes`, `class_size`, `objectives`) thay vì nhãn trên form ("Phút", "Số học viên", "Mục tiêu học tập"); ô còn thiếu không được đánh dấu. | Vừa | Cả ba vai | Nguyễn Văn Minh |
| 5 | Form điền sẵn 60 phút, 40 học viên, offline, "Máy chiếu và laptop"; người dùng không chỉnh sửa sẽ nhận kịch bản sai bối cảnh. | Vừa | Cả ba vai | Nguyễn Văn Minh |
| 6 | Nút Duyệt bị khóa nhưng không nêu lý do; giao diện không thông báo rằng nội dung đã chỉnh sửa cần được duyệt lại; người dùng có thể xác nhận "đã đối chiếu" mà không mở phần nguồn. | Vừa | Giảng viên OOP, lab coach | Nguyễn Văn Minh |
| 7 | Chức năng tải file chỉ hoạt động sau khi chọn "Nội dung tự nhập", nhưng giao diện không hướng dẫn; lựa chọn này nằm cuối danh sách. | Vừa | Tài liệu riêng | Nguyễn Văn Minh |
| 8 | Mock giới hạn 12 đoạn nguồn mà không thông báo và tách mỗi dòng, kể cả tiêu đề, thành một đoạn. | Vừa, chỉ ở chế độ mock | Tài liệu riêng | Khắc phục khi chạy chế độ AI thật với `codebase/parser.py` |
| 9 | Kết quả kiểm tra thời lượng cập nhật chậm: trong lúc chỉnh sửa vẫn hiển thị "đạt", chỉ khi rời ô nhập mới hiện "Tổng 50 phút, cần 45 phút." | Vừa | Giảng viên OOP | Nguyễn Văn Minh |
| 10 | Cảnh báo của mock lẫn tiếng Anh, ví dụ "Structural check only; human must check meaning and grounding." | Thấp | Cả ba vai | Nguyễn Văn Minh |
| 11 | Khi một đoạn nguồn vừa chứa câu ra lệnh vừa chứa email, `codebase/guardrails.py` chỉ báo lỗi câu ra lệnh; giảng viên phải gửi lại lần thứ hai mới biết còn dữ liệu cá nhân. | Thấp | Tài liệu riêng | Hoàng Văn Bảo |

## Chức năng hoạt động đúng

- Chưa xác nhận quyền sử dụng nguồn thì không sinh được kịch bản, kèm thông báo "Xác nhận quyền sử dụng nguồn trước."
- Chưa xác nhận "đã đối chiếu" thì không duyệt được; mọi chỉnh sửa đều hủy trạng thái duyệt và khóa các nút xuất.
- Thay đổi thông tin lớp sẽ hủy bản nháp cũ, kèm thông báo "Context đã thay đổi. Sinh lại kịch bản trước khi duyệt."
- Màn hình riêng ghi rõ không trình chiếu cho học viên; giao diện thông báo trung thực khi đang chạy chế độ mock.
- Không phát sinh lỗi JavaScript; mọi API trả mã 200.
- `codebase/parser.py` chia đúng 6 đoạn theo tiêu đề cho file Markdown tự nạp.

## Đề xuất cho phiên người dùng thử

Giao nhiệm vụ tập trung vào các điểm trên để kiểm tra người dùng thật có gặp khó khăn tương tự không: nhập thiếu thông tin (lỗi 4), chỉnh sửa sau khi duyệt (lỗi 2, 3, 6) và nạp tài liệu riêng (lỗi 7).

Ảnh chụp màn hình và script kiểm thử được lưu ngoài repo.
