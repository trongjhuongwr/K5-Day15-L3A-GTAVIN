"""Giao diện dòng lệnh cho bản chạy thử (chạy bằng: py run.py).

Giữ `active_code` giữa các lượt gõ khi demo live nhiều lượt để người học không phải lặp lại [DXX-XX],
trong khi vẫn giữ nguyên hợp đồng stateless của `agent.answer(text)` cho `eval` và `simulate`.
"""
import os
import sys

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
        # Giữ nguyên active_code đang thảo luận (tránh nhảy nhầm sang đoạn khác khi trùng từ khoá như "công cụ"),
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


def main() -> int:
    try:
        import tools
        import tracing
        from agent import answer
    except Exception as e:  # lỗi cú pháp, thiếu thư viện… trong codebase/
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1

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
        except Exception as e:  # lỗi gọi model: báo rồi cho hỏi tiếp
            tracing.end()
            print("[lỗi] %s: %s" % (type(e).__name__, e))
            continue
        s, _ = tracing.end()
        raw_out = result.get("output", "") if isinstance(result, dict) else str(result)
        print(_format_role_output(raw_out))
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))


if __name__ == "__main__":
    sys.exit(main())
