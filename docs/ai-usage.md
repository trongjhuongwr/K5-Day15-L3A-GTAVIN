# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Antigravity (Gemini) | Gợi ý gia cố khớp ranh giới từ `_contains_term` và tinh chỉnh `_STOPWORDS` trong `codebase/tools.py`; dựng khung giữ `active_code` và hiển thị rõ vai cho `codebase/app.py` | Kiểm tra giữ nguyên chữ ký/output 5 `@tool`, tự chạy script kiểm thử ca biên + `py run.py eval --fake` + `py run.py eval --try` và thử nghiệm tương tác nhiều lượt | Trần Minh Tân |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | Antigravity (Gemini) | Đề xuất bổ sung 3 đoạn kiến thức cô đọng (`D02-01`, `D07-01`, `D09-01`) vào `data/lessons.json` | Kiểm tay 11/11 đoạn đối chiếu đề cương AI20K L3, không chép nguyên slide/transcript; kiểm tra không gây nhiễu câu ngoài bài `T09` | Trần Minh Tân |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |
| Rà hồ sơ Eval CP1–CP2 của Đạt | Codex | Đối chiếu phân công và mốc nộp; làm rõ cấu trúc benchmark, cách chấm và giới hạn nguồn; chuẩn bị bảng chấm chéo 5 output trong `eval/README.md` | Chờ Lê Thành Đạt kiểm lại nội dung và phối hợp Quân kiểm nguồn; chấm chéo đang chờ output và hai người chấm | Lê Thành Đạt |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
