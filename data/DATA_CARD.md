# Data card — TeachFlow AI (CP2)

Phiên bản v0.1 · 27/11/2026. Dữ liệu phục vụ prototype và benchmark, không dùng để train model.

| Dataset / path | Nguồn, xử lý, quy mô | Nhãn và giới hạn |
|---|---|---|
| Nội dung bài mẫu — lessons/teachflow_examples.json | AI hỗ trợ soạn mới theo chủ đề workflow/agent và thực hành tool; chuẩn hóa JSON, mã đoạn duy nhất, 4 bài/fixture, 15 đoạn (6+5+2+2). | synthetic; hai fixture conflict/injection cố ý sai hoặc chứa chỉ dẫn không tin cậy, chỉ để test; không dùng như nguồn kiến thức thật. |
| Teaching strategies — teaching_strategies.json | AI hỗ trợ biên soạn thủ công 6 chiến lược, có thời lượng, điều kiện và mục tiêu; không sao chép tài liệu khóa. | synthetic; danh mục nhỏ, chưa được chuyên gia sư phạm duyệt. |
| Context lớp — classroom_profiles.json | 3 hồ sơ lớp minh họa: 40 người, 200 người, 35 người thực hành; chuẩn hóa trường trình độ, thiết bị, thời lượng. | synthetic; không phải số liệu lớp thật. |
| Ghi chép P1/P2 — ../evidence/interviews/ | 2 phỏng vấn thực tế theo thông tin TV1, bỏ tên người trả lời; tách nhu cầu/kỳ vọng khỏi pain quan sát được. | thật (ghi chép, không xác nhận nguyên văn); mẫu nhỏ, thiếu số phút/tỷ lệ, không đại diện toàn khóa. Không nạp vào runtime model. |
| Benchmark — ../eval/benchmark.csv | 24 câu (`B01–B15` khóa từ CP2; bổ sung `B16–B24` cho CP3): 7 chuyển thể từ ghi chép P1/P2 (`nguoi_dung`), 4 lấy căn cứ thống kê lỗi/bỏ bước từ `data/preclass/` (`data_that`, tái lập qua `eval/preclass_stats.py`), 13 tự thiết kế từ spec §4–§5 (`tu_viet`). | hỗn hợp nguồn thực (11/24 = 45.8%) và tình huống synthetic; context và nội dung bài mẫu dùng trong input là synthetic; giữ nguyên B01–B15, chỉ bổ sung B16–B24. |
| Thống kê tổng hợp pre-class — ../data/preclass/ (BTC cấp) | Đọc chỉ số tổng hợp KC `answers.csv` (`pre_post_post`, `lan_thu=1`, `thuc_hanh`) và sự kiện `lab_opened`/`lab_completed` trong `events.csv` qua `eval/preclass_stats.py`. Không chép bản ghi cá nhân hay đưa vào runtime model. | dữ liệu thật AI20K K5 L3-4 (05/11–25/11/2026) đã ẩn danh từ BTC; chỉ dùng làm căn cứ thiết kế 4 câu thử `data_that` (`B16–B18`, `B21`), không thay thế bằng chứng pain giảng viên. |
| Quy mô lịch vận hành — ../data/training-ops/ (BTC cấp) | Tham chiếu quy mô đội ngũ (22 giảng viên, 62 lab coach) và phân bố số buổi/ca từ `teaching-schedule.xlsx` (`Nhan_su`) và `lab-coach-schedule.xlsx` (`Workload - Lab coach`) để xây dựng `cost/personas.yaml`. | dữ liệu lịch giả lập theo cấu trúc khóa thật (xem `data/training-ops/README.md`); không tính là bằng chứng pain hay `data_that` benchmark; mọi hệ số quy đổi tần suất đều ghi rõ nguồn hoặc *(tự ước tính)*. |

Cách sinh synthetic: soạn trực tiếp JSON/CSV từ context sản phẩm, không lấy mẫu ngẫu nhiên, seed không áp dụng; nội dung cố định trong file là bản tái lập. Không dùng các data synthetic làm bằng chứng pain. Chưa có người kiểm chuyên môn độc lập; kiểm cấu trúc bằng code, người phụ trách cần review 15 đoạn và 6 chiến lược trước khi dùng đánh giá chính thức. Không chia train/test vì không train model. Giữ benchmark 24 câu cố định khi so sánh hai lượt đánh giá Run 1 và Run 2.

Không đưa tên, email, bản ghi cá nhân, tài liệu khóa học nguyên bản hay API key vào dữ liệu mới hoặc runtime model.
