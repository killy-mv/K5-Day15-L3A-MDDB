# Data card — TeachFlow AI

Phiên bản v0.2 · 28/11/2026 (CP3 chuẩn bị); giữ thông tin CP2 v0.1. Dữ liệu phục vụ prototype và benchmark, không dùng để train model.

| Dataset / path | Nguồn, xử lý, quy mô | Nhãn và giới hạn |
|---|---|---|
| Nội dung bài mẫu — lessons/teachflow_examples.json | AI hỗ trợ soạn mới theo chủ đề workflow/agent và thực hành tool; chuẩn hóa JSON, mã đoạn duy nhất, 4 bài/fixture, 15 đoạn (6+5+2+2). | synthetic; hai fixture conflict/injection cố ý sai hoặc chứa chỉ dẫn không tin cậy, chỉ để test; không dùng như nguồn kiến thức thật. |
| Teaching strategies — teaching_strategies.json | AI hỗ trợ biên soạn thủ công 6 chiến lược, có thời lượng, điều kiện và mục tiêu; không sao chép tài liệu khóa. | synthetic; danh mục nhỏ, chưa được chuyên gia sư phạm duyệt. |
| Context lớp — classroom_profiles.json | 3 hồ sơ lớp minh họa: 40 người, 200 người, 35 người thực hành; chuẩn hóa trường trình độ, thiết bị, thời lượng. | synthetic; không phải số liệu lớp thật. |
| Ghi chép P1/P2 — ../evidence/interviews/ | 2 phỏng vấn thực tế theo thông tin TV1, bỏ tên người trả lời; tách nhu cầu/kỳ vọng khỏi pain quan sát được. | thật (ghi chép, không xác nhận nguyên văn); mẫu nhỏ, thiếu số phút/tỷ lệ, không đại diện toàn khóa. Không nạp vào runtime model. |
| Benchmark — ../eval/benchmark.csv | 15 câu: 5 chuyển thể trực tiếp từ ghi chép P1/P2 với context giả lập, 10 tự thiết kế từ spec §5; mã B01–B15. | hỗn hợp nguồn yêu cầu thực và tình huống synthetic, không phải 15 sự kiện đã xảy ra. |

Cách sinh synthetic: soạn trực tiếp JSON/CSV với ChatGPT từ context sản phẩm, không lấy mẫu ngẫu nhiên, seed không áp dụng; nội dung cố định trong file là bản tái lập. Không dùng các data synthetic làm bằng chứng pain. Chưa có người kiểm chuyên môn độc lập; kiểm cấu trúc bằng code, người phụ trách cần review 15 đoạn và 6 chiến lược trước khi dùng đánh giá chính thức. Không chia train/test vì không train model. Giữ benchmark cố định khi so sánh hai lượt đánh giá.

Không sử dụng dữ liệu preclass/training-ops của BTC cho lát cắt này. Không đưa tên, email, bản ghi cá nhân, tài liệu khóa học nguyên bản hay API key vào dữ liệu mới.


## Nguồn bài giảng ngoài AI20K — OOP annotations (v0.2)

| Thuộc tính | Thông tin |
|---|---|
| Nguồn | PDF lect01a_b-oop-with-ano.pdf do đội trưởng cung cấp; Software Engineering — Lecture 1(a,b): Using Annotation in Object Oriented Programming; footer Duc M. L., metadata Author Duc Le; PDF metadata tạo 08/03/2023. Không có URL nguồn được cung cấp. |
| SHA-256 PDF | 98f97841a2d666a2e4187277385262b5e213a899270c7c17f9ca3e11b53802ed |
| Quy mô | 131 trang; trích xuất được text ở cả 131 trang; bản dùng chung có 1 lesson, 131 đoạn tóm lược có mã OOP-P001–OOP-P131. |
| File | lessons/oop_annotations.json; lesson_id oop_annotations. |
| Xử lý | Trích text bằng PDF parser, đối chiếu ảnh một số trang có bảng/sơ đồ; viết tóm lược tiếng Việt theo từng trang, giữ tên Java/annotation, mã trang và nhóm chủ đề. Không OCR; không chép toàn bộ code, ảnh, slide hoặc text gốc vào repo. |
| Loại dữ liệu | Tài liệu bài giảng thực ngoài AI20K; tóm lược do AI hỗ trợ, không phải trích nguyên văn hoặc bản chuyên gia duyệt. Fixture input/output và context lớp là giả lập. |
| Quyền sử dụng | Người dùng cung cấp PDF để chuẩn bị dataset. Chưa xác minh giấy phép, quyền tái phân phối PDF/text đầy đủ hay quyền gửi nguyên tài liệu tới nhà cung cấp LLM. Repo công khai chỉ có ghi chú diễn giải và metadata, không có PDF hoặc text trích xuất đầy đủ; không gán giấy phép mở cho tài liệu gốc. Cần xác nhận quyền trước khi phân phối bản đầy đủ hoặc đưa vào dịch vụ bên ngoài. |
| Hạn chế | Tóm lược có thể mất thứ tự bố cục, ký hiệu, code, chi tiết hình; một số trang như bìa/Q&A không có kiến thức chuyên môn mới. Cần đối chiếu PDF gốc, đặc biệt trang 21 (DAttr so với AttrRef), 65 (nhận định hiệu năng), 90–91 (giả mã/ký hiệu). Chưa review chuyên môn độc lập. |
| Tái lập | 1 đoạn mỗi trang PDF, mã cố định, không dùng random (seed N/A). Không thay đổi ID khi hiệu chỉnh ghi chú; ghi phiên bản và lịch sử nếu sửa nội dung. |

Không dùng slide làm bằng chứng pain. Chỉ đánh nhãn data_that cho case bổ sung có căn cứ cụ thể từ slide thật; ghi mã trang, mô tả rõ context giả lập. Giữ B01–B15 và metric đã khóa. Một bài giảng không chứng minh khả năng tổng quát hóa sang các môn khác.

Fixture dùng chung: fixtures/lesson_request.json (60 phút, 40 người, 4 nguồn được chọn), fixtures/script_response.json (4 hoạt động, 5+15+20+20 phút, pending_review). Cả hai là minh họa tự soạn, không phải output LLM hoặc kết quả benchmark. Contract: ../docs/interface-contract.md.
