# B4-03 — Nhật ký người dùng thử

**Trạng thái: 2 phiên với người dùng thử đã được ghi nhận** (mục tiêu 2–3 người, khoảng 10 phút mỗi người). Người thử là hai học viên AI20K ngoài nhóm MDDB, mỗi phiên khoảng 7 phút. Cả hai tự thao tác trên TeachFlow Studio, chế độ mock, bài `oop_annotations`. Quy trình theo [guide §4.3](../02-guide.md#b4-3) và [kịch bản phiên thử](kich-ban-phien-thu.md).

## Kết quả từng phiên

| Người thử (vai) | Việc giao | Quan sát | Trích nguyên văn | Mức nghiêm trọng |
|---|---|---|---|---|
| Học viên AI20K ngoài nhóm, nhận vai giảng viên OOP | Chuẩn bị kịch bản Customer cho lớp 40 người trong 45 phút, có bài tập theo cặp và đáp án. | Người thử chỉnh thời lượng từ 60 xuống 45 phút, chọn slide `OOP-P041` và nhập bốn chặng 5/10/20/10 phút. Studio trả về một hoạt động duy nhất dài 45 phút. Người thử mở nguồn để kiểm tra ràng buộc `id` và độ dài tên, rồi tự thêm đề, đáp án và các mốc vào lời dẫn. File Markdown giữ phần đã sửa. Màn hình đứng lớp chỉ có đồng hồ `45:00` và nút "Tiếp" bị khóa. | "Tôi dùng được tệp này làm ghi chú. Đến lúc chữa bài, tôi vẫn phải tự canh giờ vì màn hình chỉ có một chặng." | Vừa: người thử phải tự soạn bài tập và tự theo dõi từng chặng. |
| Học viên AI20K ngoài nhóm, nhận vai lab coach | Chuẩn bị kịch bản Customer 45 phút, sau đó yêu cầu công cụ chấm bài lab cho cả lớp. | Người thử chỉnh thời lượng xuống 45 phút và xác nhận quyền sử dụng nguồn. Khi bỏ trống ô "Phút", thông báo gọi trường này là `duration_minutes`. Người thử điền lại, mở nguồn, xem cảnh báo, duyệt và xuất Markdown. Sau đó người thử nhập yêu cầu chấm bài vào ô "Yêu cầu bổ sung"; Studio trả về một kịch bản mock mới ở trạng thái chờ duyệt, không có thông báo nào về yêu cầu chấm bài. | "Tôi vừa yêu cầu chấm bài mà lại nhận một kịch bản mới. Tôi không biết công cụ đã bỏ qua yêu cầu hay tôi nhập sai chỗ." | Cao: người dùng không biết yêu cầu chấm bài đã được xử lý thế nào. |

**Câu trả lời sau phiên** ("Nếu mai không dùng được nữa, bạn thấy rất tiếc, hơi tiếc hay không sao?"): Rất tiếc 0 · Hơi tiếc 0 · Không sao 2 · Tổng số câu trả lời 2.

### Trả lời phỏng vấn sau phiên

**Người thử 1, vai giảng viên OOP:** "Tôi sẽ dùng để chuẩn bị, nhưng chưa dùng màn hình đứng lớp cho buổi tới. Tôi muốn đưa cho 20 cặp một đề bài rõ ràng và biết lúc nào cần chuyển sang chữa bài. Mục đối chiếu giúp tôi kiểm tra ngay vì sao `id = 0` sai và tên dài 51 ký tự vượt giới hạn. Tôi tin hai đáp án sau khi tự kiểm tra với slide. Chỗ tôi vướng nhất là đã nhập bốn chặng mà đồng hồ vẫn chỉ có một mốc 45 phút. Với buổi tới, tôi sẽ dùng tệp Markdown đã sửa làm ghi chú và tự canh giờ."

**Người thử 2, vai lab coach:** "Tôi sẽ thử lại để chuẩn bị lab nếu bản nháp có bài tập đủ cụ thể. Tôi mở được nguồn và xuất được bản nháp, nhưng chỉ dẫn 'Nêu lại ý chính' chưa đủ để tôi giao việc cho cả lớp. Điều khó hiểu nhất là sau khi yêu cầu chấm bài, tôi vẫn nhận một kịch bản mới. Tôi biết bản nào vừa được tạo, nhưng không biết công cụ xử lý yêu cầu chấm điểm ra sao. Nếu chấm điểm nằm ngoài phạm vi, tôi muốn được báo ngay để chuyển sang bước khác. Với buổi lab tiếp theo, tôi chỉ dùng phần kịch bản sau khi đã sửa bài tập và kiểm tra đáp án."

## Tổng hợp

- **Chủ đề lặp nhiều nhất:** cả hai người thử đều mở được nguồn đối chiếu và xuất được Markdown, nhưng khi yêu cầu vượt khung mock (bốn chặng thời gian, yêu cầu chấm bài), Studio vẫn trả bản nháp mà không chỉ ra phần nào của yêu cầu chưa được đáp ứng. Cả hai đều trả lời "không sao" nếu không còn dùng công cụ, cho thấy bản mock chưa đủ giá trị để thay đổi cách chuẩn bị bài hiện tại.
- **Sửa gì trước demo:** thông báo rõ giới hạn khi người dùng yêu cầu chấm bài; dùng nhãn "Phút" thay cho `duration_minutes` trong thông báo thiếu thời lượng; chạy lại đề bài bốn chặng ở chế độ AI thật trước khi dùng làm kịch bản demo. Các đề xuất này thuộc phần giao diện; thay đổi nào được thực hiện sẽ ghi vào [spec.md §10](../spec.md).
- **Giữ gì và vì sao:** giữ phần đối chiếu nguồn và xuất Markdown sau khi duyệt. Người thử 1 dùng phần đối chiếu để tự kiểm tra hai đáp án với slide và cho biết tin đáp án sau bước này.
- **Để dành sau:** chia kịch bản thành nhiều chặng có đồng hồ riêng trên màn hình đứng lớp; thử với giảng viên và lab coach đang đứng lớp thật để xem họ dùng các chặng thế nào.
