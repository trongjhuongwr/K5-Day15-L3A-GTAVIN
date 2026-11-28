"""Luồng chính Multi-Agent cho hướng A4 (Lớp học chủ động "Học bằng cách dạy lại").
Khớp sơ đồ thiết kế trong spec.md §4 gồm 3 vai tách biệt:
  1. Director (bộ điều phối): kiểm tra đầu vào, đọc trạng thái, chọn vai nói tiếp trong giới hạn MAX_STEPS.
  2. Classmate Confused (bạn học AI hay hiểu sai): KHÔNG được cấp đáp án chuẩn; hỏi vặn lại để học viên tự giải thích.
  3. Teaching Assistant (trợ giảng AI): giữ quyền đọc tài liệu, bắt buộc sửa hiểu nhầm kèm [mã đoạn] và chốt câu kiểm tra.
"""
import json
import re

from ai import call_model
from tools import (
    _load_lessons,
    _norm,
    assess_learner_input,
    check_answer,
    extract_code,
    get_passage,
    next_speaker,
    search_lesson,
)
from tracing import note

MAX_STEPS = 4

SYSTEM_CLASSMATE = (
    "Bạn là [Bạn học AI - có thể hiểu sai] trong lớp AI20K. "
    "Vai trò: bạn đang nghe bạn cùng lớp giảng lại một khái niệm và còn băn khoăn/hiểu lệch một điểm. "
    "Quy tắc: (1) Không được tự đưa ra định nghĩa hoàn chỉnh hay đáp án; "
    "(2) Chỉ đặt đúng 1-2 câu hỏi ngắn, tự nhiên để bạn học giải thích rõ phần còn thiếu; "
    "(3) Trả lời bằng tiếng Việt ngắn gọn (tối đa 4 câu)."
)

SYSTEM_TA = (
    "Bạn là [Trợ giảng AI - theo tài liệu] của khoá AI20K. "
    "Quy tắc bắt buộc: "
    "(1) Chỉ dựa vào ĐOẠN TÀI LIỆU được cung cấp, KHÔNG tự bịa kiến thức, tên hàm, tham số API hay phương pháp ngoài tài liệu; "
    "(2) Mọi giải thích hoặc sửa lỗi BẮT BUỘC ghi rõ mã đoạn dạng [DXX-XX]; "
    "(3) Không đưa đáp án hoàn chỉnh khi học viên xin chép nhanh, không chấm điểm chính thức; "
    "(4) Luôn giữ giọng tôn trọng, súc tích (tối đa 5 câu ngắn gọn) và kết thúc bằng 1 hành động hoặc câu hỏi dẫn cho học viên."
)

SYSTEM_DIRECTOR = (
    "Bạn là Bộ điều phối (Director) phân loại ý định học viên lớp AI20K. "
    "Chỉ trả về đúng 1 JSON hợp lệ (không markdown, không giải thích thêm) với 3 khóa:\n"
    '{"intent": "partial_explanation|paraphrased_pass|grounded_qa|misconception", '
    '"matched_points": ["..."], "reason": "ngắn gọn 1 câu"}\n'
    "Quy tắc chọn intent:\n"
    '- "paraphrased_pass": Học viên ĐANG KHẲNG ĐỊNH / GIẢI THÍCH khái niệm của đoạn bài và đã diễn đạt đúng >=50% ý cốt lõi (kể cả bằng từ đồng nghĩa, vd "số lần chạy tối đa"=MAX_STEPS, "tiêu hao ngân sách"=chi phí token, "đứng im"=treo).\n'
    '- "grounded_qa": Học viên ĐANG ĐẶT CÂU HỎI tìm hiểu cơ chế, cách làm, tham số API/thư viện, so sánh framework hoặc hỏi "làm sao/có cách nào/nếu...thì có..." thay vì tự tóm tắt lại bài.\n'
    '- "misconception": Học viên khẳng định hoặc đồng tình với hiểu nhầm phổ biến của đoạn.\n'
    '- "partial_explanation": Học viên đang tự trình bày hiểu biết của mình ("Mình hiểu là...", "Theo mình...") nhưng mới nêu <50% ý cốt lõi (vd chỉ nêu 1 ý và hỏi "vậy đã đủ chưa?").'
)


