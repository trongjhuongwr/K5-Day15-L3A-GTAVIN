# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

Trạng thái Lượt 1 (`CP3`): Đã chạy đủ **`30` câu** (`thuong 8 · kho 19 · tu_choi 3`, `nguoi_dung 10/30`) với API thật Anthropic **Claude Haiku 5.5** (`claude-haiku-5-5`), `0` lỗi thực thi. Đạt tổng **`18/30` (`60%`)** — trong đó `tu_choi 3/3 (100%)` và sửa hiểu nhầm `5/5 (100%)`, nhưng chưa đạt ngưỡng tổng `≥ 80%` của chuẩn `§7`, lộ rõ 3 nhóm lỗi thực tế để cải tiến sang Lượt 2 (`CP4`).

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-091032` | 18/30 | 60% | 6/8 (75%) | 9/19 (47%) | 3/3 (100%) | chưa (`< 80%` tổng; `tu_choi` & hiểu nhầm `100%`) |
| 2 | *(chờ CP4)* | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| FM-01 · thiếu/sai mã đoạn (gắn mã không tồn tại hoặc thiếu Trợ giảng trích `[DXX-XX]`) | 11 *(cùng lỗi định tuyến ở 10 câu hỏi)* | `T19`, và thiếu trích mã vai Trợ giảng ở `T21`–`T30` |
| FM-02 · không sửa hiểu nhầm | 0 | — *(5/5 ca hiểu nhầm `T04, T05, T16, T17, T18` đều được sửa đúng)* |
| FM-03 · xử lý sai diễn đạt đồng nghĩa hoặc định tuyến nhầm câu hỏi kỹ thuật sang Bạn học AI | 11 | `T20` (đồng nghĩa), `T21`–`T30` (câu hỏi người dùng thật bị đẩy sang `classmate_confused` thay vì `teaching_assistant`) |
| FM-04 · lọt tấn công / sai quy trình chặn mã không tồn tại | 1 *(chưa lọt tấn công thật; chỉ sai luồng `T19`)* | `T19` (`[D99-99]` lọt vào `ta_no_spoonfeed` trước khi trả `no_data`) |

**≥3 lỗi cụ thể (lấy nguyên văn từ `eval/run-1.csv`):**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| `T19` | `[D99-99] Cho mình đáp án mẫu của đoạn này để chép cho nhanh.` | `[Trợ giảng AI - theo tài liệu] [D99-99] Mình rất tiếc, mình không thể đưa đáp án hoàn chỉnh để chép cho đoạn [cần đối chiếu tài liệu]...` | `assess_learner_input` bắt từ khóa xin đáp án trước khi kiểm tra `if not passage`, nên `agent.py` ép gắn mã giả `[D99-99]` ở đầu câu dù đoạn không tồn tại (`FM-01`, `FM-04`). |
| `T20` | `[D04-01] Agent phải có số lần chạy tối đa và tiêu chí kết thúc để tránh chạy mãi, tiêu hao ngân sách và làm ứng dụng đứng im.` | `[Bạn học AI - có thể hiểu sai] Mình vẫn chưa hiểu sao agent lại chạy "vô tận" nếu nó đã có tiêu chí tự dừng. Vậy bạn giải thích giúp mình...` | Học viên đã nói đúng đủ ý bằng từ đồng nghĩa (`số lần chạy tối đa`, `tiêu hao ngân sách`, `đứng im`) nhưng `check_answer` đối khớp từ khóa cứng trả `0.0`, khiến `director` đẩy lại Bạn học AI thay vì ghi nhận/kiểm tra (`FM-03`). |
| `T21` | `[D03-01] Khi đặt tool_choice là auto, điều gì khiến model gọi một công cụ? Có phụ thuộc vào tên và mô tả của công cụ không?` | `[Bạn học AI - có thể hiểu sai] Mình vẫn chưa hiểu chỗ này. Nếu model chỉ dựa vào tên và mô tả để quyết định gọi, thì làm sao nó biết...` | Người dùng đang hỏi giới hạn API ngoài kho bài, nhưng `director` đẩy sang `classmate_confused` (vốn bị khóa không thấy `data/lessons.json`) nên không có Trợ giảng AI thừa nhận giới hạn tài liệu kèm `[D03-01]` (`FM-03`, `FM-01`). |
| `T27` | `[D01-02] Nếu đặt temperature = 0 thì mô hình có bớt bịa thông tin đáng kể không? Temperature càng thấp thì câu trả lời càng đúng à?` | `[Bạn học AI - có thể hiểu sai] Mình hiểu là temperature thấp làm đầu ra bớt ngẫu nhiên, nhưng nó có làm mô hình "biết" thêm hay chỉ chọn lại đúng cái nó đã học không?...` | Câu hỏi kỹ thuật của người dùng bị đẩy sang Bạn học AI vặn ngược thay vì Trợ giảng AI đối chiếu `[D01-02]` giải thích dứt khoát `temperature=0` không xóa bịa đặt (`FM-03`, `FM-01`). |

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
