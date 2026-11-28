# Tóm tắt mô phỏng simulate-1@20261128-103243

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 22 | 1 | 659 | 346 | 0.7 | 4.2 |
| dung_vua | 16 | 1 | 971 | 427 | 1.1 | 4.6 |
| dung_nhieu | 12 | 1 | 980 | 603 | 1.1 | 4.9 |

Tỉ lệ đạt dùng để tính: 29/30 (97%) — lượt run-2@20261128-102437

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| claude-haiku-5-5 (vào 0.1 · ra 0.5 $/1M) | $0.00030 | $0.00031 | $0.00031 | $1.06 | $2.47 | $3.53 | $0.0035 |
| claude-sonnet-5-5 (vào 2.0 · ra 10.0 $/1M) | $0.0060 | $0.0062 | $0.0062 | $21.16 | $49.38 | $70.54 | $0.0705 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: claude-haiku-5-5. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
