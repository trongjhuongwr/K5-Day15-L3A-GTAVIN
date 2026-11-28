# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1, gói gọn **đúng 4 trang** theo yêu cầu trình bày. Mã nguồn HTML trình chiếu lưu tại `slides/slides.html` (hỗ trợ phím `←`/`→`, `P`, `F`) và xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo để nộp tại CP4 14:30 Thứ Bảy 28/11. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng, Pain & Chọn hướng A4 | Ai · việc gì · chỗ đau (`1.08%`, `74.3%`, `89.6%`) + trích dẫn ẩn danh + biểu đồ so sánh A4 (`61.040 phút`) vs A1, A2 | `evidence/summary.md` · `spec.md` §2 | ☑ |
| 2 | Giải pháp 3 vai & Demo Live | Lát cắt 1 câu · sơ đồ 3 vai tách quyền đọc tài liệu · chỗ chặn rủi ro & HAX · kịch bản demo ca thường + ca khó + X-Ray + video dự phòng | `spec.md` §4 · `eval/benchmark.csv` · `codebase/ui.html` | ☑ |
| 3 | **Đánh giá định lượng (60% → 97%)** | Kho 11 đoạn · bộ 30 câu (`10/30` nguồn thật) · 4 metric · biểu đồ Lượt 1 → Lượt 2 kèm run ID · 3 nhóm lỗi & ca còn trượt trung thực `T20` | `eval/README.md` · `eval/report.md` | ☑ |
| 4 | **Chi phí thật, Kết luận GO & 1 tuần tới** | `$0.00031/task`, `$2.47/tháng` (`700 HV`), `$0.021/giờ` vs `140 phút/HV` · Quyết định **GO** kèm ranh giới an toàn · 3 việc tiếp theo (`T20`, `T24/T29`, `validation/log.md`) | `cost/cost-estimate.md` · `eval/report.md` §4 · `validation/log.md` | ☑ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Phân công thuyết trình & Trả lời hỏi đáp (R7):

| Phần | Phụ trách |
|---|---|
| Thuyết trình chính cả 4 trang & Demo trực tiếp | **Nguyễn Trọng Hưởng** (`2A202603607`) |
| Sẵn sàng trả lời Hỏi–Đáp Giám khảo phần R1–R2 (Data & Pain) | Phạm Ngọc Trung Quân (`2A202603626`) |
| Sẵn sàng trả lời Hỏi–Đáp Giám khảo phần R4–R6 (Eval & Cost) | Lê Thành Đạt (`2A202603579`) |
| Sẵn sàng trả lời Hỏi–Đáp Giám khảo phần Kho bài 11 đoạn & HAX | Trần Minh Tân (`2A202603688`) |