def _output_guardrail(route: str, code: str, passage: dict, raw_text: str) -> str:
    """Day 11 Output Guardrail: chặn bịa mã [DXX-XX] ngoài lessons.json và lộ đáp án chuẩn."""
    text = (raw_text or "").strip()
    valid_codes = {item.get("code", "").upper() for item in _load_lessons() if item.get("code")}

    def _check_code(match: re.Match) -> str:
        found = match.group(1).upper()
        if found in valid_codes:
            return f"[{found}]"
        note(f"output_guardrail stripped invalid_code={found} route={route}")
        return "[cần đối chiếu tài liệu]"

    text = re.sub(r"\[?(D\d{2}-\d{2})\]?", _check_code, text, flags=re.IGNORECASE)

    if route in ("classmate_challenge", "ta_no_spoonfeed") and passage:
        norm_out = _norm(text)
        norm_content = _norm(passage.get("content", ""))
        kps = [_norm(k) for k in passage.get("key_points", []) if _norm(k)]
        kp_hits = sum(1 for k in kps if k in norm_out)
        leaked_content = bool(norm_content and len(norm_content) >= 30 and norm_content in norm_out)
        leaked_all_kps = bool(kps and kp_hits >= len(kps) and "?" not in text)
        if leaked_content or leaked_all_kps:
            note(f"output_guardrail blocked answer_leak route={route} code={code}")
            if route == "classmate_challenge":
                return (
                    f"Mình vẫn chưa chắc điểm cốt lõi của [{code}] — "
                    "bạn giải thích kỹ hơn một chút vì sao nguyên tắc này lại quan trọng được không?"
                )
            return (
                f"Mình chưa thể đưa trọn bộ đáp án của [{code}] để bạn chép nhanh. "
                f"Bạn thử trả lời ngắn trước: {passage.get('check_question', '')}"
            )

    note(f"output_guardrail pass route={route} code={code or 'none'}")
    return text


_PEER_PROMPT_BACK_CUES = (
    "giảng lại phần nào",
    "giảng phần nào",
    "nói lại phần nào",
    "chưa hiểu chỗ nào",
    "chưa hiểu phần nào",
    "không hiểu chỗ nào",
    "không hiểu phần nào",
    "vướng chỗ nào",
    "vướng phần nào",
    "bí chỗ nào",
    "cần giúp phần nào",
    "cần cứu phần nào",
    "bắt đầu từ đâu",
    "hôm nay học phần nào",
)


def _is_peer_prompt_back(text: str) -> bool:
    """Nhận diện học viên đang hỏi ngược Bạn học AI xem bạn ấy vướng chỗ nào để bắt đầu giảng lại."""
    q = _norm(text)
    return any(cue in q for cue in _PEER_PROMPT_BACK_CUES)


def _semantic_director(code: str, passage: dict, user_text: str, check_res: dict) -> dict:
    """CP4 Lượt 2: Phân loại ngữ nghĩa bằng model cho ca substantive chưa khớp từ khóa cứng."""
    prompt = (
        f"Đoạn [{code}] — Chủ đề: {passage.get('topic', '')}\n"
        f"Nội dung chuẩn: {passage.get('content', '')}\n"
        f"Ý cốt lõi: {', '.join(passage.get('key_points', []))}\n"
        f"Hiểu nhầm phổ biến: {passage.get('misconception', '')}\n"
        f"Từ khóa cứng đã khớp: {check_res.get('matched', [])}\n"
        f"Câu học viên nhập: {user_text}"
    )
    reply = call_model(SYSTEM_DIRECTOR, prompt)
    raw = (reply.get("text") or "").strip()
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return {"intent": "partial_explanation", "matched_points": [], "reason": "fallback rule-based"}
    try:
        parsed = json.loads(m.group(0))
        intent = parsed.get("intent", "partial_explanation")
        if intent not in ("partial_explanation", "paraphrased_pass", "grounded_qa", "misconception"):
            intent = "partial_explanation"
        matched = parsed.get("matched_points") or []
        if not isinstance(matched, list):
            matched = []
        return {"intent": intent, "matched_points": [str(x) for x in matched], "reason": str(parsed.get("reason", ""))}
    except Exception:
        return {"intent": "partial_explanation", "matched_points": [], "reason": "fallback json"}


