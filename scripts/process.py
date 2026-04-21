"""抓取、整理并保存诈骗案例数据。"""

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


def generate_id(content: str) -> str:
    """根据案例内容生成稳定 ID。"""
    return hashlib.md5(content.encode("utf-8")).hexdigest()[:8]


def deduplicate(new_cases: list[dict], existing_cases: list[dict]) -> list[dict]:
    """按 ID 去重，只保留新增案例。"""
    existing_ids = {case["id"] for case in existing_cases}
    return [case for case in new_cases if case["id"] not in existing_ids]


def process_case(raw_case: dict) -> dict:
    """把原始抓取结果补充成结构化案例。"""
    extracted = extract_case_info(
        raw_case.get("title", ""),
        raw_case.get("content", ""),
    )

    return {
        "id": generate_id(raw_case.get("content", "")),
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
    """读取已有发布数据；文件不存在时返回空列表。"""
    if not cases_file.exists():
        return []

    with cases_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data: list[dict]) -> None:
    """统一使用 UTF-8 保存 JSON。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def main() -> None:
    """执行抓取、处理、去重和保存流程。"""
    print("开始抓取诈骗案例数据...")

    spider = FanZhaSpider()
    list_items = spider.fetch_list(page=1)
    print(f"获取到 {len(list_items)} 条列表项。")

    raw_cases: list[dict] = []
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
    new_cases = deduplicate(processed_cases, existing_cases)
    print(f"新增 {len(new_cases)} 条案例（去重后）。")

    all_cases = existing_cases + new_cases
    save_json(cases_file, all_cases)
    print(f"发布数据已保存到: {cases_file}")
    print(f"当前累计案例数: {len(all_cases)}")

    generate_case_pages(all_cases)
    print("案例文档页已生成。")


if __name__ == "__main__":
    main()
