# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào log `preclass` và lập persona | Codex | Đối chiếu bảy tỉ số với log BTC, bổ sung phép đếm phân vị lượt mở bài và tính tỉ trọng ba nhóm | Tái lập bằng `evidence/count.py`, kiểm cách quy đổi tháng và các tần suất mô phỏng trước khi nộp | Quân |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Rà nguồn câu thử và tìm câu hỏi công khai | Codex | Đối chiếu bốn câu dựng từ log, tìm và dịch chín câu hỏi từ diễn đàn công khai ngoài khóa | Đạt rà phạm vi từng câu và xác nhận cách tính nguồn R4 với lab coach | Quân |
| Chuẩn bị mô phỏng chi phí | Codex | Điền persona, đối chiếu bảng giá BTC và nhà cung cấp, tính ví dụ độ nhạy cho cache, prompt và giờ duyệt | Kiểm các giả định, đối chiếu kết quả chi phí với lượt mô phỏng thật và Lượt 2 đã chấm | Quân |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