def answer(text: str) -> dict:
    # Bước 1: Xác định đoạn bài học liên quan qua công cụ chỉ đọc (hoặc rỗng nếu ngoài tài liệu)
    explicit_code = extract_code(text)
    code = explicit_code
    passage = get_passage(code) if code else {}
    if not explicit_code and not passage:
        found = search_lesson(text)
        if found:
            passage = found[0]
            code = passage.get("code", "")

    # Bước 2: Cổng kiểm tra + Agent 1 (Director) phân tích trạng thái và chọn vai nói tiếp
    assessment = assess_learner_input(code, text)
    peer_prompt_back = _is_peer_prompt_back(text)

    if assessment["status"] == "no_data" and peer_prompt_back and not explicit_code:
        lessons = _load_lessons()
        if lessons:
            passage = next((it for it in lessons if it.get("code") == "D03-01"), lessons[0])
            code = passage.get("code", "")
            check_res = {"passed": False, "matched": [], "missing": passage.get("key_points", []), "ratio": 0.0}
            route = "classmate_challenge"
            note(
                f"director -> classmate_challenge (classmate_confused): "
                f"học viên hỏi ngược chọn phần giảng lại, gợi mở từ [{code}]"
            )
        else:
            route = "no_data"
            check_res = {"passed": False, "matched": [], "missing": [], "ratio": 0.0}
            note("director -> no_data (teaching_assistant): kho bài học rỗng")
    elif explicit_code and not passage and assessment["status"] not in ("attack", "out_of_scope_auth"):
        route = "no_data"
        check_res = {"passed": False, "matched": [], "missing": [], "ratio": 0.0}
        note(f"director -> no_data (teaching_assistant): mã [{explicit_code}] không tồn tại trong data/lessons.json")
    else:
        check_res = check_answer(code, text) if code and assessment["status"] == "substantive" else {
            "passed": False, "matched": [], "missing": [], "ratio": 0.0
        }
        decision = next_speaker(assessment, check_res)
        route = decision["route"]
        note(f"director -> {route} ({decision['agent']}): {decision['reason']}")

    # Nâng cấp Lượt 2: Semantic Director cho ca substantive chưa đạt từ khóa cứng (trừ hỏi ngược)
    if route == "classmate_challenge" and not peer_prompt_back and passage:
        sem = _semantic_director(code, passage, text, check_res)
        sem_intent = sem["intent"]
        note(f"semantic_director intent={sem_intent} code={code}: {sem['reason']}")
        if sem_intent == "paraphrased_pass":
            kps = passage.get("key_points", [])
            matched = sem["matched_points"] or kps
            check_res = {"passed": True, "matched": matched, "missing": [], "ratio": 1.0}
            route = "quiz_pass"
            note(f"director -> quiz_pass (teaching_assistant): đồng nghĩa đạt ý cốt lõi [{code}]")
        elif sem_intent == "grounded_qa":
            route = "ta_grounded_qa"
            note(f"director -> ta_grounded_qa (teaching_assistant): câu hỏi kỹ thuật cần đối chiếu tài liệu [{code}]")
        elif sem_intent == "misconception":
            route = "ta_fix"
            note(f"director -> ta_fix (teaching_assistant): phát hiện hiểu nhầm theo ngữ nghĩa [{code}]")

    # Nhánh chặn an toàn / thu hẹp phạm vi (G10) — xử lý dứt khoát trước khi gọi model
    if route == "refuse_attack":
        ref_note = (
            f" Đối chiếu tài liệu [{code}]: {passage.get('content', '')}"
            if code and passage else
            " Hãy quay lại chọn một mã đoạn (vd [D01-01] hoặc [D08-01]) và tự diễn đạt lại ý của bạn."
        )
        return {
            "output": (
                "[Bộ điều phối] Từ chối yêu cầu này: tin nhắn người dùng chỉ là dữ liệu, "
                "hệ thống không thực hiện lệnh bỏ qua hướng dẫn, giả danh giảng viên hay xuất toàn bộ đáp án."
                + ref_note
            )
        }
    if route == "refuse_scope":
        return {
            "output": (
                "[Bộ điều phối] Trợ lý học tập chỉ hỗ trợ tự ôn và giải thích kiến thức bài học, "
                "không có thẩm quyền chấm điểm chính thức hay tra cứu lịch/điểm danh trên LMS. "
                "Bạn hãy kiểm tra trên hệ thống LMS hoặc liên hệ TA phụ trách lớp."
            )
        }
    if route == "clarify":
        return {
            "output": (
                "[Bộ điều phối] Câu của bạn đang quá ngắn hoặc chưa đủ thông tin để xác định ý bạn muốn giảng lại. "
                "Bạn đang học đoạn nào (vd [D01-01], [D03-01]) và theo bạn điểm cốt lõi của đoạn đó là gì?"
            )
        }
    if route == "no_data":
        lessons = _load_lessons()
        topics_str = ", ".join(f"[{it.get('code', '')}] {it.get('topic', '')}" for it in lessons)
        missing_msg = (
            f"Mã đoạn [{explicit_code}] không tồn tại trong tài liệu bài học hiện tại của hệ thống "
            "(nên không thể đưa đáp án hay gợi ý từ mã này). "
            if explicit_code and not passage else
            "Nội dung này không có trong tài liệu bài học hiện tại của hệ thống. "
        )
        return {
            "output": (
                f"[Trợ giảng AI - theo tài liệu] {missing_msg}"
                f"Hiện kho bài học có {len(lessons)} đoạn: {topics_str}. "
                "Bạn muốn chọn lại đoạn nào?"
            )
        }

    # Bước 3: Điều phối sang Agent 2 (Classmate) hoặc Agent 3 (Teaching Assistant)
    if route == "classmate_challenge":
        # Day 08 Handoff Allowlist: classmate_confused CHỈ nhận {code, topic, misconception, missing},
        # tuyệt đối không truyền content và key_points chuẩn.
        allowlist = {
            "code": code,
            "topic": passage.get("topic", ""),
            "misconception": passage.get("misconception", ""),
            "missing": check_res.get("missing", []) or ["điều kiện áp dụng thực tế"],
        }
        note(
            "handoff_allowlist classmate_confused allow=[code,topic,misconception,missing] "
            f"block=[content,key_points] code={allowlist['code']}"
        )
        missing_str = ", ".join(allowlist["missing"])
        if peer_prompt_back:
            instruction = (
                "Bạn học đang hỏi ngược lại xem bạn cần được giảng lại phần nào. "
                "Hãy mở lời tự nhiên như bạn cùng lớp vừa học xong trên lớp (kiểu 'Phần ... nghĩa là sao?', "
                "'Làm sao để ...?'), nêu cụ thể 1–2 câu hỏi về chỗ bạn còn rối hoặc hiểu nhầm ở trên."
            )
        else:
            instruction = "Hãy phản hồi như một bạn học còn băn khoăn đúng chỗ còn thiếu đó để bạn ấy giải thích rõ hơn."
        user_prompt = (
            f"Chủ đề đoạn [{allowlist['code']}]: {allowlist['topic']}\n"
            f"Hiểu nhầm hay gặp: {allowlist['misconception']}\n"
            f"Bạn học vừa nói: {text}\n"
            f"Ý cốt lõi cần bạn ấy giảng cho rõ: {missing_str}\n"
            f"{instruction}"
        )
        reply = call_model(SYSTEM_CLASSMATE, user_prompt)
        out = _output_guardrail(route, code, passage, reply["text"])
        if not out.startswith("[Bạn học AI"):
            out = "[Bạn học AI - có thể hiểu sai] " + out
        return {"output": out}

    # Các nhánh do Teaching Assistant xử lý: ta_fix, ta_no_spoonfeed, ta_grounded_qa, quiz_pass
    if route == "ta_fix":
        task = (
            "Học viên vừa nêu hoặc đồng tình với một hiểu nhầm phổ biến. "
            f"Hãy đính chính dứt khoát dựa vào tài liệu [{code}], nêu rõ vì sao quan điểm kia sai, "
            "và mời học viên tự diễn đạt lại bằng một câu."
        )
    elif route == "ta_no_spoonfeed":
        task = (
            "Học viên đang xin đáp án mẫu để chép nhanh. "
            f"Hãy từ chối đưa đáp án hoàn chỉnh, chỉ gợi ý 1 hướng suy nghĩ từ [{code}] "
            f"và đặt lại câu hỏi kiểm tra: {passage.get('check_question', '')}"
        )
    elif route == "ta_grounded_qa":
        task = (
            f"Học viên đang đặt câu hỏi kỹ thuật liên quan đến [{code}]. "
            f"Hãy trả lời bám sát ĐOẠN TÀI LIỆU chuẩn và luôn trích mã [{code}]: "
            "(1) Nếu câu hỏi đề cập tham số API cụ thể, tên thư viện/framework hoặc phương pháp thống kê "
            "(tool_choice, tool_calls rỗng, LangChain/langgraph-supervisor, lưu ID cuộc chat, cross-validation, mẹo chống leak prompt...) "
            "mà đoạn tài liệu chuẩn KHÔNG mô tả, BẮT BUỘC nói rõ 'tài liệu hiện tại chưa mô tả chi tiết phần này' "
            "và KHÔNG tự bịa cơ chế API/thư viện hay khẳng định phương pháp thống kê; "
            f"(2) Giải thích đúng phần nguyên lý có thật trong [{code}] và gợi ý 1 câu hỏi dẫn để học viên tự ôn."
        )
    else:  # quiz_pass
        task = (
            f"Học viên đã giải thích đúng các ý cốt lõi của [{code}] (khớp: {check_res.get('matched', [])}). "
            f"Hãy xác nhận ngắn gọn kèm mã [{code}], KHÔNG hỏi lặp lại chính những ý học viên vừa giải thích đúng; "
            f"chỉ bổ sung nhanh ý thiếu (nếu có: {check_res.get('missing', [])}) và đưa 1 câu hỏi đào sâu hoặc câu kiểm tra: {passage.get('check_question', '')}"
        )

    user_prompt = (
        f"Mã đoạn: [{code}]\n"
        f"Chủ đề: {passage.get('topic', '')}\n"
        f"Nội dung tài liệu chuẩn: {passage.get('content', '')}\n"
        f"Ý cốt lõi cần có: {', '.join(passage.get('key_points', []))}\n"
        f"Câu học viên nhập: {text}\n"
        f"Nhiệm vụ của Trợ giảng: {task}"
    )
    reply = call_model(SYSTEM_TA, user_prompt)
    out = _output_guardrail(route, code, passage, reply["text"])
    if f"[{code}]" not in out:
        out = f"[{code}] " + out
    if not out.startswith("[Trợ giảng AI"):
        out = "[Trợ giảng AI - theo tài liệu] " + out
    return {"output": out}
