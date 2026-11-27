# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, cập nhật bản đầu ở CP2 và hoàn thiện trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data `data/preclass/` (`x/N`, %, script chạy lại được, 6 ví dụ ẩn danh) | ☑ | [`evidence/data-mining.md`](data-mining.md) · [`evidence/count.py`](count.py) |
| Đào kênh Discord công khai của khoá (nguồn kiểm chéo) | ☐ *(chờ số đếm và trích đoạn đã ẩn danh)* | [Quy tắc lấy mẫu và bàn giao](discord-check.md) |
| Phỏng vấn / Khảo sát | ☐ *(không dùng)* | Nhóm chọn đào data hành vi thật + kênh công khai khoá |

## 2. Số chính

- **Đào data `data/preclass/` (436/721 học viên hoạt động, 05–25/11/2026):**
  - **385/761 (50.6%)** quyết định của bộ điều phối có chèn bạn học AI. Trong toàn bộ đợt log, ghi nhận **151** phản hồi thảo luận trên **13.975** lượt hiển thị bạn học AI (**1.08%**).
  - **909/1.223 (74.3%)** câu nhắn AI đã chấm có `rubric_y_moi = 0` (chưa tạo ra diễn đạt ý mới); `rewards.csv` ghi nhận **0/228** lượt thưởng cho `giai_thich` và `phan_hoi_xay_dung`.
  - **887/1.260 (70.4%)** câu AI trả lời thiếu mốc trích dẫn (`moc_trich_dan` rỗng); **150/1.260 (11.9%)** câu hỏi ngắn `≤ 15` ký tự và nhóm này bị lạc bài tới **84/144 (58.3%)** (`rubric_bam_bai = 0`).
  - **399/1.968 (20.3%)** lượt làm câu kiểm tra cuối ngày (`pre_post_post`) bị sai ngay lần đầu, xảy ra ở **69/77 (89.6%)** học viên làm bài; **102/453 (22.5%)** lượt hoàn thành mini-lab kết thúc bằng bấm bỏ qua (`skipped = true`).

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. Ví dụ ẩn danh `program-day01:ai-llm-foundation@V1:5` (`class_events.csv`): `director_decided` chèn `classmate_deep_thinker` (`ask_check`, `constructive`), nhưng tỉ lệ phản hồi chung chỉ đạt `151/13.975 (1.08%)`.
2. Ví dụ ẩn danh `C01056` (`chat.csv`, `hv = L0057`, Day01): câu hỏi chỉ dài `2` ký tự, AI trả lời `171` ký tự nhưng bị chấm `rubric_bam_bai = 0`, `rubric_y_moi = 0`.
3. Ví dụ ẩn danh `C00128` (`chat.csv`, `hv = L0384`): `video_discussion_reply` trả lời lại `classmate_deep_thinker` (`24` ký tự) nhưng `rubric_y_moi = 0`.
4. Ví dụ ẩn danh `A00611` (`answers.csv`, `hv = L0213`, `kc = chatbot_is_app_around_model`): làm sai ngay lần đầu (`lan_thu = 1`) ở bài kiểm tra cuối ngày `pre_post_post`.
5. Ví dụ ẩn danh `L0287` (`events.csv`, `d01-lab-ban-la-llm`): kết thúc mini-lab ở bước `1/2` bằng `skipped = true`.
Các trích đoạn từ kênh công khai của khoá sẽ được ghi trong [bảng bàn giao Discord](discord-check.md#bàn-giao-cho-đạt) khi có mẫu thật.

## 4. Các nguồn có khớp nhau không

Log `preclass/` ghi khoảng 1,08 phản hồi thảo luận trên 100 lượt hiển thị và 74,3% câu nhắn đã chấm có điểm ý mới bằng 0. Trong 77 người làm kiểm tra sau bài, 69 người từng sai ít nhất một câu ở lần thử đầu. Mẫu Discord sẽ bổ sung nội dung học viên hỏi khi vướng. Việc đối chiếu hai nguồn chờ số đếm và trích đoạn thật.

## 5. Kết luận

Giả thuyết ở [`evidence/hypothesis.md`](hypothesis.md): **đúng với dữ liệu hành vi `data/preclass/`** (`1.08%` phản hồi thấp hơn nhiều ngưỡng dự đoán `<50%`, `74.3%` `rubric_y_moi = 0` vượt ngưỡng `≥50%`). Điều vẫn chưa biết từ log số: nội dung câu chữ cụ thể khiến học viên hiểu lệch hoặc hỏi ngắn là gì — sẽ kiểm thêm trên kênh Discord công khai trước CP3.

## 6. Lời nói demo của Quân

**Trang 1 · Người dùng và vấn đề**

> Người dùng của nhóm là học viên L3 tự học trước buổi học. Trong đợt log của BTC, có 151 phản hồi thảo luận trên 13.975 lượt bạn học AI hiện ra. Trong 1.223 câu nhắn đã chấm và có điểm ý mới, 909 câu đạt 0 điểm ở tiêu chí này. Nhóm chọn một phiên để học viên tự giải thích lại một khái niệm, nhận phản hồi đúng chỗ và làm một câu kiểm tra hiểu.

Khi được hỏi về mẫu số, nói rõ `151/13.975` đếm lượt ghi log trên toàn bộ mẫu. Ví dụ `C00128` là một phản hồi 24 ký tự có `rubric_y_moi = 0`. Nguồn Discord của khóa chờ mẫu để kiểm nội dung học viên hỏi. [Số liệu và mã ví dụ](data-mining.md)

**Trang 2 · Vì sao chọn A4**

> Nhóm chọn A4 vì mục tiêu là xem học viên có diễn đạt lại và kiểm tra được mình hiểu đến đâu. Quy mô kịch bản là 436 học viên có hoạt động trong đợt log, nhân 14 lượt mở bài mỗi tháng và 10 phút học lại mỗi lượt theo giả định. Kết quả là 61.040 phút/tháng, tương đương 140 phút/người/tháng. Hai thừa số 14 và 10 đều là ước tính.

Nếu được hỏi về các hướng đã cân nhắc, A1 tập trung vào tra cứu đoạn bài và có phạm vi người dùng hẹp hơn. Với A2, nhóm chưa có số đo thật cho nhu cầu hỏi lịch hoặc hạn nộp. Mức 140 phút dùng để mô tả quy mô vấn đề trong kịch bản. Phần thời gian tiết kiệm cần đo khi thử sản phẩm. [Bảng Impact trong spec](../spec.md)
