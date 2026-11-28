# Kịch bản phiên người dùng thử (B4-03)

Kịch bản được xây dựng theo mục 4.3 của guide. Kết quả mỗi phiên được ghi vào `validation/log.md`. Người thử chỉ được ghi theo vai, không ghi tên; chỉ ghi nhận hành vi quan sát được và câu nói nguyên văn.

## Đối tượng

Hai đến ba người ngoài nhóm, đúng vai người dùng của TeachFlow: giảng viên hoặc lab coach. Với track A, học viên khóa AI20K cũng là người dùng hợp lệ; ưu tiên người đã từng giảng dạy hoặc hướng dẫn lab. Mỗi phiên kéo dài khoảng 10 phút.

## Chuẩn bị

- Khởi động `python run.py` và mở giao diện studio. Thông báo rõ cho người thử nếu phiên chạy ở chế độ mock.
- Chọn sẵn bài `oop_annotations`.
- Chuẩn bị biểu mẫu ghi chép và đồng hồ bấm giờ.

## Quy trình một phiên

1. **Giới thiệu (khoảng 1 phút):** "Chúng tôi đang đánh giá sản phẩm, không đánh giá bạn. Bạn hãy nói to suy nghĩ của mình trong khi sử dụng."
2. **Bối cảnh (khoảng 1 phút):** "Lần gần nhất bạn chuẩn bị lời giảng hoặc kịch bản cho một buổi dạy, bạn đã làm những gì và mất bao lâu?"
3. **Giao nhiệm vụ (khoảng 1 phút):** giao theo kết quả cần đạt, không hướng dẫn từng thao tác. Người thử tự sử dụng giao diện.
   - Nhiệm vụ 1: "Bạn dạy 45 phút cho lớp 40 người, nội dung thiết kế lớp Customer. Hãy dùng công cụ này để có một kịch bản bạn sẵn sàng mang lên lớp."
   - Nhiệm vụ 2, nếu còn thời gian: "Bạn muốn công cụ chấm điểm bài lab cho cả lớp. Hãy thử thực hiện."
4. **Quan sát (khoảng 5 phút):** không can thiệp, ghi nhận:
   - thao tác đầu tiên;
   - những điểm người thử dừng lại hoặc do dự quá 5 giây;
   - người thử có đọc nguồn đối chiếu và cảnh báo trước khi duyệt hay không;
   - người thử có chỉnh sửa nội dung trước khi duyệt hay không;
   - với nhiệm vụ 2, người thử có hiểu lý do bị từ chối hay không.

   Khi người thử gặp khó khăn, chỉ hỏi: "Bạn định làm gì tiếp theo?" hoặc "Theo bạn, công cụ nên hoạt động thế nào?". Không giải thích và không hỏi người thử có thích sản phẩm hay không.
5. **Phỏng vấn sau phiên (khoảng 2 phút):**
   - Điều gì khó hiểu nhất?
   - Bạn có tin tưởng kịch bản này không, vì sao?
   - Bạn có sử dụng cho buổi dạy tiếp theo không?
   - "Nếu ngày mai không thể dùng công cụ này nữa, bạn cảm thấy rất tiếc, hơi tiếc hay không sao?"

## Ghi nhận kết quả

Mỗi người thử tương ứng một dòng trong `validation/log.md`, gồm vai, nhiệm vụ, quan sát, câu nói nguyên văn và mức độ nghiêm trọng (cao, vừa, thấp). Sau các phiên, hoàn thành bốn dòng tổng hợp cuối file. Mọi thay đổi thực hiện trước demo được ghi vào `spec.md` §10.

Phiên chỉ nhận được lời khen là phiên chưa đạt yêu cầu; khi đó cần giao nhiệm vụ khó hơn. Kết quả người dùng thử không thay thế bằng chứng về pain trong `evidence/`.

Các điểm nên quan sát kỹ, rút từ bản rà soát giao diện `validation/ai-walkthrough.md`: thông báo khi nhập thiếu thông tin, trạng thái sau khi chỉnh sửa bản đã duyệt và cách nạp tài liệu riêng.
