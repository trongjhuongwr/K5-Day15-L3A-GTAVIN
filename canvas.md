# Canvas — GTA VIN · Track A

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track A (EdTech · hướng A4 Lớp học kiểu mới) — Học viên tự học trên pre-class giải thích lại khái niệm cho bạn học giả lập hay hiểu sai, có trợ giảng kiểm tra và chốt hiểu trước khi qua đoạn tiếp theo. |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Học viên lớp L3 đi làm ban ngày, tối tự học video và làm mini-lab trên trang pre-class trước buổi học. |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Học viên L3 đi làm ban ngày, tối tự học trên pre-class thường chỉ xem video một chiều và ít tự diễn đạt lại kiến thức, nên không nhận ra chỗ hiểu sai cho đến khi làm bài kiểm tra cuối ngày. |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | Đã đào xong `data/preclass/` (`evidence/count.py`): AI hiện tại chèn bạn học `385/761 (50.6%)` đoạn (`13.975` lượt hiển thị) nhưng chỉ nhận `151/13.975 (1.08%)` phản hồi; `909/1.223 (74.3%)` câu nhắn thiếu ý mới (`rubric_y_moi = 0`); `399/1.968 (20.3%)` câu kiểm tra `pre_post_post` sai ngay lần đầu (`69/77` học viên). Ví dụ: `C01056` (`L0057`) hỏi `2` ký tự, AI đáp `171` ký tự nhưng bị `rubric_bam_bai = 0`, `rubric_y_moi = 0`. |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Một học viên L3 · tự học xong một đoạn bài trên pre-class · AI chọn đưa bạn học hỏi sai để học viên giảng lại, hoặc gọi trợ giảng sửa lỗi kèm mã đoạn · học viên tự giải thích đúng và qua được câu kiểm tra ngay sau đó. |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI tự điều phối lượt nói, đóng vai bạn học hiểu sai và gợi ý kèm mã đoạn bài giảng; nhưng mọi hiểu nhầm của bạn học AI bắt buộc phải được trợ giảng sửa đúng trước khi kết thúc phiên và AI không tự chấm điểm chính thức (vì để sai kiến thức khiến học viên nhớ nhầm rất đắt). |
| 7 | Phân công có tên | Cặp X: Hưởng (Đội trưởng, kiến trúc `agent.py`, nối `ai.py`) & Tân (dữ liệu bài học mã đoạn, `tools.py`, demo) · Cặp Y: Quân (đào `data/preclass/`, `DATA_CARD.md`, `cost/`) & Đạt (`eval/`, báo cáo, `demo-slides.pdf`). |
| — | *(CP2)* Đã đổi gì so với CP1 | Cập nhật dòng 4 bằng số liệu thực đo từ `data/preclass/` (`evidence/count.py`) và chốt thiết kế Multi-agent 3 vai tách biệt (`director`, `classmate_confused`, `teaching_assistant`) cùng chuẩn "đạt" ở `spec.md §7`. |
