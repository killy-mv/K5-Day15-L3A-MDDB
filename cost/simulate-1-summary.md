# Tóm tắt mô phỏng simulate-1@20261128-140657

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| giang_vien_thinh_giang | 19 | 2 | 3484 | 1948 | 1.6 | 3.2 |
| lab_coach_chinh | 25 | 2 | 3427 | 1771 | 1.6 | 3.1 |
| giang_vien_chu_chot | 6 | 3 | 5922 | 3104 | 2.7 | 5.3 |

Tỉ lệ đạt dùng để tính: 22/24 (92%) — lượt run-2@20261128-135219

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (22 người) | Chi phí / tháng — cơ sở (84 người) | Chi phí / tháng — cao (168 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0039 | $0.0043 | $0.0020 | $0.5114 | $1.95 | $3.91 | $0.0232 |
| gemini-3.8-flash (vào 1.5 · ra 7.5 $/1M) | $0.0206 | $0.0225 | $0.0106 | $2.68 | $10.23 | $20.46 | $0.1218 |
| gpt-6.1-terra (vào 1.0 · ra 5.0 $/1M) | $0.0137 | $0.0150 | $0.0071 | $1.79 | $6.82 | $13.64 | $0.0812 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0206 | $0.0225 | $0.0106 | $2.68 | $10.23 | $20.46 | $0.1218 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.1) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
