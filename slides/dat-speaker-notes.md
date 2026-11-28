# Lời trình bày của Đạt — Trang 5, 6, 8

> Bản nháp ngày 28/11/2026, chờ Đạt duyệt. Mục tiêu khoảng 100–110 giây tổng, cần bấm giờ khi tập. Chưa có `demo-slides.pdf` tại local; bố cục dựa trên `slides/outline.md`, cần đối chiếu PDF trước buổi demo.

## Trang 5 — Đánh giá thế nào (45 giây)

- Nhóm đánh giá trên 30 câu, gồm 10 câu có nguồn người dùng, với 4 metric: trích dẫn, sửa hiểu nhầm, học chủ động và từ chối đúng.
- Theo CSV hiện tại, Lượt 1 đạt 18/30, Lượt 2 đạt 29/30, khoảng 97%; cả hai lượt đều qua 3/3 câu từ chối và sửa đúng 5/5 ca hiểu nhầm.
- Tôi đã chốt điểm chấm chéo 5 mẫu có AI hỗ trợ, khớp Hưởng 4/5. T02 còn bất đồng về lộ đáp án; số tổng chưa điều chỉnh theo bất đồng này.

Nguồn: `eval/README.md` §3, §5; `eval/report.md` §1. Run ID để trên slide: `run-1@20261128-091032`, `run-2@20261128-102437`. Không gọi 97% là mức cải thiện học tập; đây là tỷ lệ qua bộ câu thử.

## Trang 6 — Chi phí khi dùng thật (30 giây)

- Mô phỏng 50 phiên cho chi phí khoảng 0,00031 đô mỗi task thành công trên Haiku, theo bảng giá của đề.
- Ba kịch bản 300, 700 và 1.000 người có chi phí token khoảng 1,06; 2,47 và 3,53 đô mỗi tháng.
- Đây là dự phóng theo tần suất giả định, chưa gồm đầy đủ vận hành và công người duyệt; 140 phút học lại mỗi người mỗi tháng cũng là ước tính, chưa phải thời gian đã tiết kiệm được.

Nguồn: `cost/cost-estimate.md` §1–§4; mô phỏng dùng tỷ lệ đạt từ CSV Lượt 2 hiện tại. Giá là giả định theo đề, không phải xác minh giá nhà cung cấp hiện hành.

## Trang 8 — Nếu có thêm một tuần (25–30 giây)

- Thứ nhất, sửa T20 để hỏi đào sâu thay vì lặp lại điều học viên vừa nói; đồng thời thống nhất cách chấm T02.
- Thứ hai, xử lý hai câu T24 và T29 bị cắt phần kết, rồi chạy kiểm tra độ ổn định qua ba lần lặp.
- Thứ ba, mời người ngoài nhóm dùng thử và ghi phản hồi thật, để kiểm tra việc dạy lại có giúp học tốt hơn hay chỉ làm hội thoại trôi chảy.

Nguồn: `eval/report.md` §4 và bất đồng tại `eval/README.md` §3. Đây là kế hoạch, không khẳng định đã có kết quả thử người dùng.
