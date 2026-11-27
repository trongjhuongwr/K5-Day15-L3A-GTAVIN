# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, cập nhật bản đầu ở CP2 và hoàn thiện trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data `data/preclass/` (`x/N`, %, script chạy lại được, 6 ví dụ ẩn danh) | ☑ | [`evidence/data-mining.md`](data-mining.md) · [`evidence/count.py`](count.py) |
| Đào kênh Discord công khai của khoá (nguồn kiểm chéo — bổ sung trước CP3) | ☐ *(đang thu thập)* | *(sẽ ghi tại `evidence/discord-check.md` trước CP3)* |
| Phỏng vấn / Khảo sát | ☐ *(không dùng)* | Nhóm chọn đào data hành vi thật + kênh công khai khoá |

## 2. Số chính

- **Đào data `data/preclass/` (436/721 học viên hoạt động, 05–25/11/2026):**
  - Bộ điều phối chèn bạn học AI vào **385/761 (50.6%)** đoạn bài giảng, tạo **13.975** lượt hiển thị (`agent_message_shown`), nhưng chỉ có **151/13.975 (1.08%)** lượt học viên trả lời trong khung thảo luận.
  - **909/1.223 (74.3%)** câu nhắn AI đã chấm có `rubric_y_moi = 0` (chưa tạo ra diễn đạt ý mới); `rewards.csv` ghi nhận **0/228** lượt thưởng cho `giai_thich` và `phan_hoi_xay_dung`.
  - **887/1.260 (70.4%)** câu AI trả lời thiếu mốc trích dẫn (`moc_trich_dan` rỗng); **150/1.260 (11.9%)** câu hỏi ngắn `≤ 15` ký tự và nhóm này bị lạc bài tới **84/144 (58.3%)** (`rubric_bam_bai = 0`).
  - **399/1.968 (20.3%)** lượt làm câu kiểm tra cuối ngày (`pre_post_post`) bị sai ngay lần đầu, xảy ra ở **69/77 (89.6%)** học viên làm bài; **102/453 (22.5%)** lượt hoàn thành mini-lab kết thúc bằng bấm bỏ qua (`skipped = true`).

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. Ví dụ ẩn danh `program-day01:ai-llm-foundation@V1:5` (`class_events.csv`): `director_decided` chèn `classmate_deep_thinker` (`ask_check`, `constructive`), nhưng tỉ lệ phản hồi chung chỉ đạt `151/13.975 (1.08%)`.
2. Ví dụ ẩn danh `C01056` (`chat.csv`, `hv = L0057`, Day01): câu hỏi chỉ dài `2` ký tự, AI trả lời `171` ký tự nhưng bị chấm `rubric_bam_bai = 0`, `rubric_y_moi = 0`.
3. Ví dụ ẩn danh `C00128` (`chat.csv`, `hv = L0384`): `video_discussion_reply` trả lời lại `classmate_deep_thinker` (`24` ký tự) nhưng `rubric_y_moi = 0`.
4. Ví dụ ẩn danh `A00611` (`answers.csv`, `hv = L0213`, `kc = chatbot_is_app_around_model`): làm sai ngay lần đầu (`lan_thu = 1`) ở bài kiểm tra cuối ngày `pre_post_post`.
5. Ví dụ ẩn danh `L0287` (`events.csv`, `d01-lab-ban-la-llm`): kết thúc mini-lab ở bước `1/2` bằng `skipped = true`.
6. *(Sẽ bổ sung thêm trích dẫn câu hỏi nguyên văn từ kênh công khai Discord của khoá — tối đa 2 câu mỗi tin, bỏ tên — trước CP3 10:00 T7).*

## 4. Các nguồn có khớp nhau không

Data `preclass/` chỉ ra rõ học viên gần như bỏ qua bạn học AI hiện tại (`1.08%` phản hồi) và thiếu tự diễn đạt (`74.3%` `rubric_y_moi = 0`), đồng thời hay sai bài kiểm tra (`89.6%` người làm bài từng sai ít nhất 1 câu). Chữ câu hỏi thật trên kênh Discord công khai sẽ được dùng ở bước tiếp theo để kiểm chứng *vì sao* học viên không tương tác và bổ sung đầu vào thật cho bộ câu thử.

## 5. Kết luận

Giả thuyết ở [`evidence/hypothesis.md`](hypothesis.md): **đúng với dữ liệu hành vi `data/preclass/`** (`1.08%` phản hồi thấp hơn nhiều ngưỡng dự đoán `<50%`, `74.3%` `rubric_y_moi = 0` vượt ngưỡng `≥50%`). Điều vẫn chưa biết từ log số: nội dung câu chữ cụ thể khiến học viên hiểu lệch hoặc hỏi ngắn là gì — sẽ kiểm thêm trên kênh Discord công khai trước CP3.
