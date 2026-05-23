#!/usr/bin/env python3
"""Build aggregate-only summaries from AI Hub finance counseling labels.

The script deliberately excludes raw text fields such as consulting_content,
question, answer, follow_up_question, and output.
"""

from __future__ import annotations

import csv
import json
import os
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT.parent / "3.개방데이터" / "1.데이터"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def iter_label_json():
    for zip_path in DATA_ROOT.glob("*/02.라벨링데이터/*.zip"):
        split = zip_path.parts[-3]
        domain = zip_path.stem.split("_")[1]
        with zipfile.ZipFile(zip_path) as zf:
            for name in zf.namelist():
                if not name.endswith(".json"):
                    continue
                payload = json.loads(zf.read(name))
                yield split, domain, payload


def safe_value(value):
    if value is None:
        return "<NULL>"
    return str(value)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    counters = {
        "split_domain": Counter(),
        "consulting_category": Counter(),
        "consulting_topic": Counter(),
        "task_category": Counter(),
        "consulting_situation": Counter(),
        "qa_topic": Counter(),
        "core_financial_terms": Counter(),
    }
    source_counts = Counter()
    missing_counts = Counter()
    total_rows = 0

    for split, domain, payload in iter_label_json():
        total_rows += 1
        source = payload.get("source", {})
        consulting = payload.get("consulting", {})
        qa_rows = payload.get("qa_data", []) or []
        qa = qa_rows[0] if qa_rows else {}

        counters["split_domain"][(split, domain)] += 1
        counters["consulting_category"][safe_value(consulting.get("consulting_category"))] += 1
        counters["consulting_topic"][safe_value(consulting.get("consulting_topic"))] += 1
        counters["task_category"][safe_value(qa.get("task_category"))] += 1
        counters["consulting_situation"][safe_value(qa.get("consulting_situation"))] += 1
        counters["qa_topic"][safe_value(qa.get("qa_topic"))] += 1
        counters["core_financial_terms"][safe_value(qa.get("core_financial_terms"))] += 1

        source_id = source.get("source_id")
        if source_id:
            source_counts[(split, domain, source_id)] += 1

        for field_name, value in {
            "consulting_category": consulting.get("consulting_category"),
            "consulting_topic": consulting.get("consulting_topic"),
            "task_category": qa.get("task_category"),
            "consulting_situation": qa.get("consulting_situation"),
            "qa_topic": qa.get("qa_topic"),
            "consulting_purpose": qa.get("consulting_purpose"),
        }.items():
            if value is None:
                missing_counts[field_name] += 1

    metrics = {
        "label_rows": total_rows,
        "unique_labeled_source_ids": len(source_counts),
        "sources_with_multiple_qa": sum(1 for count in source_counts.values() if count > 1),
        "max_qa_per_source": max(source_counts.values()) if source_counts else 0,
        "missing_counts": dict(missing_counts),
    }

    with (OUTPUT_DIR / "project_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    with (OUTPUT_DIR / "label_distribution_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "count"])
        for metric, counter in counters.items():
            for value, count in counter.most_common():
                if isinstance(value, tuple):
                    value = " / ".join(value)
                writer.writerow([metric, value, count])

    print(f"Wrote {OUTPUT_DIR / 'project_metrics.json'}")
    print(f"Wrote {OUTPUT_DIR / 'label_distribution_summary.csv'}")


if __name__ == "__main__":
    main()
