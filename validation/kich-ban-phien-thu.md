# Kịch bản phiên người dùng thử (B4-03, bonus)

Chuẩn bị theo guide mục 4.3. Ghi kết quả vào `validation/log.md`. Không ghi tên người thử, chỉ ghi vai. Chỉ ghi những gì thật sự quan sát và nghe được.

## Chọn người thử

Cần 2 đến 3 người ngoài nhóm, đúng vai người dùng của TeachFlow: giảng viên hoặc lab coach. Với track A thì học viên khóa AI20K cũng dùng được, nhưng nên ưu tiên người đã từng đứng lớp hoặc hướng dẫn lab. Mỗi phiên khoảng 10 phút.

## Chuẩn bị máy

- Chạy `python run.py`, mở trang studio. Nếu chưa có AI thật thì nói rõ với người thử đây là bản mock.
- Chọn sẵn bài `oop_annotations`.
- Chuẩn bị file ghi chép, đồng hồ bấm giờ.

## Năm bước của một phiên

1. **Làm quen (khoảng 1 phút):** "Tụi mình đang thử sản phẩm, không đánh giá bạn. Bạn cứ nói to những gì bạn nghĩ trong lúc dùng."
2. **Bối cảnh (khoảng 1 phút):** "Lần gần nhất bạn chuẩn bị lời giảng hoặc kịch bản cho một buổi dạy, bạn đã làm những gì? Mất bao lâu?"
3. **Giao việc (khoảng 1 phút):** giao theo kết quả, không chỉ nút bấm. Người thử tự cầm chuột.
   - Việc 1: "Bạn có 45 phút dạy lớp 40 người phần thiết kế lớp Customer. Hãy dùng công cụ này để có một kịch bản bạn dám mang lên lớp."
   - Việc 2 (nếu còn thời gian): "Bạn muốn công cụ chấm điểm luôn bài lab cho cả lớp. Bạn thử xem."
4. **Quan sát (khoảng 5 phút):** im lặng và ghi lại:
   - bấm vào đâu đầu tiên;
   - chỗ nào dừng lại hoặc do dự quá 5 giây;
   - có đọc phần nguồn và cảnh báo không, hay duyệt luôn;
   - có sửa nội dung trước khi duyệt không;
   - với việc 2, có hiểu vì sao bị từ chối không.
   Nếu người thử bị kẹt, chỉ hỏi: "Bạn định làm gì tiếp?" hoặc "Bạn nghĩ nó nên hoạt động thế nào?". Không giải thích, không hỏi "bạn có thích không".
5. **Hỏi sau (khoảng 2 phút):**
   - Chỗ nào khó hiểu nhất?
   - Bạn có tin kịch bản này không? Vì sao?
   - Bạn có dùng thật cho buổi dạy tới không?
   - "Nếu mai không được dùng nữa, bạn thấy: rất tiếc, hơi tiếc hay không sao?"

## Ghi vào log

Mỗi người một dòng trong `validation/log.md`: vai, việc giao, quan sát, câu nói nguyên văn, mức nghiêm trọng (cao, vừa, thấp). Sau đó điền 4 dòng tổng hợp ở cuối file. Nếu sửa gì trước demo thì ghi thêm vào `spec.md` §10.

Lưu ý: toàn lời khen nghĩa là phiên chưa đạt, nên giao việc khó hơn. Người dùng thử không thay được bằng chứng pain trong `evidence/`.
