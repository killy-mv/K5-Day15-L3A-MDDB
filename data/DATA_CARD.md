# Data card — TeachFlow AI (CP2)

Phiên bản v0.1 · 27/11/2026. Dữ liệu phục vụ prototype và benchmark, không dùng để train model.

| Dataset / path | Nguồn, xử lý, quy mô | Nhãn và giới hạn |
|---|---|---|
| Nội dung bài mẫu — lessons/teachflow_examples.json | AI hỗ trợ soạn mới theo chủ đề workflow/agent và thực hành tool; chuẩn hóa JSON, mã đoạn duy nhất, 4 bài/fixture, 15 đoạn (6+5+2+2). | synthetic; hai fixture conflict/injection cố ý sai hoặc chứa chỉ dẫn không tin cậy, chỉ để test; không dùng như nguồn kiến thức thật. |
| Teaching strategies — teaching_strategies.json | AI hỗ trợ biên soạn thủ công 6 chiến lược, có thời lượng, điều kiện và mục tiêu; không sao chép tài liệu khóa. | synthetic; danh mục nhỏ, chưa được chuyên gia sư phạm duyệt. |
| Context lớp — classroom_profiles.json | 3 hồ sơ lớp minh họa: 40 người, 200 người, 35 người thực hành; chuẩn hóa trường trình độ, thiết bị, thời lượng. | synthetic; không phải số liệu lớp thật. |
| Ghi chép P1/P2 — ../evidence/interviews/ | 2 phỏng vấn thực tế theo thông tin TV1, bỏ tên người trả lời; tách nhu cầu/kỳ vọng khỏi pain quan sát được. | thật (ghi chép, không xác nhận nguyên văn); mẫu nhỏ, thiếu số phút/tỷ lệ, không đại diện toàn khóa. Không nạp vào runtime model. |
| Benchmark — ../eval/benchmark.csv | 15 câu: 5 chuyển thể trực tiếp từ ghi chép P1/P2 với context giả lập, 10 tự thiết kế từ spec §5; mã B01–B15. | hỗn hợp nguồn yêu cầu thực và tình huống synthetic, không phải 15 sự kiện đã xảy ra. |

Cách sinh synthetic: soạn trực tiếp JSON/CSV với ChatGPT từ context sản phẩm, không lấy mẫu ngẫu nhiên, seed không áp dụng; nội dung cố định trong file là bản tái lập. Không dùng các data synthetic làm bằng chứng pain. Chưa có người kiểm chuyên môn độc lập; kiểm cấu trúc bằng code, người phụ trách cần review 15 đoạn và 6 chiến lược trước khi dùng đánh giá chính thức. Không chia train/test vì không train model. Giữ benchmark cố định khi so sánh hai lượt đánh giá.

Không sử dụng dữ liệu preclass/training-ops của BTC cho lát cắt này. Không đưa tên, email, bản ghi cá nhân, tài liệu khóa học nguyên bản hay API key vào dữ liệu mới.
