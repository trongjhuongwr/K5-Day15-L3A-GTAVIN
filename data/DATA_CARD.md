# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Chấm ở rubric R4.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp.

## Dataset 1 · `data/preclass/` (Nhật ký hành vi thật — dùng đào bằng chứng pain)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain và tính tần suất sử dụng cho mô phỏng chi phí (`evidence/count.py`, `evidence/data-mining.md`, `cost/personas.yaml`) |
| Từ đâu | Bộ dữ liệu BTC cấp (`K5-L3-Day15-AI-Product-Hackathon/data/preclass/`) — đã ẩn danh trước khi phát |
| Xử lý những bước gì | Không chỉnh sửa file gốc, chỉ đọc bằng `evidence/count.py` để đếm theo bảng và điều kiện lọc (`nguon`, `lan_thu`, `trang_thai_cham`, `moc_trich_dan`, `skipped`); không commit file CSV gốc |
| Số dòng / số đoạn | `721` học viên (`436` hoạt động), `107.709` dòng `events.csv`, `1.260` dòng `chat.csv`, `3.776` dòng `answers.csv`, `849` dòng `class_events.csv`, `228` dòng `rewards.csv` |
| Phiên bản / ngày lấy | 05/11/2026 → 25/11/2026 (Day01 → Day13), bản phát ngày 27/11/2026 |
| Nhãn | `thật` (đã ẩn danh bởi BTC) |
| Giới hạn | Không chứa nội dung câu chữ học viên gõ (chỉ có độ dài ký tự); cột `learning_mode` mới ghi từ 25/11/2026 |

## Dataset 2 · `data/lessons.json` (Kho đoạn bài giảng cô đọng — dùng cho bản chạy thử)

| | |
|---|---|
| Dùng để làm gì | Nguồn căn cứ cho công cụ `get_passage`, `search_lesson`, `check_answer` trong `codebase/tools.py` |
| Từ đâu | Nhóm tự biên soạn bản tóm tắt khái niệm cốt lõi dựa theo đề cương công khai của khoá AI20K Level 3 (Day01, Day03, Day04, Day05, Day06, Day08, Day11) — không sao chép nguyên slide hay transcript |
| Xử lý những bước gì | Chuẩn hoá mỗi khái niệm thành 1 mục JSON gồm: `code`, `day`, `topic`, `keywords`, `content`, `misconception`, `check_question`, `key_points` |
| Số dòng / số đoạn | `8` đoạn kiến thức cốt lõi (`D01-01` → `D11-01`) |
| Phiên bản / ngày lấy | Tự biên soạn ngày 27/11/2026 |
| Nhãn | `synthetic` (tự biên soạn có cấu trúc chuẩn, kiểm tay 8/8 đoạn) |
| Giới hạn | Chỉ phủ 8 chủ đề tiêu biểu trong phạm vi lát cắt demo, chưa phủ toàn bộ 15 ngày học |
