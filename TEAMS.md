# TEAMS

> **Khi chấm và đánh giá, BTC dùng máy quét file này để ghép điểm cho từng người. Phải điền đúng format.**
> Giữ nguyên tên file `TEAMS.md` ở thư mục gốc repo, giữ nguyên các dòng `- Tên nhóm:` … và tiêu đề cột của bảng. Chỉ thay chỗ `____`.
> Kiểm bằng `python run.py check`: phần "Kiểm TEAMS.md" không báo gì là đúng format.

- Tên nhóm: GTA VIN
- Lớp: L3A
- Track: A
- Link repo: https://github.com/trongjhuongwr/K5-Day15-L3A-GTAVIN

| STT | Họ và tên | Mã học viên | Vai trò | Phần việc chính |
|---|---|---|---|---|
| 1 | Nguyễn Trọng Hưởng | 2A202603607 | Đội trưởng | Điều phối nhóm, nộp checkpoint, thiết kế kiến trúc multi-agent (`codebase/agent.py`) và nối model (`codebase/ai.py`) |
| 2 | Trần Minh Tân | 2A202603688 | Thành viên | Dựng kho đoạn bài học & công cụ kiểm tra/tra cứu (`codebase/tools.py`), hỗ trợ demo và quay video |
| 3 | Phạm Ngọc Trung Quân | 2A202603626 | Thành viên | Đào dữ liệu `data/preclass/` (`evidence/`), viết `data/DATA_CARD.md` và mô phỏng chi phí (`cost/`) |
| 4 | Lê Thành Đạt | 2A202603579 | Thành viên | Định nghĩa metric (`eval/metric_spec.yaml`), bộ câu thử (`eval/benchmark.csv`), đánh giá lượt 1–2 và slide (`demo-slides.pdf`) |

**Quy tắc điền**
- **Lớp:** `L3A` hoặc `L3B`. **Track:** một chữ `A` (EdTech), `B` (Y tế), `C` (Du lịch), `D` (Thương mại điện tử), `E` (Tài chính) hoặc `F` (Làn khác). **Link repo:** link GitHub công khai của nhóm.
- Mỗi thành viên một dòng, nhóm **3–5 người**. Thiếu thì thêm dòng theo đúng mẫu, thừa thì xoá dòng.
- **Đội trưởng ở dòng 1**, cột Vai trò ghi đúng chữ `Đội trưởng`. Người khác ghi `Thành viên`.
- **Mã học viên** ghi đúng như trên hệ thống của khoá, không có khoảng trắng. Đội trưởng nộp các checkpoint bằng mã ở dòng 1.
- **Họ và tên** ghi đủ, có dấu.
- **Phần việc chính:** 1 dòng ngắn, khớp với phần có tên người đó trong repo.
