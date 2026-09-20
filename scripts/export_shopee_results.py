"""Export saved Shopee benchmark evidence as UTF-8 text, without API calls.

Usage: python -m scripts.export_shopee_results [--details]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def compact(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def retrieval_lines(label: str, rows: list[dict], hit: bool) -> list[str]:
    lines = [f"{label}; hit@3={str(hit).lower()}", ""]
    for row in rows:
        metadata = row["metadata"]
        lines.extend([
            f"Rank {row['rank']} | doc_id={metadata['doc_id']} | chunk_index={metadata['chunk_index']}",
            f"score={row['score']} | answer_bearing={str(row['answer_bearing']).lower()}",
            f"Nguồn: {row.get('source_url') or metadata['source_url']}",
            f"Metadata: {compact(metadata)}",
            "Nội dung chunk đầy đủ:",
            *("    " + line for line in row["content"].splitlines()),
            "",
        ])
    return lines


def render(data: dict, strategies: list[str], source_name: str) -> str:
    student = data["student"]
    lines = [
        "# Minh chứng benchmark đơn hàng Shopee", "",
        f"Sinh viên: {student['name']} | MSSV: {student['student_id']} | Nhóm {student['group_size']} người",
        f"Thời điểm ghi kết quả: {data['recorded_at']}",
        f"JSON nguồn: {source_name}",
        f"Embedding: {data['provider']} / {data['backend']} / {data['embedding_dimensions']} chiều",
        f"LLM: {data['llm']['provider']} / {data['llm']['model']}",
        f"Cấu hình: {compact(data['strategy_configs'])}",
        f"Sử dụng API/cache trong lần chạy: {compact(data['api_usage_this_run'])}", "",
        "Heading là chiến lược cá nhân của Phan Danh Đạt. Fixed-size và recursive là các cấu hình",
        "so sánh được chạy trên cùng máy; không phải kết quả do hai thành viên khác tự thực hiện.",
        "answer_bearing=true khi cùng một chunk có đúng doc_id và đủ các cụm bằng chứng yêu cầu.",
        "Hit@3 đo việc tìm thấy ít nhất một chunk như vậy; không tự động chứng minh câu trả lời LLM đúng.",
        "Gold answer và bằng chứng được giữ để người đọc đối chiếu. chunk_index bắt đầu từ 0.", "",
    ]
    if data.get("methodology", {}).get("quality_warning"):
        lines.extend([data["methodology"]["quality_warning"], ""])
    for strategy in strategies:
        result = data["results"][strategy]
        metric = result["hit_at_3"]
        lines.extend([
            f"## Chiến lược: {strategy}", "",
            f"Tham số: {compact(data['strategy_configs'][strategy])}",
            f"Số chunks: {result['chunk_count']} | Hit@3: {metric['hits']}/{metric['queries']} ({metric['rate']:.1%})", "",
        ])
        for query in result["queries"]:
            filters = query.get("metadata_filter")
            lines.extend([
                f"### {query['id']}", "", f"Câu hỏi gốc: {query['question']}",
                f"Metadata filter: {compact(filters)}", f"Gold answer: {query['gold_answer']}",
                f"Bằng chứng yêu cầu: {compact(query['evidence'])}", "",
            ])
            label = "Top-3 có lọc metadata" if filters else "Top-3 không lọc metadata"
            lines.extend(retrieval_lines(label, query["top3"], query["hit_at_3"]))
            if "without_filter" in query:
                comparison = query["without_filter"]
                lines.extend(retrieval_lines("Đối chứng top-3 bỏ filter", comparison["top3"], comparison["hit_at_3"]))
            lines.extend([
                "Câu hỏi đưa vào agent (bao gồm phạm vi metadata khi có):", query["generation_question"], "",
                f"Câu trả lời agent nguyên văn (answer_mode={query['answer_mode']}; dùng top-3 chính ở trên):",
                query["answer"], "",
            ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "report/shopee_benchmark_gemini_gemini.json")
    parser.add_argument("--output", type=Path, default=ROOT / "report/ket_qua_benchmark.txt")
    parser.add_argument("--details", action="store_true", help="Also export all three configurations as Markdown")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        exports = {args.output: render(data, ["heading"], args.input.name)}
        if args.details:
            exports[args.output.parent / "SHOPEE_BENCHMARK_DETAILS.md"] = render(
                data, ["heading", "fixed_size", "recursive"], args.input.name)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Export failed ({type(exc).__name__}); provide a complete benchmark JSON. No reports were written.")
        return 1
    for path, content in exports.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"Saved {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
