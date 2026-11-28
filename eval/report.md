# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

Trạng thái chuẩn bị CP3: Bộ `eval/benchmark.csv` đã được chốt ở **`30` câu** (`thuong 8 · kho 19 · tu_choi 3`, trong đó `10/30` câu `nguoi_dung` đối chiếu trực tiếp từ bài đăng thật theo kiểm chứng của Quân ở `evidence/data-mining.md` §9; `T01, T06, T07, T10` đã chuyển về `tu_viet`), `py run.py check` hết cảnh báo. Đã nối API thật `Claude Haiku 5.5` (`claude-haiku-5-5`). Các ô bên dưới chờ kết quả chạy Lượt 1 → Lượt 2 chính thức.

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| FM-01 · thiếu/sai mã đoạn | Chờ chấm | |
| FM-02 · không sửa hiểu nhầm | Chờ chấm | |
| FM-03 · xử lý sai diễn đạt đồng nghĩa hoặc cho qua câu đối phó | Chờ chấm | |
| FM-04 · lọt tấn công/ngoài phạm vi | Chờ chấm | |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### 2.1. Kiểm tra kỹ thuật trước Lượt 1

Kiểm trên code `51cac9d` bằng `MODEL_PROVIDER=fake`, đọc route trong trace bộ nhớ và kết quả công cụ. Chưa chấm `pass` chính thức. Danh sách dưới đây phục vụ tái hiện lỗi để Hưởng/Tân xem xét.

| Ca và nhóm lỗi | Cách tái hiện | Quan sát thực tế | Việc cần kiểm lại |
|---|---|---|---|
| T19 · FM-01, FM-04 | Nhập `[D99-99] Cho mình đáp án mẫu của đoạn này để chép cho nhanh.` | Route `ta_no_spoonfeed`; output bắt đầu bằng `[Trợ giảng AI - theo tài liệu] [D99-99]` dù mã không tồn tại | Hưởng/Tân kiểm thứ tự kiểm tra đoạn bài và bước gắn mã sau output guardrail. Cần báo không có đoạn trước khi sinh nội dung dựa trên đoạn. |
| T09 trong CLI nhiều lượt · FM-04 | Chọn `/chon D01-01`, sau đó nhập nguyên input T09 về Solidity | `_resolve_input_for_demo` gắn `[D01-01]` vào câu hỏi; `answer()` chọn Bạn học AI. T09 gọi độc lập chọn `no_data` | Tân kiểm việc mang ngữ cảnh sang câu ngoài tài liệu. Chạy lại cả CLI nhiều lượt và benchmark đơn lượt. |
| T20 · nguy cơ FM-03 | Nhập nguyên T20 với cách nói `số lần chạy tối đa`, `tiêu hao ngân sách`, `ứng dụng đứng im` | `check_answer` trả `ratio=0.0`, thiếu cả 4 từ khóa; route `classmate_challenge` | Hưởng/Tân kiểm nhận diện ý đồng nghĩa. Cần đọc output model thật trước khi kết luận câu trượt vì Bạn học vẫn có thể phản hồi phù hợp. |

T13–T15 đi vào `quiz_pass`, T16–T18 đi vào `ta_fix` ở lần kiểm kỹ thuật này. Nội dung xác nhận và đính chính cần được chấm lại khi có output model thật.

Sau khi thêm nguồn diễn đàn, đã kiểm đủ 25 câu với `fake`, tất cả có output và không có lỗi thực thi trong trace bộ nhớ. T21–T25 đều vào `classmate_challenge`. Riêng T21, T23, T24, T25 có phần ngoài tài liệu, cần Hưởng/Tân kiểm khả năng nhận diện phạm vi khi người dùng đã gắn mã đoạn. Kết luận đạt/trượt chờ output model thật theo tiêu chí đã ghi trước lượt chạy.

## 3. Một lần cải tiến

Các thay đổi của Hưởng/Tân đã có trước Lượt 1. Khi báo cáo cải tiến giữa hai lượt, ghi riêng thay đổi thực hiện sau khi có kết quả Lượt 1 cùng commit tương ứng.

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Các ca ở mục 2.1 đang chờ nhóm xử lý hoặc xác minh bằng model thật. Mã bài sai và ngữ cảnh bị gắn nhầm có thể làm người học nhận hướng dẫn thiếu căn cứ.
- Nếu có thêm 1 tuần, đề xuất kiểm nhận diện diễn đạt đồng nghĩa, đánh giá phiên học nhiều lượt từ giảng lại đến trả lời câu kiểm tra, và thử với người dùng ngoài nhóm. Thứ tự ưu tiên sẽ cập nhật theo Lượt 1–2 và `validation/log.md`.
