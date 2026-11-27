# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số thực đo lấy từ `cost/simulate-N-summary.md` do `python run.py simulate` sinh theo `cost/personas.yaml`.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona theo lượt mở bài** gồm `dung_it` (226/436), `dung_vua` (118/436), `dung_nhieu` (92/436). Dùng lần lượt 4, 12, 24 phiên/người/tháng *(tự ước tính)*. Mỗi phiên lấy một câu thử, có thể là câu thường, khó hoặc từ chối. [Cấu hình](personas.yaml) · [Cách tính tỉ trọng từ preclass](../evidence/data-mining.md#7-lượt-mở-bài-dùng-để-lập-persona)
- **Quy mô kịch bản** thấp 300, cơ sở 700, cao 1.000 người *(tự ước tính)*. Mốc cơ sở tham chiếu 721 tài khoản trong bản trích `preclass`. [Bằng chứng preclass](../evidence/data-mining.md)
- **Giá theo BTC ngày 25/11/2026**, đơn vị USD/1 triệu token. Claude Haiku 5.5 có giá vào **$0,10**, ra **$0,50**, đọc cache **$0,01** ở bậc prompt tối đa 100.000 token. Claude Sonnet 5.5 có giá vào **$2,00**, ra **$10,00**. [Bảng giá của đề](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md) · [Giá từ nhà cung cấp](https://platform.claude.com/docs/en/about-claude/pricing)
- **Tỉ lệ đạt và token thực đo** đang chờ `eval/run-2.csv` đã chấm và API của nhóm. Kết quả trên model khác với model đo token là kịch bản áp giá trên cùng lượng token.

## 2. Kết quả mô phỏng

Chờ `python run.py simulate --rate-from eval/run-2.csv` chạy 50 phiên với seed `42`. Điền run ID và bảng từ `cost/simulate-N-summary.md` khi đã có lượt chạy thật.

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

- **Chi phí đo trên Lượt 2** bằng tổng chi phí gọi model của mọi câu ở Lượt 2, kể cả các ca lỗi và ca tấn công, chia cho số câu đạt theo cột `pass` của chính lượt đó. Ca bị chặn trước lời gọi model có chi phí token bằng 0. Một ca từ chối đúng tiêu chí vẫn tính là đạt.
- **Chi phí dự phóng trên lượt mô phỏng** bằng tổng chi phí mô phỏng chia cho số phiên thành công kỳ vọng. Số phiên thành công kỳ vọng là số phiên mô phỏng × tỉ lệ đạt Lượt 2 cùng model. Nếu chưa có tỉ lệ cùng model hoặc số đạt bằng 0, để trống chỉ số tới khi có dữ liệu phù hợp.

## 3. So với impact

- Impact theo kịch bản trong `spec.md` §2 là **140 phút học lại/người/tháng** *(tự ước tính)*. Đây là quy mô vấn đề theo giả định 14 lượt × 10 phút.
- So sánh chi phí USD/người/tháng trong kịch bản 700 người với số phút thực sự tiết kiệm khi thử nghiệm. Nếu chi phí là `C` USD/người/tháng và tiết kiệm được `m` phút/người/tháng, giá trị một giờ học cần đạt `60 × C / m` USD/giờ để hòa vốn. Kết luận chờ chi phí thật và số đo `m`.

## 4. Độ nhạy và giờ công giảng viên

Tính riêng từng thay đổi trên chi phí cơ sở của Haiku với prompt tối đa 100.000 token. Các ví dụ dưới đây là kịch bản *(tự ước tính)*.

| Thay đổi | Cách tính phần chênh lệch | Ví dụ minh họa |
|---|---|---|
| Bật prompt cache 5 phút | Mỗi triệu token đọc từ cache tiết kiệm $0,09 so với giá vào thường. Mỗi triệu token ghi mới tăng $0,025. Đếm riêng lượng token đọc và ghi từ API. | Với 500.000 token đọc và 100.000 token ghi, giảm **$0,0425** so với tính tất cả token đó theo giá vào thường. |
| Rút gọn system prompt | Token đầu vào giảm × $0,10/1 triệu token. Chạy lại bộ eval cùng model để kiểm tra tỉ lệ đạt sau khi rút gọn. | Cắt 500 token mỗi lời gọi trên 1.000 lời gọi, đầu ra giữ nguyên, giảm **$0,05**. |
| Giảng viên duyệt `lessons.json` | Cộng số giờ duyệt × đơn giá giờ. Chia khoản này cho số người dùng trong kỳ muốn phân bổ. | Duyệt 1 giờ với $20/giờ, phân bổ hết trong tháng đầu, cộng **$20/tháng** hoặc khoảng **$0,029/người** ở kịch bản 700 người. |

Giá ghi cache 5 phút là $0,125/1 triệu token với Haiku ở bậc prompt nói trên. Bảng mô phỏng của khung dùng giá token thường, còn thay đổi chi phí cache được tính ở bảng độ nhạy. [Giá cache của Claude](https://platform.claude.com/docs/en/about-claude/pricing) · [Lab Day 13](https://github.com/VinUni-AI20k/K5-L34-Day13-Lab)
