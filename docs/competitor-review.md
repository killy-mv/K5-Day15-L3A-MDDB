# M3-11 — Review giải pháp tương tự

Ngày nghiên cứu: 28/11/2026. Phương pháp: xem trang chức năng, FAQ, ví dụ đầu ra công khai và thử mở liên kết sinh mẫu. Không đăng nhập tài khoản cá nhân, không tải tài liệu OOP chưa rõ quyền lên dịch vụ bên ngoài. Đây là review tài liệu và mẫu công khai, không phải phép thử sinh mới cùng input hay kết quả đo chất lượng/latency của ba ứng dụng.

## MagicSchool — Lesson Plan Generator

- Nguồn: [Lesson Plan](https://www.magicschool.ai/tools/lesson-plan), [FAQ](https://www.magicschool.ai/faq).
- Quan sát: trang công cụ mô tả kế hoạch theo mục tiêu và chương trình. FAQ cho biết có thể chọn trình độ lớp, môn, mục tiêu, thời gian, nhu cầu phân hóa và sửa nội dung. Khi mở "See full generation", trang chuyển tới đăng nhập; không có output mới từ phiên review.
- Đáng học: thu thập context có cấu trúc, cho phép giáo viên sửa bản nháp.
- Điều tránh trong TeachFlow: mở rộng sang cả bộ công cụ quản trị, tài nguyên và trình chiếu; không dừng lại ở lesson plan tổng quát. Ưu tiên lời dẫn dùng trực tiếp và tham chiếu từng đoạn nguồn.

## Eduaide — 5E Lesson Plan Generator

- Nguồn: [5E Lesson Plan Generator](https://www.eduaide.ai/tools/5e-lesson-plan-generator), [Lesson Planning](https://www.eduaide.ai/solutions/lesson-planning), [Finalizing Your Resource & Model Selection](https://www.eduaide.ai/academy/fundamentals/finalizing-resource-model).
- Quan sát từ nội dung được lập chỉ mục công khai: ví dụ "Sink or Float? A 5E Sequence for 3rd Grade" trình bày mục tiêu, tiêu chí thành công, vật liệu và 5 pha. Các pha Engage/Explore/Explain/Elaborate/Evaluate có thời lượng tương ứng 20/45/30/35/30 phút. Mẫu Engage có câu hỏi gợi mở của giáo viên, nhiệm vụ học viên, kiểm tra hiểu và hỗ trợ phân hóa. Đây là mẫu nhiều buổi, không phải kịch bản AI20K đã chạy thử. Mở trực tiếp một số trang bị lỗi truy cập; thông tin lấy từ bản nội dung công khai được lập chỉ mục.
- Đáng học: phối hợp hành động giảng viên/học viên, câu hỏi gợi mở, phân hóa và kiểm tra hiểu theo từng hoạt động. Tài liệu hướng dẫn cũng mô tả đính kèm nguồn và chỉnh sửa tài liệu.
- Điều tránh trong TeachFlow: áp cứng một mô hình sư phạm hoặc kế hoạch nhiều buổi cho mọi lớp; chọn hoạt động theo context và thời lượng một buổi, giữ cấu trúc phù hợp nguồn.

## Diffit — tài nguyên phân hóa theo nội dung

- Nguồn: [FAQ](https://web.diffit.me/faq), [mẫu Inference and Sentence Structure](https://app.diffit.me/p/fdf94d64-6b9f-42dc-a532-ff57ea991ade), [mẫu Matter's Building Blocks](https://app.diffit.me/p/a9c96a52-b3c2-4dde-aeff-e8f6a513f2f6).
- Quan sát: FAQ mô tả nhập text/PDF/URL, sửa nội dung và độ khó qua chat, thêm teacher guide, xuất tài liệu. Bản mẫu công khai được lập chỉ mục "Inference and Sentence Structure" có gợi ý chia nhóm, ưu tiên phần đọc hoặc thêm thời gian cho nhóm gặp khó, và exit ticket. Mẫu "Matter's Building Blocks" có từ vựng, câu hỏi và thảo luận nhóm. Các liên kết mẫu có nội dung đọc được qua kết quả lập chỉ mục, không thực hiện đăng nhập, chỉnh sửa hoặc xuất tài liệu.
- Đáng học: bắt đầu từ nguồn có sẵn, tạo hoạt động theo trình độ, có phương án hỗ trợ khi học viên gặp khó.
- Điều tránh trong TeachFlow: biến output chính thành worksheet, slide hay tài nguyên riêng cho học viên. Giữ một kịch bản cho người dạy, trong đó hoạt động và câu hỏi gắn với timeline.

## Đối chiếu thiết kế

| Tiêu chí | MagicSchool (tài liệu) | Eduaide (tài liệu/mẫu 5E) | Diffit (tài liệu/mẫu công khai) | TeachFlow (thiết kế) |
|---|---|---|---|---|
| Context | Lớp, môn, mục tiêu, thời gian, phân hóa | Mục tiêu, lớp, mô hình dạy | Nguồn, trình độ, điều chỉnh hoạt động | Sĩ số, trình độ, thời lượng, thiết bị, hình thức, mục tiêu |
| Đầu ra quan sát/mô tả | Lesson plan có thể sửa | Chuỗi 5E với teacher moves, hoạt động, pacing | Tài nguyên, câu hỏi, teacher guide, phân hóa | Một kịch bản JSON có lời dẫn, hoạt động, kiểm tra hiểu, fallback |
| Grounding | Chưa đo mức bám nguồn | Có hướng dẫn đính kèm nguồn; chưa đo | Có nhập nội dung sẵn có; chưa đo | Mã nguồn trong đoạn truy xuất và validator; người duyệt kiểm ngữ nghĩa |
| Timeline và phê duyệt | Có thời gian và sửa nội dung theo FAQ; chưa thử | Có pacing và hướng dẫn chỉnh sửa | Có chỉnh sửa; chưa đo timeline | Timeline nguyên, liên tục, khớp tổng; duyệt rõ ràng, sửa mất duyệt |
| Màn hình đọc riêng theo slide gốc | Chưa xác định trong phạm vi review | Chưa xác định trong phạm vi review | Chưa xác định trong phạm vi review | Đã có cửa sổ riêng cho bản đã duyệt; slide gốc không bị thay thế |

Kết luận: khác biệt của TeachFlow là phạm vi hẹp cho giảng viên/lab coach AI20K, kịch bản thực thi bám mã đoạn nguồn và thời lượng một buổi, lời dẫn cụ thể và chế độ đọc riêng. P1–P3 củng cố hướng này: cả ba chưa từng có bản kịch bản đầy đủ; P2 gặp khó khi chuẩn bị, P3 không muốn tạo lại slide/video. Không khẳng định các đối thủ thiếu tính năng tương tự hoặc TeachFlow vượt trội về chất lượng nếu chưa có phép đo chung. Chưa chạy sinh mới trên các dịch vụ; bảng chỉ phản ánh những gì đã đọc được, không tính là eval hay log dùng thử có tài khoản.
