# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Script đếm để trong repo: [`evidence/count.py`](count.py).
> Chạy lại từ thư mục gốc repo (trỏ về thư mục `data/preclass/` của repo đề):
> `py evidence/count.py --data ../K5-L3-Day15-AI-Product-Hackathon/data/preclass`
> Repo chỉ chứa số tổng hợp và mã dòng đã ẩn danh — không chép nguyên file CSV của BTC.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: `learners.csv`, `events.csv`, `class_events.csv`, `chat.csv`, `answers.csv`, `rewards.csv` trong `data/preclass/` (05/11/2026 → 25/11/2026, Day01 → Day13).
- Đếm gì · trên tập nào · lọc gì:
  1. Tỉ lệ quyết định chèn bạn học AI: đếm dòng `type = director_decided` có `data.inserted = true` trên tổng số dòng `director_decided` trong `class_events.csv`.
  2. Tỉ lệ học viên phản hồi lại trong khung thảo luận bạn học AI: đếm dòng `channel = video_discussion_reply` trong `chat.csv` trên tổng số lượt tin nhắn bạn học AI hiển thị (`type = agent_message_shown` trong `events.csv`).
  3. Tỉ lệ câu nhắn AI chưa đạt diễn đạt ý mới: đếm dòng `nguon = chat`, `trang_thai_cham = da_cham` có `rubric_y_moi = 0` trên tổng số câu `nguon = chat` đã chấm có điểm `rubric_y_moi` trong `answers.csv`.
  4. Tỉ lệ câu hỏi ngắn (`≤ 15` ký tự) và mức độ lạc bài (`rubric_bam_bai = 0`): đếm trong `chat.csv` nối sang `answers.csv` qua `id = ref`.
  5. Tỉ lệ AI trả lời thiếu mốc trích dẫn (`moc_trich_dan` rỗng) và `missing_context = true`: đếm trên toàn bộ dòng `type = agent_replied` trong `events.csv`.
  6. Tỉ lệ làm sai câu kiểm tra cuối ngày (`pre_post_post`) ngay lần đầu: lọc `nguon = pre_post_post`, `lan_thu = 1` trong `answers.csv`, đếm `was_correct = False`.
  7. Tỉ lệ bỏ qua mini-lab: đếm `type = lab_completed` có `data.skipped = true` trên tổng `lab_completed` trong `events.csv`.
- **Mẫu số là gì:**
  - Quy mô người học: `436` học viên có hoạt động trong `events.csv` (trên `721` tài khoản ở `learners.csv`).
  - Lượt bạn học AI xen vào: `13.975` lượt `agent_message_shown`; quyết định điều phối: `761` lượt `director_decided`.
  - Câu nhắn AI đã chấm rubric: `1.223` dòng (trong `1.260` lượt chat).
  - Câu kiểm tra sau bài (`pre_post_post`) lần đầu: `1.968` lượt từ `77` học viên.
- Script: [`evidence/count.py`](count.py)

## 2. Đọc trước, đếm sau

