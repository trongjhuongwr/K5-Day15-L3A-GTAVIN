# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số thực đo lấy từ `cost/simulate-N-summary.md` do `python run.py simulate` sinh theo `cost/personas.yaml`.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona theo lượt mở bài** gồm `dung_it` (226/436), `dung_vua` (118/436), `dung_nhieu` (92/436). Dùng lần lượt 4, 12, 24 phiên/người/tháng *(tự ước tính)*. Mỗi phiên lấy một câu thử, có thể là câu thường, khó hoặc từ chối. [Cấu hình](personas.yaml) · [Cách tính tỉ trọng từ preclass](../evidence/data-mining.md#7-lượt-mở-bài-dùng-để-lập-persona)
- **Quy mô kịch bản** thấp 300, cơ sở 700, cao 1.000 người *(tự ước tính)*. Mốc cơ sở tham chiếu 721 tài khoản trong bản trích `preclass`. [Bằng chứng preclass](../evidence/data-mining.md)
- **Giá theo BTC ngày 25/11/2026**, đơn vị USD/1 triệu token. Claude Haiku 5.5 có giá vào **$0,10**, ra **$0,50**, đọc cache **$0,01** ở bậc prompt tối đa 100.000 token. Claude Sonnet 5.5 có giá vào **$2,00**, ra **$10,00**. [Bảng giá của đề](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md) · [Giá từ nhà cung cấp](https://platform.claude.com/docs/en/about-claude/pricing)
- **Tỉ lệ đạt và token thực đo:** Lấy tỉ lệ đạt thật **`29/30 (97%)`** từ `eval/run-2.csv` (`run-2@20261128-102437`, đo trên `claude-haiku-5-5`). Dòng `claude-sonnet-5-5` là kịch bản *đo token trên `claude-haiku-5-5`, tính giá `claude-sonnet-5-5`*.

## 2. Kết quả mô phỏng

Đã chạy `py run.py simulate --rate-from eval/run-2.csv` với **50 phiên**, `seed = 42`, **`0/50` lỗi** (`cost/simulate-1.csv`, `cost/simulate-1-summary.md`, `traces/simulate-1.jsonl`).

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| `dung_it` | 22 | 1 | 659 | 346 | 0.7 | 4.2 |
| `dung_vua` | 16 | 1 | 971 | 427 | 1.1 | 4.6 |
| `dung_nhieu` | 12 | 1 | 980 | 603 | 1.1 | 4.9 |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (300) | / tháng — cơ sở (700) | / tháng — cao (1.000) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| `claude-haiku-5-5` | `$0.00030` | `$0.00031` | `$1.06` | `$2.47` | `$3.53` | `$0.0035` |
| `claude-sonnet-5-5` *(đo token trên `claude-haiku-5-5`, tính giá Sonnet)* | `$0.0060` | `$0.0062` | `$21.16` | `$49.38` | `$70.54` | `$0.0705` |

- **Chi phí đo trên Lượt 2** tính trên tổng token mọi câu ở `eval/run-2.csv` (kể cả các ca tấn công/câu ngắn/ngoài tài liệu có `0` token), chia cho `29` câu đạt của chính lượt đó.
- **Chi phí dự phóng trên lượt mô phỏng:** `18/50` phiên rơi vào các câu ngắn/ngoài tài liệu/tấn công được chặn trước lời gọi model (`0` token) giúp kéo chi phí trung bình xuống còn `$0.00030/phiên` trên Haiku.

## 3. So với impact

- Impact theo kịch bản trong `spec.md` §2 là **`140` phút học lại/người/tháng** *(tự ước tính theo 14 lượt × 10 phút)*, tương đương `~1.017` giờ/tháng cho `436` học viên.
- Với `claude-haiku-5-5`, chi phí cơ sở ở quy mô `700` người chỉ là **`$0.0035/người/tháng`** (`$2.47/tháng` cho cả lớp). Ngay cả trong giả định thận trọng nhất là hệ thống chỉ giúp tiết kiệm được **`10` phút/người/tháng** *(~7% của 140 phút — tự ước tính)*, điểm hòa vốn thời gian học là `60 × $0.0035 / 10 = $0.021/giờ` (chưa tới `600 VND/giờ`), cực kỳ đáng triển khai; kể cả phương án `claude-sonnet-5-5` (`$0.0705/người/tháng`) cũng vẫn kinh tế ở quy mô khoá học.

## 4. Độ nhạy và giờ công giảng viên

Tính riêng từng thay đổi trên chi phí cơ sở của Haiku với prompt tối đa 100.000 token. Các ví dụ dưới đây là kịch bản *(tự ước tính)*.

| Thay đổi | Cách tính phần chênh lệch | Ví dụ minh họa |
|---|---|---|
| Bật prompt cache 5 phút | Mỗi triệu token đọc từ cache tiết kiệm $0,09 so với giá vào thường. Mỗi triệu token ghi mới tăng $0,025. Đếm riêng lượng token đọc và ghi từ API. | Với 500.000 token đọc và 100.000 token ghi, giảm **$0,0425** so với tính tất cả token đó theo giá vào thường. |
| Rút gọn system prompt | Token đầu vào giảm × $0,10/1 triệu token. Chạy lại bộ eval cùng model để kiểm tra tỉ lệ đạt sau khi rút gọn. | Cắt 500 token mỗi lời gọi trên 1.000 lời gọi, đầu ra giữ nguyên, giảm **$0,05**. |
| Giảng viên duyệt `lessons.json` | Cộng số giờ duyệt × đơn giá giờ. Chia khoản này cho số người dùng trong kỳ muốn phân bổ. | Duyệt 1 giờ với $20/giờ, phân bổ hết trong tháng đầu, cộng **$20/tháng** hoặc khoảng **$0,029/người** ở kịch bản 700 người. |

Giá ghi cache 5 phút là $0,125/1 triệu token với Haiku ở bậc prompt nói trên. Bảng mô phỏng của khung dùng giá token thường, còn thay đổi chi phí cache được tính ở bảng độ nhạy. [Giá cache của Claude](https://platform.claude.com/docs/en/about-claude/pricing) · [Lab Day 13](https://github.com/VinUni-AI20k/K5-L34-Day13-Lab)
