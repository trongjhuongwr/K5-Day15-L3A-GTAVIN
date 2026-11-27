# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Script đếm để trong repo: [`evidence/count.py`](count.py).
> Chạy lại từ thư mục gốc repo (trỏ về thư mục `data/preclass/` của repo đề):
> `py evidence/count.py --data ../K5-L3-Day15-AI-Product-Hackathon/data/preclass`
> Repo chỉ chứa số tổng hợp và mã dòng đã ẩn danh — không chép nguyên file CSV của BTC.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: `learners.csv`, `events.csv`, `class_events.csv`, `chat.csv`, `answers.csv`, `rewards.csv` trong `data/preclass/` (05/11/2026 → 25/11/2026, Day01 → Day13).
- Đếm gì · trên tập nào · lọc gì:
  1. Tỉ lệ đoạn bài giảng được bộ điều phối cho bạn học AI xen vào: đếm dòng `type = director_decided` có `data.inserted = true` trên tổng số dòng `director_decided` trong `class_events.csv`.
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
| Đoạn bài giảng được chèn bạn học AI (`inserted = true`) | 385 / 761 | 50.6% | `class_events.csv` (`director_decided`) |
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
→ Cần bổ sung kiểm chéo bằng tin nhắn hỏi bài trên **kênh Discord công khai của khoá** (trích tối đa 2 câu, bỏ tên) để làm rõ *vì sao* và lấy đầu vào thực tế cho bộ câu thử.