Đã đọc từ điển cột (`column_dictionary.csv`, `event_types.csv`) và rà các dòng mẫu đầu tiên của `chat.csv`, `answers.csv`, `class_events.csv`. Các kiểu hành vi quan sát được trước khi chạy đếm:
- Bộ điều phối (`director`) chèn bạn học AI theo kiểu `summarize`, `ask_check` rất dày, nhưng số lượt `video_discussion_reply` trong `chat.csv` rất thưa.
- Nhiều câu học viên nhắn trong `chat.csv` chỉ dài 2–15 ký tự, nối sang `answers.csv` hay bị chấm `rubric_bam_bai = 0` và `rubric_y_moi = 0`.
- Phần lớn dòng `agent_replied` trong `events.csv` để trống `moc_trich_dan`.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Học viên có hoạt động / tổng tài khoản | 436 / 721 | 60.5% | `events.csv` / `learners.csv` |
| Quyết định chèn bạn học AI (`inserted = true`) | 385 / 761 | 50.6% | `class_events.csv` (`director_decided`) |
| Phản hồi thảo luận / lượt bạn học AI hiện ra | 151 / 13.975 | 1.08% | `chat.csv` (`video_discussion_reply`) / `events.csv` (`agent_message_shown`) |
| Câu nhắn AI không có ý mới (`rubric_y_moi = 0`) | 909 / 1.223 | 74.3% | `answers.csv` (`nguon = chat`, `da_cham`) |
| Câu nhắn AI lạc bài (`rubric_bam_bai = 0`) | 261 / 1.223 | 21.3% | `answers.csv` (`nguon = chat`, `da_cham`) |
| Câu hỏi ngắn `≤ 15` ký tự | 150 / 1.260 | 11.9% | `chat.csv`; trong nhóm đã chấm có `84/144 (58.3%)` bị `rubric_bam_bai = 0` |
| AI trả lời thiếu mốc trích dẫn (`moc_trich_dan` rỗng) | 887 / 1.260 | 70.4% | `events.csv` (`agent_replied`) |
| AI trả lời thiếu ngữ cảnh (`missing_context = true`) | 101 / 1.260 | 8.0% | `events.csv` (`agent_replied`) |
| Câu kiểm tra `pre_post_post` sai ngay lần đầu (`lan_thu = 1`) | 399 / 1.968 | 20.3% | `answers.csv`; `69/77 (89.6%)` học viên từng sai ít nhất 1 câu |
| Mini-lab kết thúc bằng bấm bỏ qua (`skipped = true`) | 102 / 453 | 22.5% | `events.csv` (`lab_completed`); có `602` lượt `lab_opened` |
| Thưởng hành vi `giai_thich` và `phan_hoi_xay_dung` | 0 / 228 | 0.0% | `rewards.csv` (`du_doan = 219`, `sua_sai = 9`) |

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

1. **`program-day01:ai-llm-foundation@V1:5`** (`class_events.csv`): `director_decided` chèn `classmate_deep_thinker` (`intervention_type = ask_check`, `expected_icap = constructive`), nhưng tỉ lệ phản hồi chung chỉ đạt `151/13.975 (1.08%)`.
2. **`C01056`** (`chat.csv`, `hv = L0057`, Day01): học viên gửi câu hỏi chỉ dài `2` ký tự (`do_dai_cau_hoi = 2`), AI trả lời `171` ký tự nhưng trong `answers.csv` bị chấm `rubric_bam_bai = 0`, `rubric_y_moi = 0`.
3. **`C00128`** (`chat.csv`, `hv = L0384`): `video_discussion_reply` trả lời lại `classmate_deep_thinker` (`do_dai_cau_hoi = 24`), nhưng `rubric_y_moi = 0` (chưa tạo ra diễn đạt ý mới của người học).
4. **`C00869`** (`chat.csv`, `hv = L0384`): một trong số ít lượt `video_discussion_reply` đạt `rubric_y_moi = 2` (`do_dai_cau_hoi = 43`) khi đối thoại trực tiếp với `classmate_deep_thinker`.
5. **`A00611`** (`answers.csv`, `hv = L0213`, `program-day01:ai-llm-foundation`, `kc = chatbot_is_app_around_model`): câu kiểm tra cuối ngày `pre_post_post` ở `lan_thu = 1` trả lời sai (`was_correct = False`).
6. **`L0287`** (`events.csv`, `program-day01:ai-llm-foundation`, `d01-lab-ban-la-llm`): `lab_completed` dừng ở bước `1/2` với `skipped = True`.

## 5. Giới hạn của data

- `data/preclass/` chỉ ghi nhận hành vi và độ dài ký tự, **không chứa nội dung câu chữ học viên gõ** nên không biết trực tiếp học viên đang vướng ý nào về mặt ngữ nghĩa; chế độ `learning_mode` (`maic`/`tutor`) mới ghi từ 25/11/2026 nên chưa đủ mẫu so sánh chéo.
- `pre_post_post` mới có `77` học viên làm bài trong đợt xuất này (`1.968` lượt trả lời), vì vậy tỉ lệ sai ở nhóm còn lại chưa đo được trực tiếp.
→ Dùng tin nhắn hỏi bài trên kênh Discord công khai của khoá để đối chiếu học viên đang vướng nội dung nào và lấy đầu vào thực tế cho bộ câu thử. Xem [quy tắc lấy mẫu và bàn giao](discord-check.md).

