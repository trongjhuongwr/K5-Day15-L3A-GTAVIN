"""Công cụ của bài toán A4 (Lớp học chủ động) — khớp spec.md §4.
Mỗi công cụ có @tool và docstring 4 ý: mô tả · input · output · tác động ra ngoài.
"""
import json
import os
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_PATH = os.path.join(ROOT, "data", "lessons.json")

_ATTACK_PATTERNS = (
    "bỏ qua mọi hướng dẫn",
    "bỏ qua hướng dẫn",
    "ignore previous",
    "toàn bộ đáp án",
    "tất cả đáp án",
    "in ra đáp án",
    "quản trị viên",
    "tôi là giảng viên",
    "xác nhận từ hôm nay",
)
_GRADE_PATTERNS = (
    "chấm cho tôi",
    "chấm điểm",
    "cho tôi 10 điểm",
    "qua môn",
    "lịch thi",
    "điểm danh",
)
_SPOONFEED_PATTERNS = (
    "đưa luôn đáp án",
    "cho đáp án",
    "đáp án mẫu",
    "chép cho nhanh",
    "giải hộ",
    "làm hộ",
)
_LOW_EFFORT_EXACT = {"ok", "đúng", "đúng rồi", "ok đúng", "sai rồi", "lỗi rồi", "uk", "ừ", "yes", "no", "?"}


def _norm(text: str) -> str:
    s = unicodedata.normalize("NFC", (text or "")).lower().strip()
    return re.sub(r"\s+", " ", s)


def _load_lessons() -> list:
    if not os.path.exists(LESSONS_PATH):
        return []
    with open(LESSONS_PATH, encoding="utf-8") as f:
        return json.load(f)


def extract_code(text: str) -> str:
    m = re.search(r"\[(D\d{2}-\d{2})\]", (text or "").upper())
    if m:
        return m.group(1)
    m2 = re.search(r"\b(D\d{2}-\d{2})\b", (text or "").upper())
    return m2.group(1) if m2 else ""


@tool
def get_passage(code: str) -> dict:
    """Lấy đầy đủ một đoạn kiến thức trong data/lessons.json theo mã đoạn.
    Input: mã đoạn (str, vd 'D01-01'). Output: dict đoạn bài học hoặc {} nếu không tồn tại. Không tác động ra ngoài."""
    target = (code or "").strip().upper()
    for item in _load_lessons():
        if item.get("code", "").upper() == target:
            return item
    return {}


_STOPWORDS = {
    "trong", "này", "cách", "viết", "bằng", "trên", "cho", "của", "không", "như",
    "thế", "nào", "khi", "làm", "một", "các", "những", "được", "với", "từ", "về",
    "theo", "mình", "bạn", "hỏi", "thì", "hay", "hoặc", "nhưng", "vẫn", "đang",
    "cần", "phải", "nên", "thực", "hiện", "của", "khoá", "khóa", "bài", "học",
}


@tool
def search_lesson(query: str) -> list:
    """Tìm tối đa 2 đoạn bài học phù hợp nhất với câu hỏi/giải thích của học viên trong data/lessons.json.
    Input: câu chữ người học (str). Output: danh sách dict đoạn kèm điểm khớp. Không tác động ra ngoài."""
    q = _norm(query)
    code = extract_code(query)
    lessons = _load_lessons()
    if code:
        for item in lessons:
            if item.get("code", "").upper() == code:
                return [dict(item, score=100)]

    scored = []
    for item in lessons:
        kw_hits = 0
        for kw in item.get("keywords", []):
            if _norm(kw) in q:
                kw_hits += 1
        topic_words = [
            w for w in re.findall(r"\w+", _norm(item.get("topic", "")))
            if len(w) >= 3 and w not in _STOPWORDS
        ]
        t_hits = sum(1 for w in topic_words if w in q)
        if kw_hits >= 1 or t_hits >= 3:
            scored.append((kw_hits * 3 + t_hits, item))
    scored.sort(key=lambda x: -x[0])
    return [dict(it, score=sc) for sc, it in scored[:2]]


