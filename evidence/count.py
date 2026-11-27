"""Script đếm số liệu bằng chứng từ data/preclass/ (Track A · A4).
Chạy lại được bằng:
    py evidence/count.py --data ../K5-L3-Day15-AI-Product-Hackathon/data/preclass
(hoặc đặt bộ preclass vào data-btc/preclass/ — đã có trong .gitignore, không commit).
Chỉ dùng thư viện chuẩn Python 3.10+.
"""
import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from statistics import quantiles

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pct(x, n):
    return (100.0 * x / n) if n else 0.0


def main():
    p = argparse.ArgumentParser(description="Đếm chỉ số pain từ data/preclass/")
    p.add_argument("--data", default=os.path.join("data-btc", "preclass"),
                   help="Đường dẫn tới thư mục chứa các file CSV preclass")
    args = p.parse_args()
    d = args.data
    if not os.path.isdir(d):
        sys.exit(f"Không tìm thấy thư mục dữ liệu: {d}")

    learners = load_csv(os.path.join(d, "learners.csv"))
    chat = load_csv(os.path.join(d, "chat.csv"))
    answers = load_csv(os.path.join(d, "answers.csv"))
    rewards = load_csv(os.path.join(d, "rewards.csv"))
    class_events = load_csv(os.path.join(d, "class_events.csv"))

    # 1. Đếm từ events.csv (streaming để nhẹ RAM)
    active_hvs = set()
    ev_counts = Counter()
    lecture_openings_by_hv = Counter()
    agent_shown = 0
    agent_replied_total = 0
    agent_no_cite = 0
    agent_missing_ctx = 0
    lab_opened = 0
    lab_completed = 0
    lab_skipped = 0

    with open(os.path.join(d, "events.csv"), encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            active_hvs.add(row["hv"])
            t = row["type"]
            ev_counts[t] += 1
            if t == "lecture_opened":
                lecture_openings_by_hv[row["hv"]] += 1
            elif t == "agent_message_shown":
                agent_shown += 1
            elif t == "agent_replied":
                agent_replied_total += 1
                data = json.loads(row["data"]) if row["data"] else {}
                if not data.get("moc_trich_dan"):
                    agent_no_cite += 1
                if data.get("missing_context") is True:
                    agent_missing_ctx += 1
            elif t == "lab_opened":
                lab_opened += 1
            elif t == "lab_completed":
                lab_completed += 1
                data = json.loads(row["data"]) if row["data"] else {}
                if data.get("skipped") is True:
                    lab_skipped += 1

    # 2. Đếm từ class_events.csv (director_decided)
    dir_total = 0
    dir_inserted = 0
    for row in class_events:
        if row["type"] == "director_decided":
            dir_total += 1
            data = json.loads(row["data"]) if row["data"] else {}
            if data.get("inserted") is True:
                dir_inserted += 1

    # 3. Đếm từ chat.csv
    chat_total = len(chat)
    chat_hvs = {r["hv"] for r in chat}
    disc_replies = sum(1 for r in chat if r["channel"] == "video_discussion_reply")
    short_q = sum(1 for r in chat if r["do_dai_cau_hoi"] and int(r["do_dai_cau_hoi"]) <= 15)

    # 4. Đếm từ answers.csv
    chat_ans = [r for r in answers if r["nguon"] == "chat"]
    chat_graded = [r for r in chat_ans if r["trang_thai_cham"] == "da_cham" and r["rubric_y_moi"] != ""]
    y_moi_0 = sum(1 for r in chat_graded if r["rubric_y_moi"] == "0")
    bam_bai_0 = sum(1 for r in chat_graded if r["rubric_bam_bai"] == "0")

    short_ids = {r["id"] for r in chat if r["do_dai_cau_hoi"] and int(r["do_dai_cau_hoi"]) <= 15}
    short_graded = [r for r in chat_graded if r["ref"] in short_ids]
    short_bam_bai_0 = sum(1 for r in short_graded if r["rubric_bam_bai"] == "0")

    post_ans = [r for r in answers if r["nguon"] == "pre_post_post"]
    post_first = [r for r in post_ans if r["lan_thu"] == "1"]
    post_wrong_all = sum(1 for r in post_ans if r["was_correct"] == "False")
    post_wrong_first = sum(1 for r in post_first if r["was_correct"] == "False")
    post_hvs = {r["hv"] for r in post_ans}
    post_hvs_wrong = {r["hv"] for r in post_first if r["was_correct"] == "False"}

    # 5. Đếm từ rewards.csv
    rew_by_type = Counter(r["hanh_vi"] for r in rewards)

    print("=== TONG QUAN TAP DU LIEU ===")
    print(f"Tai khoan learners.csv: {len(learners)}")
    print(f"Hoc vien co hoat dong (events.csv): {len(active_hvs)}/{len(learners)} ({pct(len(active_hvs), len(learners)):.1f}%)")
    print(f"Hoc vien tung nhan AI (chat.csv): {len(chat_hvs)}/{len(active_hvs)} ({pct(len(chat_hvs), len(active_hvs)):.1f}%)")
    print()
    active_openings = [lecture_openings_by_hv[hv] for hv in active_hvs]
    if active_openings:
        quartiles = quantiles(active_openings, n=4, method="inclusive") if len(active_openings) > 1 else active_openings * 3
        monthly_openings = [count * 30 / 20 for count in active_openings]
        low = sum(count <= 8 for count in monthly_openings)
        medium = sum(8 < count <= 18 for count in monthly_openings)
        high = len(monthly_openings) - low - medium
        openings_total = sum(active_openings)
        openers = len(lecture_openings_by_hv)
        mean = openings_total / openers if openers else 0.0
        print("=== LUOT MO BAI VA PERSONA ===")
        print(f"lecture_opened: {openings_total} luot / {openers} nguoi mo bai ({mean:.2f} luot/nguoi)")
        print(f"P25, P50, P75 tren {len(active_openings)} hoc vien hoat dong: {quartiles}")
        print(f"So nguoi theo luot mo bai quy doi thang (x30/20): <=8: {low}; >8 den 18: {medium}; >18: {high}")
        print()

    print("=== CHI SO PAIN CHINH (A4 - LOP HOC CHU DONG) ===")
    print(f"1. Bo dieu phoi chen ban hoc AI: {dir_inserted}/{dir_total} ({pct(dir_inserted, dir_total):.1f}%) doan bai giang")
    print(f"2. Luot ban hoc AI hien cho hoc vien (agent_message_shown): {agent_shown}")
    print(f"   Phan hoi trong thao luan duoi video (video_discussion_reply): {disc_replies}/{agent_shown} ({pct(disc_replies, agent_shown):.2f}%)")
    print(f"3. Cau nhan AI da cham co rubric_y_moi = 0 (khong co y moi): {y_moi_0}/{len(chat_graded)} ({pct(y_moi_0, len(chat_graded)):.1f}%)")
    print(f"4. Cau nhan AI da cham co rubric_bam_bai = 0: {bam_bai_0}/{len(chat_graded)} ({pct(bam_bai_0, len(chat_graded)):.1f}%)")
    print(f"5. Cau hoi ngan <= 15 ky tu: {short_q}/{chat_total} ({pct(short_q, chat_total):.1f}%)")
    print(f"   Trong cac cau ngan da cham, bi rubric_bam_bai = 0: {short_bam_bai_0}/{len(short_graded)} ({pct(short_bam_bai_0, len(short_graded)):.1f}%)")
    print(f"6. AI tra loi thieu moc trich dan (moc_trich_dan rong): {agent_no_cite}/{agent_replied_total} ({pct(agent_no_cite, agent_replied_total):.1f}%)")
    print(f"   AI tra loi bi missing_context = True: {agent_missing_ctx}/{agent_replied_total} ({pct(agent_missing_ctx, agent_replied_total):.1f}%)")
    print(f"7. Bai kiem tra cuoi ngay (pre_post_post) sai o lan dau (lan_thu=1): {post_wrong_first}/{len(post_first)} ({pct(post_wrong_first, len(post_first)):.1f}%)")
    print(f"   Tong luot pre_post_post sai (moi lan thu): {post_wrong_all}/{len(post_ans)} ({pct(post_wrong_all, len(post_ans)):.1f}%)")
    print(f"   So hoc vien tung sai it nhat 1 cau pre_post_post lan dau: {len(post_hvs_wrong)}/{len(post_hvs)} ({pct(len(post_hvs_wrong), len(post_hvs)):.1f}%)")
    print(f"8. Mini-lab ket thuc nhung bam skipped=True: {lab_skipped}/{lab_completed} ({pct(lab_skipped, lab_completed):.1f}%) (mo lab: {lab_opened})")
    print(f"9. Thuong hanh vi giai thich / phan hoi xay dung (rewards.csv, tong {len(rewards)} dong): "
          f"giai_thich={rew_by_type.get('giai_thich', 0)}, phan_hoi_xay_dung={rew_by_type.get('phan_hoi_xay_dung', 0)}, "
          f"du_doan={rew_by_type.get('du_doan', 0)}, sua_sai={rew_by_type.get('sua_sai', 0)}")


if __name__ == "__main__":
    main()
