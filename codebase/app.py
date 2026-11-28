"""Giao diện Web (mặc định) và dòng lệnh (--cli) cho bản chạy thử `py run.py`.

Chỉ dùng thư viện chuẩn Python (`http.server.ThreadingHTTPServer`), không cần cài thêm gói ngoài.
Giữ nguyên hợp đồng stateless của `agent.answer(text)` cho `eval` và `simulate`, đồng thời khóa
truy vết (`_TRACE_LOCK`) an toàn khi nhiều request gọi đồng thời.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import re
import sys
import threading
import time
import urllib.parse
import webbrowser

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CODEBASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_HTML_PATH = os.path.join(CODEBASE_DIR, "ui.html")
sys.path.insert(0, CODEBASE_DIR)

_TRACE_LOCK = threading.Lock()
_MAX_INPUT_CHARS = 4000


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback

    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(CODEBASE_DIR)
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path


def _print_lessons(lessons: list) -> None:
    print("Danh sách đoạn bài học hiện có:")
    for item in sorted(lessons, key=lambda x: x.get("code", "")):
        print("  [%s] (%s) %s" % (item.get("code", ""), item.get("day", ""), item.get("topic", "")))


def _format_role_output(raw_text: str) -> str:
    """Làm nổi bật nhãn vai ở đầu câu trả lời để người xem demo phân biệt rõ 3 vai."""
    tags = (
        ("[Bộ điều phối]", "\n[BỘ ĐIỀU PHỐI]"),
        ("[Bạn học AI - có thể hiểu sai]", "\n[BẠN HỌC AI · có thể hiểu sai]"),
        ("[Trợ giảng AI - theo tài liệu]", "\n[TRỢ GIẢNG AI · theo tài liệu]"),
    )
    text = (raw_text or "").strip()
    for prefix, header in tags:
        if text.startswith(prefix):
            rest = text[len(prefix):].strip()
            return f"{header}\n  {rest}" if rest else header
    return "\n" + text


def _detect_role(raw_text: str) -> tuple[str, str]:
    """Tách nhãn vai đầu câu để UI hiển thị màu sắc và thẻ vai chính xác."""
    text = (raw_text or "").strip()
    prefixes = (
        ("[Bạn học AI - có thể hiểu sai]", "classmate"),
        ("[Trợ giảng AI - theo tài liệu]", "ta"),
        ("[Bộ điều phối]", "director"),
    )
    for prefix, role in prefixes:
        if text.startswith(prefix):
            return role, text[len(prefix):].strip()
    return "director", text


def _resolve_input_for_demo(text: str, active_code: str, tools_mod) -> tuple[str, str]:
    """Cập nhật active_code theo ngữ cảnh phiên demo và gắn mã đoạn khi cần tiếp nối lượt trước."""
    explicit = tools_mod.extract_code(text)
    if explicit:
        passage = tools_mod.get_passage(explicit)
        if passage:
            return text, explicit
        # Người học gõ mã không tồn tại (vd [D99-01]) -> giữ nguyên để agent trả no_data
        return text, active_code

    if active_code:
        # Giữ nguyên active_code đang thảo luận (tránh nhảy nhầm sang đoạn khác khi trùng từ khoá),
        # trừ các câu tấn công / ngoài phạm vi thẩm quyền để guard xử lý độc lập.
        pre_check = tools_mod.assess_learner_input("", text)
        if pre_check.get("status") not in ("attack", "out_of_scope_auth"):
            return f"[{active_code}] {text}", active_code
        return text, active_code

    found = tools_mod.search_lesson(text)
    if found:
        new_code = found[0].get("code", "")
        return text, new_code

    return text, active_code


def _process_chat_turn(text: str, active_code: str, tools_mod, tracing_mod, answer_fn) -> dict:
    """Thực thi 1 lượt hỏi/giảng lại an toàn luồng và trả về output + trace cho giao diện."""
    clean_text = (text or "").strip()
    if not clean_text:
        raise ValueError("Vui lòng nhập nội dung trước khi gửi.")
    if len(clean_text) > _MAX_INPUT_CHARS:
        raise ValueError(f"Nội dung vượt giới hạn {_MAX_INPUT_CHARS} ký tự.")

    clean_code = (active_code or "").strip().upper()
    if clean_code and not tools_mod.get_passage(clean_code):
        clean_code = ""

    query_for_agent, next_code = _resolve_input_for_demo(clean_text, clean_code, tools_mod)

    t0 = time.perf_counter()
    with _TRACE_LOCK:
        tracing_mod.begin("app")
        try:
            result = answer_fn(query_for_agent)
        except Exception:
            tracing_mod.end()
            raise
        summary, events = tracing_mod.end()
    latency_s = round(time.perf_counter() - t0, 3)

    raw_out = result.get("output", "") if isinstance(result, dict) else str(result)
    role, clean_output = _detect_role(raw_out)
    cited_codes = sorted({m.upper() for m in re.findall(r"\[(D\d{2}-\d{2})\]", raw_out, flags=re.IGNORECASE)})
    route_name = ""
    for ev in events:
        if ev.get("kind") == "note":
            ev_text = ev.get("text", "")
            if not route_name and ev_text.startswith("director -> "):
                route_name = ev_text[len("director -> "):].split()[0]
            if not next_code:
                m_code = re.search(r"code=(D\d{2}-\d{2})\b", ev_text, flags=re.IGNORECASE)
                if m_code and tools_mod.get_passage(m_code.group(1).upper()):
                    next_code = m_code.group(1).upper()

    mastery = None
    if next_code and route_name not in ("refuse_attack", "refuse_scope", "no_data", "clarify"):
        passage = tools_mod.get_passage(next_code)
        if passage:
            chk = tools_mod.check_answer(next_code, clean_text)
            total_kps = len(passage.get("key_points", []))
            mastery = {
                "code": next_code,
                "matched": chk.get("matched", []),
                "total": total_kps,
                "ratio": chk.get("ratio", 0.0),
                "passed": route_name == "quiz_pass" or bool(chk.get("passed")),
            }

    cited_passages = {}
    for c in cited_codes:
        p = tools_mod.get_passage(c)
        if p:
            cited_passages[c] = {"topic": p.get("topic", ""), "content": p.get("content", "")}

    return {
        "output": raw_out,
        "clean_output": clean_output,
        "role": role,
        "route": route_name,
        "active_code": next_code,
        "cited_codes": cited_codes,
        "cited_passages": cited_passages,
        "mastery": mastery,
        "latency_s": latency_s,
        "summary": summary,
        "events": events,
    }


def _make_handler(ai_mod, tools_mod, tracing_mod, answer_fn):
    """Tạo HTTP handler phục vụ giao diện Web và 3 endpoint JSON cục bộ."""

    class AppHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):  # noqa: A002
            return  # Giữ terminal sạch khi chạy demo

        def _send_json(self, status: int, payload: dict) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):  # noqa: N802
            path = urllib.parse.urlparse(self.path).path
            if path in ("/", "/index.html"):
                try:
                    with open(UI_HTML_PATH, encoding="utf-8") as f:
                        html = f.read().encode("utf-8")
                except OSError as e:
                    self._send_json(500, {"error": f"Không đọc được ui.html: {e}"})
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(html)
                return

            if path == "/api/health":
                self._send_json(200, {"status": "ok"})
                return

            if path == "/api/lessons":
                raw_lessons = tools_mod._load_lessons()
                public_lessons = [
                    {
                        "code": it.get("code", ""),
                        "day": it.get("day", ""),
                        "topic": it.get("topic", ""),
                        "misconception": it.get("misconception", ""),
                        "check_question": it.get("check_question", ""),
                        "key_points_count": len(it.get("key_points", [])),
                    }
                    for it in raw_lessons
                ]
                provider = getattr(ai_mod, "MODEL_PROVIDER", "fake")
                model_name = getattr(ai_mod, "MODEL_NAME", "")
                api_key = getattr(ai_mod, "API_KEY", "")
                live_ready = provider != "fake" and (provider == "ollama" or bool(api_key))
                self._send_json(
                    200,
                    {
                        "lessons": public_lessons,
                        "runtime": {
                            "provider": provider,
                            "model": model_name or ("fake" if provider == "fake" else ""),
                            "live_ready": live_ready,
                        },
                    },
                )
                return

            self._send_json(404, {"error": "Không tìm thấy đường dẫn."})

        def do_POST(self):  # noqa: N802
            path = urllib.parse.urlparse(self.path).path
            if path != "/api/chat":
                self._send_json(404, {"error": "Không tìm thấy đường dẫn."})
                return
            try:
                length = int(self.headers.get("Content-Length") or "0")
            except ValueError:
                self._send_json(400, {"error": "Content-Length không hợp lệ."})
                return
            if length <= 0 or length > 65536:
                self._send_json(400, {"error": "Kích thước payload không hợp lệ."})
                return
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "JSON đầu vào không hợp lệ."})
                return

            try:
                resp = _process_chat_turn(
                    body.get("text", ""),
                    body.get("active_code", ""),
                    tools_mod,
                    tracing_mod,
                    answer_fn,
                )
            except ValueError as e:
                self._send_json(400, {"error": str(e)})
                return
            except NotImplementedError as e:
                self._send_json(503, {"error": f"Chưa nối model: {e}"})
                return
            except Exception as e:
                self._send_json(502, {"error": f"{type(e).__name__}: {e}"})
                return

            self._send_json(200, resp)

    return AppHandler


def run_cli(tools, tracing, answer) -> int:
    """Chế độ dòng lệnh dự phòng (`py run.py --cli`)."""
    print("=== LỚP HỌC CHỦ ĐỘNG A4 — HỌC BẰNG CÁCH DẠY LẠI ===")
    print("Lệnh nhanh: /ds (xem mã đoạn) · /chon D01-01 (chọn đoạn) · /reset (xóa ngữ cảnh) · Enter 2 lần để thoát.")
    blank = 0
    active_code = ""
    while True:
        prompt_label = f"[{active_code}] > " if active_code else "> "
        try:
            text = input(prompt_label).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0

        low = text.lower()
        if low in ("/ds", "/list"):
            _print_lessons(tools._load_lessons())
            continue
        if low in ("/reset", "/clear"):
            active_code = ""
            print("  (Đã xóa ngữ cảnh đoạn đang học)")
            continue
        if low.startswith("/chon ") or low.startswith("/code "):
            req_code = tools.extract_code(text) or text.split(maxsplit=1)[1].strip().upper()
            passage = tools.get_passage(req_code)
            if passage:
                active_code = passage["code"]
                print("  (Đang học [%s]: %s)" % (active_code, passage.get("topic", "")))
            else:
                print("  (Không tìm thấy mã đoạn '%s' trong data/lessons.json)" % req_code)
            continue

        query_for_agent, next_code = _resolve_input_for_demo(text, active_code, tools)
        if next_code != active_code and next_code:
            p = tools.get_passage(next_code)
            if p:
                print("  (Ngữ cảnh đoạn: [%s] %s)" % (next_code, p.get("topic", "")))
        active_code = next_code

        tracing.begin("app")
        try:
            result = answer(query_for_agent)
        except NotImplementedError as e:
            tracing.end()
            print("Chưa nối model: %s" % e)
            return 1
        except Exception as e:
            tracing.end()
            print("[lỗi] %s: %s" % (type(e).__name__, e))
            continue
        s, _ = tracing.end()
        raw_out = result.get("output", "") if isinstance(result, dict) else str(result)
        print(_format_role_output(raw_out))
        print(
            "   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
            % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"])
        )


def run_server(ai_mod, tools, tracing, answer, host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True) -> int:
    """Khởi chạy Web UI cục bộ bằng thư viện chuẩn Python và tự mở trình duyệt."""
    handler = _make_handler(ai_mod, tools, tracing, answer)
    try:
        server = ThreadingHTTPServer((host, port), handler)
    except OSError:
        server = ThreadingHTTPServer((host, 0), handler)
    actual_port = server.server_address[1]
    url = f"http://{host}:{actual_port}"
    provider = getattr(ai_mod, "MODEL_PROVIDER", "fake")
    model = getattr(ai_mod, "MODEL_NAME", "") or "fake"
    print("=== GTA VIN · LỚP HỌC AI CHỦ ĐỘNG A4 (WEB UI) ===")
    print(f"Đang chạy tại : {url}")
    print(f"Model cấu hình: {provider} / {model}")
    print("Bấm Ctrl+C để dừng · Thêm cờ --cli nếu muốn dùng giao diện dòng lệnh.")
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng máy chủ Web UI.")
    finally:
        server.server_close()
    return 0


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        import ai
        import tools
        import tracing
        from agent import answer
    except Exception as e:
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1

    if "--cli" in args:
        return run_cli(tools, tracing, answer)

    open_browser = "--no-browser" not in args
    port = 8765
    if "--port" in args:
        idx = args.index("--port")
        if idx + 1 < len(args):
            try:
                port = int(args[idx + 1])
            except ValueError:
                print("Giá trị --port phải là số nguyên.")
                return 2
    return run_server(ai, tools, tracing, answer, port=port, open_browser=open_browser)


if __name__ == "__main__":
    sys.exit(main())
