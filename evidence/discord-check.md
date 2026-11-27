# Kiểm chéo bằng tin nhắn hỏi bài trên Discord

Trạng thái CP3 · **Chờ trích đoạn đã ẩn danh và số đếm từ kênh công khai của khoá.**

## Quy tắc lấy mẫu trước khi đếm

1. Chọn một kênh học tập công khai của khoá. Ghi tên hoặc đường dẫn cấp kênh, ngày xem và thời điểm chốt mẫu (giờ Việt Nam).
2. Đọc từ tin mới đến tin cũ đến khi đủ **40 tin hợp lệ**. Loại tin bot, thông báo hệ thống và tin của thành viên GTA VIN đã biết. Nếu kênh có ít hơn 40 tin hợp lệ, lấy toàn bộ số tin tìm được và ghi số thực tế. Ghi khoảng ngày của mẫu.
3. Đếm `N` là toàn bộ tin hợp lệ đã đọc, kể cả tin ngoài chủ đề. Đếm `x` là số tin hỏi về khái niệm, đoạn bài hoặc cách làm bài tập của khoá. Tính `100 × x / N` khi `N > 0`.
4. Với mỗi tin trong `x`, gắn các nhãn phù hợp: **tìm lại đoạn bài** khi người hỏi cần vị trí hoặc mốc tài liệu, **cần giải thích khái niệm** khi người hỏi cần làm rõ ý hoặc cách tự diễn đạt, **cần áp dụng** khi người hỏi cần dùng khái niệm trong bài tập. Ghi số từng nhãn trên `x`. Một tin có thể có nhiều nhãn.
5. Chọn 6–10 tin phù hợp để trích, tối đa hai câu mỗi tin. Bỏ tên, nickname, `@mention` và chi tiết nhận diện, đánh dấu phần bỏ bằng `[đã ẩn]`. Dùng mã `S01`, `S02`… và ngày đăng để tham chiếu trong repo. Đối chiếu tin tại kênh, tránh đưa permalink của từng tin vào repo công khai.

## Kết quả chờ điền

| Kênh công khai | Ngày xem và thời điểm chốt | Khoảng ngày của mẫu | Tin đã đọc `N` | Tin hỏi bài `x` | `100 × x / N` |
|---|---|---|---:|---:|---:|
| — | — | — | — | — | — |

Ghi số tin theo từng nhãn, rồi so với [kết quả `preclass`](data-mining.md#3-kết-quả). Ví dụ, đếm tin xin vị trí tài liệu để xem liệu Discord có cho thấy nhu cầu tìm lại đoạn bài hay không. `887/1.260` ở `preclass` đo lượt **AI trả lời** thiếu mốc, còn Discord đo nội dung **tin người học gửi** trong kênh đã chọn. Nêu điểm trùng về vấn đề học và giới hạn của từng mẫu.

## Bàn giao cho Đạt

| Mã tin | Ngày đăng | Trích đoạn đã ẩn danh (tối đa 2 câu) | Nhãn | Biên tập khi đưa vào benchmark |
|---|---|---|---|---|
| — | — | — | — | — |

- Cột `source` dùng mẫu `nguoi_dung: Discord công khai AI20K, Sxx, DD/MM/2026; xem evidence/discord-check.md`.
- Ghi rõ phần bỏ thông tin nhận diện, phần cắt bớt và mã đoạn `[Dxx-yy]` nếu được thêm dựa trên chủ đề xác định được. Với tin thiếu ngữ cảnh dùng để thử khả năng hỏi lại, giữ nguyên độ mơ hồ. Nếu phải tự viết lại ý của người hỏi, ghi `tu_viet` và giữ tham chiếu để giải thích cảm hứng cho ca thử.
- Mục tiêu là **8 trích đoạn hợp lệ cho 24 câu**, hoặc **9 cho 25 câu** nếu các câu còn lại do nhóm tự viết. Sau khi có các trích đoạn, Đạt chọn `expected` và `pass_criterion` theo bài học rồi chạy `python run.py check`. Xem [đối chiếu bốn câu hiện tại](data-mining.md#6-đối-chiếu-bốn-câu-thử-tham-chiếu-preclass) và [Guide §2.4](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/02-guide.md#b2-4).