## 6. Đối chiếu bốn câu thử tham chiếu `preclass`

Đối chiếu `input` trong [`eval/benchmark.csv`](../eval/benchmark.csv) với các dòng ẩn danh trong bản `preclass` của BTC. Rubric R4 yêu cầu ít nhất 1/3 số câu thử có nguồn từ lời người dùng hoặc dữ liệu thật. Bộ log ghi mã bài, hành vi, độ dài và kết quả chấm. [Mô tả bộ dữ liệu](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/data/preclass/README.md) · [Rubric R4](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/03-rubric.md#r4)

| ID | Dòng gốc và chi tiết xác minh được | Phần do nhóm dựng trong `input` |
|---|---|---|
| `T01` | `answers.csv` · `A00611` · câu `d01-on-chatbot-la-ung-dung`, `kc_code = chatbot_is_app_around_model`, sai lần đầu | Lời giải thích cụ thể về system prompt và câu hỏi “vậy đã đủ chưa?”. Log xác nhận chủ đề và kết quả sai. Đây là ca có căn cứ theo chủ đề rõ nhất trong bốn ca. |
| `T06` | `chat.csv` · `C01056` · tin hỏi dưới video dài 2 ký tự. Dòng chấm `A03361` có `rubric_bam_bai = 0`, `rubric_y_moi = 0`. | Cụm “lỗi rồi” có 7 ký tự tính cả dấu cách. Nhóm dùng tình huống hỏi ngắn để thử khả năng hỏi lại. |
| `T07` | `chat.csv` · `C00128` · phản hồi thảo luận dài 24 ký tự. Dòng chấm `A02355` có `rubric_bam_bai = 1`, `rubric_y_moi = 0`. | Cụm “ok đúng”. Điểm ý mới bằng 0 cho biết kết quả theo rubric, còn ý định của người học chưa xác định được từ log. |
| `T10` | `answers.csv` · `A00611` · cùng lượt kiểm tra sau bài sai lần đầu được dùng ở `T01`. | Yêu cầu cấp 10 điểm trên LMS. Đây là tình huống tự viết để thử giới hạn thẩm quyền. |

`python run.py check` đếm mã đầu cột `source`, nên bản hiện tại hiện 4/12 theo nhãn `data_that`. Đề xuất Đạt ghi `tu_viet` cho bốn `input` hiện tại và giữ tham chiếu log trong phần mô tả nguồn. Khi chốt đủ nguồn thật, dự trù **8 câu có nguồn cho bộ 24 câu** hoặc **9 câu cho bộ 25 câu**. Đạt có thể dùng trích đoạn Discord đã ẩn danh theo [mẫu bàn giao](discord-check.md#bàn-giao-cho-đạt).

## 7. Lượt mở bài dùng để lập persona

- `events.csv` ghi `3.982` lượt `lecture_opened` của `429` người, trung bình `9,28` lượt/người trong kỳ quan sát. Đây là đầu vào để quy đổi tần suất trong bảng Impact ở [`spec.md` §2](../spec.md).
- Tính phân vị của số lần mở bài trên cả `436` học viên có hoạt động. `7` người chưa mở bài được tính `0` lượt. Kết quả `P25 = 2`, `P50 = 5`, `P75 = 11` lượt trong kỳ log. Quy đổi theo `30/20` như giả định trong `spec.md` cho `3`, `7,5` và `16,5` lượt mở bài/tháng *(tự ước tính)*.
- Chia theo hai điểm giữa của các mốc kịch bản `4`, `12`, `24` phiên/tháng, tức `8` và `18` lượt quy đổi. Có `226/436` người ở nhóm `≤8`, `118/436` ở nhóm `>8` đến `18` và `92/436` ở nhóm `>18`. Các tỉ trọng này dùng trong [`cost/personas.yaml`](../cost/personas.yaml). Tần suất mở bài là chỉ dấu để lập kịch bản. Số phiên dùng sản phẩm `4`, `12`, `24` là *(tự ước tính)*.

## 8. Câu hỏi từ diễn đàn ngoài khóa để Đạt rà benchmark

Các câu dưới đây được trích ý và dịch từ bài đăng công khai bằng tiếng Anh. Mã bài là gợi ý đối chiếu với `lessons.json`. Đây là ứng viên benchmark, đang chờ lab coach xác nhận cách tính nguồn ngoài khóa theo R4. [Rubric R4](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/03-rubric.md#r4)

| Mã tham chiếu | Mã bài | Câu hỏi đã dịch | Bài gốc |
|---|---|---|---|
| `F01` | `D01-01` | Có thể lưu ID cuộc chat để dùng lại nội dung đã gửi làm lịch sử cho các câu hỏi sau không? | [OpenAI Developer Community](https://community.openai.com/t/can-i-consider-memory-in-chat-completion-api-requests/786851) |
| `F02` | `D01-02` | Nếu đặt `temperature = 0` thì ChatGPT có bớt bịa thông tin đáng kể không? Temperature càng thấp thì câu trả lời càng đúng à? | [OpenAI Developer Community](https://community.openai.com/t/is-the-lower-the-temperature-the-more-correct-the-answer-is/316029) |
| `F03` | `D03-01` | Khi đặt `tool_choice` là `auto`, điều gì khiến model gọi một công cụ? Có phụ thuộc vào tên và mô tả của công cụ không? | [OpenAI Developer Community](https://community.openai.com/t/question-about-the-auto-keyword-for-function-calling/674839) |
| `F04` | `D04-01` | Nếu agent có nhiều công cụ và agent con, làm sao đặt giới hạn số lần gọi để vòng lặp khỏi chạy mãi? | [LangChain Forum](https://forum.langchain.com/t/how-to-cap-tool-and-sub-agent-calls-in-deepagents/1653) |
| `F05` | `D04-01` | Có cách nào để vòng lặp tiếp tục khi model trả về `tool_calls` rỗng dù công việc vẫn chưa xong không? | [LangChain Forum](https://forum.langchain.com/t/reactagent-loop-exits-prematurely-when-llm-returns-text-only-message-with-empty-tool-calls-mid-task/4608) |
| `F06` | `D05-01` | Với agent gửi email, nên đặt bước người duyệt trong công cụ gửi, trong luồng agent hay trong một lớp chính sách riêng? | [LangChain Forum](https://forum.langchain.com/t/how-should-an-agent-handle-email-threads-in-langchain/4954) |
| `F07` | `D06-01` | Nếu dữ liệu được tạo giả lập thì kiểm định chéo còn có ý nghĩa không? Để kiểm tra khả năng tổng quát hóa, tạo một bộ dữ liệu mới có tốt hơn không? | [Cross Validated](https://stats.stackexchange.com/questions/446412/cross-validation-and-synthectic-data-sets) |
| `F08` | `D08-01` | Cách xây hệ nhiều agent trong tài liệu LangChain khác gì dùng `langgraph-supervisor`? Có phải chỉ là hai cách cài đặt cùng một thứ không? | [LangChain Forum](https://forum.langchain.com/t/difference-of-creating-multi-agent/1679) |
| `F09` | `D11-01` | Làm sao để chatbot tránh lặp lại nguyên văn chỉ dẫn hệ thống trong câu trả lời? | [OpenAI Developer Community](https://community.openai.com/t/how-do-i-stop-the-chat-response-from-providing-the-prompt-verbatim/103475) |

Khi đưa vào CSV, ghi mã tham chiếu, diễn đàn, tình trạng bản dịch và URL gốc trong `source`. Nếu lab coach xác nhận cách tính nguồn ngoài khóa, dùng mẫu `nguoi_dung: F01; OpenAI Developer Community; dịch từ tiếng Anh; <URL gốc>`. Các câu hỏi chi tiết về thư viện cần tiêu chí chấm phù hợp với phạm vi tài liệu của bản chạy thử. Dùng [hồ sơ Discord](discord-check.md) cho phần kiểm chéo R1 khi có mẫu của khóa.
