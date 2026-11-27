# GTA VIN — Lớp học AI chủ động "Học bằng cách dạy lại" (Track A · A4)

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md). **Điền TEAMS.md đúng format**: khi chấm và đánh giá, BTC quét file này để ghép điểm cho từng người.

*Lát cắt = phần nhỏ nhất làm xong được trong hackathon: một người dùng · một việc · một quyết định AI · một kết quả.*

**Lát cắt của nhóm:** Một học viên L3 · tự học xong một đoạn bài trên pre-class · AI chọn đưa bạn học hỏi sai để học viên giảng lại, hoặc gọi trợ giảng sửa lỗi kèm mã đoạn · học viên tự giải thích đúng và qua được câu kiểm tra ngay sau đó.

---

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

## Chạy trong 3 phút

Bộ khung cần **Python 3.10 trở lên** (trên Windows nếu lệnh `python` mở Microsoft Store, dùng `py`). **Không cần `pip install` cho bộ khung.**

```powershell
py --version
py run.py
py run.py check
copy .env.example .env
```

Nối model thật (Anthropic Claude Haiku 5.5): xem [docs/connect-model.md](docs/connect-model.md).

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `py run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `py run.py check` | Kiểm `eval/benchmark.csv`, `eval/metric_spec.yaml` và `TEAMS.md` |
| `py run.py eval --try` | Thử nối model với 3 câu đầu → `eval/run-try.csv` |
| `py run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-N.csv` + `traces/run-N.jsonl` |
| `py run.py score eval/run-1.csv` | Tính % đạt tổng và theo `type` sau khi điền cột `pass` |
| `py run.py simulate --try` | Thử mô phỏng chi phí 10 phiên → `cost/simulate-try.csv` |
| `py run.py simulate --rate-from eval/run-2.csv` | Mô phỏng chi phí ≥50 phiên theo `cost/personas.yaml` |

## Bản chạy thử — viết ở đâu

| File | Viết gì | Bước guide |
|---|---|---|
| `codebase/agent.py` | `answer(text)` — luồng Multi-agent 3 vai (`director`, `classmate_confused`, `teaching_assistant`), khóa quyền truyền dữ liệu (**Handoff Allowlist**) và hậu kiểm đầu ra (`_output_guardrail`) khớp `spec.md` §4 | 3.2 |
| `codebase/tools.py` | 5 công cụ `@tool` chỉ đọc/phân tích cục bộ: `get_passage`, `search_lesson`, `assess_learner_input`, `check_answer`, `next_speaker` | 2.2, 3.2 |
| `codebase/ai.py` | `call_model(system, user)` — điểm gọi model duy nhất (Anthropic `Claude Haiku 5.5` với mã `claude-haiku-5-5`; hỗ trợ chế độ giả `fake` khi chưa điền `.env`) | 3.3 |

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI ở quyết định trung tâm | **Đã nối API thật (chạy thử `eval --try`)** | Dùng Anthropic `Claude Haiku 5.5` (`claude-haiku-5-5`) đo token từ `usage` thật; vẫn giữ nhánh `fake` cho kiểm thử nhanh không tốn phí |
| Kho đoạn bài giảng & câu hỏi kiểm tra | **Tự biên soạn cô đọng (`11` đoạn)** | Tóm tắt theo đề cương khoá AI20K L3 (`D01-01` → `D11-01`), không sao chép slide/transcript, mô tả tại `data/DATA_CARD.md` |

## Dùng AI vào việc gì

Nhóm dùng trợ lý lập trình AI để rà cấu trúc repo, hỗ trợ viết script thống kê `data/preclass/`, gợi ý gia cố công cụ/guardrail và biên tập tài liệu cho gọn rõ. Mọi số liệu, thiết kế luồng, câu thử và nội dung bài học đều do từng thành viên tự kiểm chứng lại trên dữ liệu và chạy code trực tiếp. Chi tiết xem [docs/ai-usage.md](docs/ai-usage.md); quy ước cho coding agent xem [AGENTS.md](AGENTS.md).

## File mẫu — điền ở bước nào

| File | Điền ở bước guide | Mốc |
|---|---|---|
| `TEAMS.md` | 1.0 | CP1 · **đúng format**, BTC quét khi chấm |
| `canvas.md` | 1.4 | CP1, cập nhật CP2 |
| `evidence/hypothesis.md` | 1.1 | trước khi tìm bằng chứng |
| `evidence/data-mining.md` · `evidence/summary.md` | 1.2 | CP3 |
| `spec.md` | §0–§2: 1.1–1.3 · §3–§5: 2.1–2.3 · §7: 2.4 · §8: 4.2 · §10: suốt | §7 chốt CP2 · §0–§7 CP3 · đủ CP4 |
| `data/DATA_CARD.md` | 2.4 | bản đầu CP2 |
| `eval/benchmark.csv` · `eval/metric_spec.yaml` | 2.4 | ≥10 câu + metric chốt CP2 · 20–30 câu CP3 |
| `codebase/` | 3.2, 3.3 | khung CP2 · AI thật CP3 |
| `eval/report.md` · `eval/README.md` | 4.1 | CP4 |
| `cost/personas.yaml` · `cost/cost-estimate.md` | 4.2 | thử 10 phiên CP3 · đủ CP4 |
| `validation/log.md` *(bonus)* | 4.3 | CP4 |
| `slides/outline.md` → `demo-slides.pdf` | 5.1 | CP4 |
| `reflection/TEMPLATE.md` → `reflection/<ten>.md` | 5.3 | 23:59 Thứ Bảy 28/11 |

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp ở `evidence/summary.md`) |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · lệnh ở mục "Lệnh" |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/` |
| 7 | Slide + demo + video dự phòng | `demo-slides.pdf` ở thư mục gốc · link video: *(cập nhật CP4)* |
| + | *Bonus:* người dùng thử | `validation/log.md` |
