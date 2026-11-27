# AGENTS.md — hướng dẫn cho coding agent (Claude Code, Cursor, Codex…) làm việc trong repo này

> Quy ước làm việc cho trợ lý AI lập trình trong repo bài tập nhóm **GTA VIN** (Track A · Hướng A4).

## Repo này là gì

Repo nộp bài hackathon AI20K của nhóm: bản chạy thử AI cho **một lát cắt** (xem `spec.md` §4), kèm bằng chứng pain, bộ câu thử và mô phỏng chi phí. Mọi thay đổi phải chạy kiểm tra được bằng các lệnh dưới đây.

## Lệnh

*(Trên Windows dùng `py` nếu lệnh `python` bị trỏ vào Microsoft Store.)*

```
py run.py                    # chạy bản chạy thử
py run.py check              # kiểm eval/benchmark.csv + eval/metric_spec.yaml + TEAMS.md
py run.py eval --try         # thử 3 câu đầu
py run.py eval               # chạy cả bộ → eval/run-N.csv + traces/run-N.jsonl
py run.py score eval/run-N.csv
py run.py simulate --try     # thử mô phỏng chi phí 10 phiên
py run.py simulate           # mô phỏng chi phí → cost/simulate-N.csv
```

Khung chỉ dùng thư viện chuẩn Python 3.10+. Nếu thêm thư viện ngoài, ghi rõ vào `requirements.txt`.

## Cấu trúc code

| File | Ai sửa | Hợp đồng |
|---|---|---|
| `codebase/agent.py` | Hưởng | `answer(text) -> {"output": str}` — điều phối 3 vai, giữ Handoff Allowlist cho `classmate_confused` và `_output_guardrail()` |
| `codebase/ai.py` | Hưởng | `call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}`, giữ `@model_call`. Token lấy nguyên từ `usage` của API |
| `codebase/tools.py`, `app.py` | Tân | 5 công cụ `@tool` chỉ đọc/phân tích cục bộ + giao diện dòng lệnh giữ `active_code` |
| `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py`, `run.py` | **khung — không sửa** | ghi trace, chạy bộ câu thử, mô phỏng chi phí |

## Luật — agent KHÔNG được làm

- Không commit `.env`, API key, dữ liệu cá nhân thật, nguyên file data BTC cấp.
- Không sửa `eval/run-*.csv`, `cost/simulate-*.csv`, `traces/*` đã chạy (trừ điền cột `pass`, `ghi_chu`).
- Không sửa chuẩn "đạt" (`spec.md` §7), `eval/metric_spec.yaml` sau CP2; không xoá câu thử trượt, không sửa `expected` cho khớp output.
- Không bịa người được phỏng vấn, trích dẫn, câu trả lời khảo sát, số liệu. Số không có nguồn thì ghi rõ *(tự ước tính)*.
- Công cụ có tác động ra ngoài (gửi tin, sửa dữ liệu, chấm điểm): chỉ tạo bản nháp chờ người duyệt.
- Không viết prompt hoặc điều kiện so khớp nguyên văn input của bộ câu thử để gian lận điểm.

## Quy ước của nhóm

- Ngôn ngữ trả lời người dùng: Tiếng Việt có dấu, ngắn gọn, bám đúng `data/lessons.json`.
- Đặt tên rõ theo đúng vai (`director`, `classmate_confused`, `teaching_assistant`), không sửa chữ ký `@tool` nếu chưa báo thành viên phụ trách.
- Đội trưởng (Nguyễn Trọng Hưởng) và thành viên phụ trách phần liên quan kiểm tra lại trực tiếp mọi thay đổi trước khi merge vào `main`.
