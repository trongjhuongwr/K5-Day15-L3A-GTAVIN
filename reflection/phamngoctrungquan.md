# Reflection — Phạm Ngọc Trung Quân

*Bản nháp để Quân đọc lại trước khi nộp. Mục 3 ghi một lỗi đã tái hiện ở lượt kiểm kỹ thuật.*

1. **Vai trò và phần mình làm**

   Mình thuộc Cặp Y của nhóm GTA VIN, lớp L3A. Phần mình phụ trách gồm bằng chứng dữ liệu, Impact, Data Card và mô phỏng chi phí.
   Mình phụ trách đối chiếu số liệu `preclass`, kiểm chứng nguồn câu thử để bàn giao cho Đạt và theo dõi phần còn thiếu để chốt R4.
   Hồ sơ chính ở [evidence/data-mining.md](../evidence/data-mining.md) và [cost/cost-estimate.md](../cost/cost-estimate.md). Bảng kiểm nguồn đã được gộp qua [PR #5](https://github.com/trongjhuongwr/K5-Day15-L3A-GTAVIN/pull/5).

2. **AI hỗ trợ mình thế nào**

   Mình dùng Codex để chạy lại phép đếm trên log BTC, đối chiếu bản dịch với bài gốc và chuẩn bị bảng độ nhạy chi phí.
   Khi rà nguồn, mình cần xem `input` có giữ câu chữ hoặc ý hỏi từ một nguồn kiểm được hay chỉ dựng tình huống theo metadata. Trong `T06`, log ghi 2 ký tự, còn câu “lỗi rồi” dài 7 ký tự. Bản kiểm chứng vì vậy đề xuất ghi `tu_viet`.
   Tỉ trọng persona lấy từ log mở bài. Tần suất dùng sản phẩm 4, 12 và 24 phiên/tháng được ghi là giả định để sau này đối chiếu với số đo thật. [Khai báo dùng AI](../docs/ai-usage.md)

3. **Một ca lỗi và bài học**

   Trong kiểm kỹ thuật, `T19` xin đáp án và gắn mã đoạn `[D99-99]` không tồn tại. Output vẫn mở đầu bằng vai Trợ giảng và lặp lại `[D99-99]` như mã đoạn.
   Lần kiểm kỹ thuật dùng `fake`. Kết quả chính thức còn chờ Lượt 1. Bài học là kiểm mã đoạn có tồn tại trước khi quyết định câu phản hồi hoặc gắn mã nguồn, vì một lời từ chối vẫn có thể khiến người học tin vào mã đoạn sai.
   [T19 trong benchmark](https://github.com/trongjhuongwr/K5-Day15-L3A-GTAVIN/blob/dfadc6a444f151d6f3f70150c101ef06d796acfa/eval/benchmark.csv) · [Quan sát của Đạt ở mục 2.1](https://github.com/trongjhuongwr/K5-Day15-L3A-GTAVIN/blob/dfadc6a444f151d6f3f70150c101ef06d796acfa/eval/report.md)
