"""Fetch, structure, and publish anti-scam cases."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

try:
    from crawl.sources.fanzha import FanZhaSpider
    from ai.extractor import extract_case_info
    from generate_case_pages import generate_case_pages
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from crawl.sources.fanzha import FanZhaSpider
    from ai.extractor import extract_case_info
    from generate_case_pages import generate_case_pages


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PUBLISHED_DIR = DATA_DIR / "published"
RAW_FETCH_LIMIT = 5


def case_identity(case: dict) -> str:
    """Build a stable identity using source url plus title."""
    title = case.get("title", "").strip()
    source_url = case.get("source_url", "").strip()
    if title or source_url:
        return f"{source_url}|{title}"
    return case.get("content", "").strip()


def generate_id(title: str, source_url: str, content: str) -> str:
    """Create a stable short id for a case."""
    seed = f"{source_url.strip()}|{title.strip()}"
    if not seed.strip("|"):
        seed = content
    return hashlib.md5(seed.encode("utf-8")).hexdigest()[:8]


def process_case(raw_case: dict) -> dict:
    """Turn raw scraped content into a structured case record."""
    title = raw_case.get("title", "").strip()
    content = raw_case.get("content", "").strip()
    extracted = extract_case_info(title, content)

    return {
        "id": generate_id(title, raw_case.get("source_url", ""), content),
        "source_url": raw_case.get("source_url", ""),
        "source_name": raw_case.get("source_name", ""),
        "source_reliability": raw_case.get("source_reliability", "community"),
        "crawled_at": raw_case.get("crawled_at", datetime.now().isoformat()),
        "processed_at": datetime.now().isoformat(),
        "status": "pending_review",
        "content_lifecycle": "new",
        **extracted,
    }


def load_existing_cases(cases_file: Path) -> list[dict]:
    """Read existing published cases."""
    if not cases_file.exists():
        return []

    with cases_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data: list[dict]) -> None:
    """Persist JSON with UTF-8 output."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def merge_cases(existing_cases: list[dict], processed_cases: list[dict]) -> tuple[list[dict], int, int]:
    """Upsert cases by id so existing entries get refreshed."""
    existing_map = {case_identity(case): case for case in existing_cases}
    updated = 0
    inserted = 0

    for case in processed_cases:
        identity = case_identity(case)
        previous = existing_map.get(identity)

        if previous is None:
            existing_map[identity] = case
            inserted += 1
            continue

        merged = {**previous, **case}

        if previous.get("status") and previous.get("status") != "pending_review":
            merged["status"] = previous["status"]
        if previous.get("content_lifecycle") and previous.get("content_lifecycle") != "new":
            merged["content_lifecycle"] = previous["content_lifecycle"]
        if previous.get("editor_notes"):
            merged["editor_notes"] = previous["editor_notes"]

        existing_map[identity] = merged
        updated += 1

    ordered = sorted(
        existing_map.values(),
        key=lambda item: item.get("crawled_at", ""),
        reverse=True,
    )
    return ordered, inserted, updated


def main() -> None:
    """Run fetch, structure, merge, and publish."""
    print("开始抓取诈骗案例数据...")

    spider = FanZhaSpider()
    raw_cases: list[dict]

    if hasattr(spider, "fetch_cases"):
        raw_cases = spider.fetch_cases()
        print(f"从官方文章中提取到 {len(raw_cases)} 条案例。")
    else:
        list_items = spider.fetch_list(page=1)
        print(f"获取到 {len(list_items)} 条列表项。")

        raw_cases = []
        for item in list_items[:RAW_FETCH_LIMIT]:
            title = item.get("title", "").strip() or "未命名案例"
            print(f"抓取详情: {title[:30]}...")
            detail = spider.fetch_detail(item.get("url", ""))
            if detail:
                raw_cases.append(detail)

    print(f"成功抓取 {len(raw_cases)} 条详情。")

    raw_file = RAW_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_json(raw_file, raw_cases)
    print(f"原始数据已保存到: {raw_file}")

    print("开始结构化处理...")
    processed_cases = [process_case(case) for case in raw_cases]

    cases_file = PUBLISHED_DIR / "cases.json"
    existing_cases = load_existing_cases(cases_file)
    all_cases, inserted, updated = merge_cases(existing_cases, processed_cases)

    print(f"新增 {inserted} 条案例。")
    print(f"刷新 {updated} 条已有案例。")

    save_json(cases_file, all_cases)
    print(f"发布数据已保存到: {cases_file}")
    print(f"当前累计案例数: {len(all_cases)}")

    generate_case_pages(all_cases)
    print("案例文档页已生成。")


if __name__ == "__main__":
    main()