@tool
def assess_learner_input(code: str, user_text: str) -> dict:
    """Kiểm tra an toàn đầu vào và đánh giá trạng thái câu trả lời của học viên (cổng chặn + độ sâu).
    Input: mã đoạn (str), nội dung học viên gõ (str). Output: dict trạng thái phân loại và chi tiết. Không tác động ra ngoài."""
    q = _norm(user_text)
    stripped_no_code = re.sub(r"\[?d\d{2}-\d{2}\]?", "", q).strip(" .,:;!?-")

    if any(p in q for p in _ATTACK_PATTERNS):
        return {"status": "attack", "code": code, "reason": "phát hiện prompt injection / giả danh / đòi xuất toàn bộ đáp án"}
    if any(p in q for p in _GRADE_PATTERNS):
        return {"status": "out_of_scope_auth", "code": code, "reason": "yêu cầu chấm điểm chính thức hoặc hỏi thông tin ngoài phạm vi bài học"}
    if not stripped_no_code or len(stripped_no_code) <= 15 or stripped_no_code in _LOW_EFFORT_EXACT:
        return {"status": "short_or_low_effort", "code": code, "reason": "câu quá ngắn (<=15 ký tự) hoặc trả lời đối phó 1-2 chữ"}
    if any(p in q for p in _SPOONFEED_PATTERNS):
        return {"status": "spoonfeed", "code": code, "reason": "yêu cầu đưa thẳng đáp án mẫu mà chưa tự giải thích"}

    passage = get_passage(code) if code else {}
    if not passage:
        return {"status": "no_data", "code": "", "reason": "không tìm thấy đoạn kiến thức phù hợp trong data/lessons.json"}

    # Kiểm tra dấu hiệu học viên đồng tình với hiểu nhầm phổ biến
    misconception_cues = {
        "D01-01": ("không cần lập trình thêm", "chỉ cần gọi thẳng api"),
        "D01-02": ("hết bịa đặt 100%", "nói đúng hoàn toàn"),
        "D03-01": ("gộp hết vào system prompt", "không cần tách tool"),
        "D04-01": ("không cần đặt giới hạn bước", "tự lặp đến khi xong"),
        "D05-01": ("tự thực hiện mọi hành động", "không cần người duyệt"),
        "D06-01": ("giả lập tự sinh làm bằng chứng", "hợp lệ mà"),
        "D08-01": ("càng nhiều agent càng tốt",),
        "D11-01": ("chỉ cần dặn nhẹ", "tự miễn nhiễm"),
    }
    cues = misconception_cues.get(passage["code"], ())
    if any(c in q for c in cues) or ("bạn học ai bảo" in q and "đúng" in q):
        return {"status": "misconception_match", "code": passage["code"], "reason": "học viên đang nêu hoặc đồng tình với hiểu nhầm phổ biến"}

    return {"status": "substantive", "code": passage["code"], "reason": "câu giải thích có nội dung cụ thể"}


@tool
def check_answer(code: str, user_text: str) -> dict:
    """Đối chiếu câu giải thích/trả lời của học viên với các ý cốt lõi của đoạn bài học.
    Input: mã đoạn (str), câu trả lời (str). Output: dict gồm số ý đạt, ý còn thiếu, và passed (bool). Không tác động ra ngoài."""
    passage = get_passage(code)
    if not passage:
        return {"passed": False, "matched": [], "missing": [], "ratio": 0.0}
    q = _norm(user_text)
    kps = passage.get("key_points", [])
    matched = [kp for kp in kps if _norm(kp) in q]
    missing = [kp for kp in kps if _norm(kp) not in q]
    ratio = len(matched) / len(kps) if kps else 0.0
    return {"passed": ratio >= 0.5, "matched": matched, "missing": missing, "ratio": round(ratio, 2)}


@tool
def next_speaker(assessment: dict, check_res: dict) -> dict:
    """Bộ điều phối (Director) quyết định vai nào nói tiếp theo trạng thái học viên.
    Input: kết quả assess_learner_input và check_answer. Output: dict {route, agent, reason}. Không tác động ra ngoài."""
    st = assessment.get("status")
    if st == "attack":
        return {"route": "refuse_attack", "agent": "guard", "reason": assessment.get("reason", "")}
    if st == "out_of_scope_auth":
        return {"route": "refuse_scope", "agent": "guard", "reason": assessment.get("reason", "")}
    if st == "short_or_low_effort":
        return {"route": "clarify", "agent": "director", "reason": assessment.get("reason", "")}
    if st == "no_data":
        return {"route": "no_data", "agent": "director", "reason": assessment.get("reason", "")}
    if st == "spoonfeed":
        return {"route": "ta_no_spoonfeed", "agent": "teaching_assistant", "reason": assessment.get("reason", "")}
    if st == "misconception_match":
        return {"route": "ta_fix", "agent": "teaching_assistant", "reason": assessment.get("reason", "")}

    ratio = check_res.get("ratio", 0.0)
    if ratio >= 0.75:
        return {"route": "quiz_pass", "agent": "teaching_assistant", "reason": "học viên giải thích đủ ý cốt lõi, chuyển sang xác nhận và câu kiểm tra"}
    return {"route": "classmate_challenge", "agent": "classmate_confused", "reason": "học viên hiểu một phần, cần Bạn học AI hỏi vặn ý còn thiếu"}
