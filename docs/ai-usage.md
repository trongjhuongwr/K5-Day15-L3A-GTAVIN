# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|

| Code bản chạy thử | Antigravity (Gemini) | Hỗ trợ dựng khung `agent.py`, `ai.py`, cài `handoff_allowlist` và `_output_guardrail` (Hưởng); gia cố `_contains_term`, `_STOPWORDS` trong `tools.py` và `active_code` trong `app.py` (Tân) | Hưởng kiểm thử toàn bộ 12 tuyến, nối thật Anthropic `claude-haiku-5-5` qua `eval --try` và duyệt merge; Tân giữ nguyên chữ ký 5 `@tool`, tự test ca biên và `eval --fake`/`--try` | Nguyễn Trọng Hưởng, Trần Minh Tân |
| Prompt / thiết kế lời gọi mô hình | Antigravity (Gemini) | Gợi ý system prompt 3 vai (`director`, `classmate_confused`, `teaching_assistant`) và cơ chế tách dữ liệu allowlist cho `classmate_confused` | Đọc kiểm từng output thật trên `eval/run-try.csv` (`T01`–`T03`) để bảo đảm bạn học AI không lộ đáp án và Trợ giảng trích đúng `[mã đoạn]` | Nguyễn Trọng Hưởng |
| Đào data (viết script đếm, gợi ý nhãn) | Antigravity (Gemini) | Viết script `evidence/count.py` (thư viện chuẩn) đọc `data/preclass/` và tổng hợp 11 chỉ số | Đối chiếu định nghĩa cột trong `column_dictionary.csv`, kiểm tay 6 mã dòng mẫu ẩn danh trong `evidence/data-mining.md` (11/11 chỉ số chạy lại khớp) | Nguyễn Trọng Hưởng, Phạm Ngọc Trung Quân |
| Rà câu hỏi phỏng vấn / khảo sát | | *(Nhóm không dùng phỏng vấn/khảo sát; dùng log hành vi `data/preclass/` và kênh công khai khoá)* | | |
| Viết câu thử (benchmark) | Antigravity (Gemini) | Đề xuất 12 tình huống khởi đầu CP2 phủ 4 lớp chỗ khó + 2 câu tấn công trong `eval/benchmark.csv` | Kiểm từng câu khớp với `spec.md §5`, đối chiếu 4 dòng `data_that` từ `data/preclass/`, chuẩn bị mở rộng lên 20–30 câu cho CP3 | Lê Thành Đạt, Nguyễn Trọng Hưởng |
| Sinh data `synthetic` (nếu có) | Antigravity (Gemini) | Đề xuất 8 đoạn gốc và bổ sung 3 đoạn (`D02-01`, `D07-01`, `D09-01`) vào `data/lessons.json` | Kiểm tay 11/11 đoạn đối chiếu đề cương AI20K L3, không chép nguyên slide/transcript; kiểm tra không gây nhiễu câu ngoài bài `T09` | Trần Minh Tân |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | Antigravity (Gemini) | Hỗ trợ biên tập tiếng Việt và đồng bộ `README.md`, `AGENTS.md`, `canvas.md`, `spec.md`, `DATA_CARD.md` theo code thật | Đội trưởng đọc soát từng mục, giữ nguyên số liệu gốc và phần §7 đã khóa ở CP2 | Nguyễn Trọng Hưởng |
| Rà hồ sơ Eval CP1–CP2 của Đạt | Codex | Đối chiếu phân công và mốc nộp; làm rõ cấu trúc benchmark, cách chấm và giới hạn nguồn; chuẩn bị bảng chấm chéo 5 output trong `eval/README.md` | Chờ Lê Thành Đạt kiểm lại nội dung và phối hợp Quân kiểm nguồn; chấm chéo đang chờ output và hai người chấm | Lê Thành Đạt |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
