# AI SPEC — Lớp học AI chủ động "Học bằng cách dạy lại" (A4) · Nhóm GTA VIN · Phòng H209 *(dự kiến)* · Zone ____

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: A4 · Lớp học kiểu mới (Học bằng cách dạy lại · Protégé Effect)
Data BTC cấp đã dùng (nếu có — không commit nguyên file): `data/preclass/` (chỉ đọc thống kê tổng hợp bằng script trong `evidence/` và trích ví dụ mã ẩn danh; không commit nguyên file CSV).

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này, trong khoá hoặc trên app thật (3–5 bước):
  1. Học viên L3 đăng nhập trang `preclass-online.com` trước buổi học chính.
  2. Mở video bài giảng; trong lúc xem, hệ thống lớp học AI (`director`) tự quyết định cho bạn học AI (`classmate_*`) xen vào khung thảo luận dưới video, hoặc học viên tự bấm hỏi trợ giảng AI (`teaching_assistant`).
  3. Học viên làm câu hỏi giữa video (`video_quiz`), bước thực hành mini-lab (`thuc_hanh`) hoặc câu ôn tập cuối ngày (`pre_post_post`).
- Công cụ / AI đang được dùng cho việc này (nếu có) + nguồn:
  - Trên `preclass-online.com` hiện đã có trợ giảng AI (`teaching_assistant`), các bạn học AI (`classmate_inquisitive`, `classmate_deep_thinker`, `classmate_clown`) và bộ điều phối `director` (nguồn: mô tả cấu trúc trong `data/preclass/README.md` và `column_dictionary.csv` do BTC cấp).

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): Học viên lớp L3 đi làm ban ngày, tối tự học video và làm mini-lab trên trang pre-class trước buổi học.
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI): Nắm chắc khái niệm cốt lõi và tự giải thích lại được kiến thức sau khi xem video pre-class để làm đúng bài thực hành và bài kiểm tra trước khi lên lớp.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: Xem lại/tua video, đọc slide, hoặc hỏi nhanh công cụ chat/trợ giảng. Hỏng ở chỗ việc xem và hỏi đáp thụ động không ép người học tự diễn đạt lại bằng lời của mình nên dễ "tưởng đã hiểu", đến lúc vào kiểm tra hoặc làm lab mới vướng. Chưa bỏ vì đây là quy trình bắt buộc trên LMS/pre-class để mở tiến độ học.
- Pain (KHÔNG chữ AI): Học viên lớp L3 tự học pre-class thường xem bài thụ động, ít có cơ hội chủ động diễn đạt lại và tự sửa chỗ hiểu lệch ngay sau từng khái niệm, dẫn đến vẫn làm sai bài kiểm tra cuối ngày và bỏ qua bước thực hành.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): *(Đang đào từ `data/preclass/` và kênh công khai của khoá — hoàn tất script và tổng hợp trước CP2/CP3)*

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| A4 · Lớp học chủ động "Học bằng cách dạy lại" (Multi-agent) | *(đối chiếu `data/preclass/` ở bước 1.2–1.3)* | | | | Kịp trong 10h (1 khái niệm/phiên) | **Chọn** |
| A1 · Trợ giảng hỏi đáp bám mã đoạn pre-class | *(đối chiếu `data/preclass/`)* | | | | Kịp | Loại (tính thụ động cao hơn, dễ trùng nhiều nhóm) |
| A2 · Trợ lý Discord tra cứu lịch & hạn nộp | *(không có data thật trong bộ cấp)* | | | | Khó đủ bằng chứng kịp CP2 nếu không khảo sát | Loại |

- **Impact / tháng** của hướng chọn = __ người × __ lần × __ phút = __ — nguồn từng thừa số: *(sẽ tính đầy đủ từ `data/preclass/` ở bước 1.3 trước CP2)*
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
  - **A1 (Trợ giảng hỏi đáp):** vẫn là tương tác thụ động (học viên hỏi → AI trả lời), không giải quyết triệt để việc học viên tự diễn đạt lại kiến thức (`rubric_y_moi`).
  - **A2 (Trợ lý Discord lịch/hạn nộp):** bộ `data/training-ops/` là giả lập (không tính là bằng chứng pain), không có sẵn bằng chứng hành vi thật như `data/preclass/`.
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8): *(sẽ cập nhật ở bước 1.3 & 4.2)*

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì *(hoàn thành ở bước 2.1 trước CP2)*

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU**: Một học viên L3 tự học pre-class · vừa xem xong một khái niệm và thấy bạn học AI nêu một hiểu nhầm phổ biến · bộ điều phối quyết định chọn bạn học AI hỏi vặn lại, trợ giảng can thiệp kèm mã đoạn, hay chốt bằng câu kiểm tra dựa trên câu giải thích của học viên · học viên tự diễn đạt đúng bản chất và vượt qua câu kiểm tra cuối đoạn.
- Không làm (≥3 điều):
  1. Không tích hợp trực tiếp vào hệ thống `preclass-online.com` thật.
  2. Không sinh video/audio bài giảng mới.
  3. Không tự động chấm điểm chính thức lên bảng điểm khoá học.
- **Sơ đồ** (ảnh / Mermaid / draw.io): *(hoàn thành ở bước 2.2 trước CP2)*
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [x] nhiều agent — *(điền đầy đủ lý do từng vai và công cụ ở bước 2.2 trước CP2)*
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | | | | |

- **Mức tự động:** *(điền ở bước 2.2)*
- **Chỗ chặn rủi ro:** *(điền ở bước 2.2)*
- **Chỗ người duyệt:** *(điền ở bước 2.2)*
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | |
  | | |
  | | |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật: *(ghi rõ ở CP2)*

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
| | | | |
| *(tấn công)* | | | |
| *(tấn công)* | | | |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"):
  - Cặp X (Code & Model): Nguyễn Trọng Hưởng (`2A202603607`, Đội trưởng) & Trần Minh Tân (`2A202603688`)
  - Cặp Y (Data, Eval & Chi phí/Slide): Phạm Ngọc Trung Quân (`2A202603626`) & Lê Thành Đạt (`2A202603579`)
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`): Sử dụng trợ lý AI lập trình hỗ trợ phân tích cấu trúc khung bài, viết script thống kê `data/preclass/` và hỗ trợ sinh mã nguồn/cấu trúc tài liệu; mọi con số thống kê, thiết kế luồng, câu thử và kết quả đều được các thành viên kiểm tra lại bằng code và đọc trực tiếp.
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
| | | |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| | | |
