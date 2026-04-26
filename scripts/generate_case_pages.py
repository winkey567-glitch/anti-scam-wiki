"""Generate static case pages from published cases."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_CASES_DIR = ROOT_DIR / "docs" / "cases"
GENERATED_DIR = DOCS_CASES_DIR / "generated"
PUBLISHED_CASES_FILE = ROOT_DIR / "data" / "published" / "cases.json"


def ensure_cases_file() -> list[dict]:
    """Ensure cases.json exists and return its content."""
    PUBLISHED_CASES_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not PUBLISHED_CASES_FILE.exists():
        PUBLISHED_CASES_FILE.write_text("[]\n", encoding="utf-8")
        return []

    with PUBLISHED_CASES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def format_list(items: list[str]) -> str:
    """Convert a string list into a Markdown list."""
    if not items:
        return "- 暂无"
    return "\n".join(f"- {item}" for item in items if item)


def case_slug(case: dict) -> str:
    """Generate a stable case page filename."""
    return case.get("id", "unknown-case")


def format_currency(amount: float) -> str:
    if amount >= 10000:
        return f"{amount / 10000:.1f} 万元"
    if amount > 0:
        return f"{int(amount)} 元"
    return "未披露"


def render_case_page(case: dict) -> str:
    """Render a single case detail page."""
    title = case.get("title") or "未命名案例"
    summary = case.get("summary") or "暂无摘要。"
    source_url = case.get("source_url") or ""
    source_name = case.get("source_name") or "未知来源"
    scenario = case.get("scenario") or "待识别"
    scam_type = case.get("scam_type") or "待分类"
    psychological_trap = case.get("psychological_trap") or "待分析"
    target_group = "、".join(case.get("target_group", []) or ["待分析"])
    crawled_at = case.get("crawled_at", "")
    incident_date = case.get("incident_date") or "待识别"
    region = case.get("region") or case.get("source_region") or "待识别"
    heat = f"{case.get('heat_level', '关注')}（{case.get('heat_score', 0)} 分）"
    loss_amount = format_currency(case.get("loss_amount_cny", 0))
    suspect_region_scope = case.get("suspect_region_scope") or "暂无法研判"
    suspect_region_confidence = case.get("suspect_region_confidence") or "低"
    suspect_region_basis = case.get("suspect_region_basis") or "公开案情缺少可直接锁定嫌疑人所在区域的线索。"
    source_line = f"[{source_name}]({source_url})" if source_url else source_name

    return f"""# {title}

> {summary}

## 基本信息

- 诈骗类型：{scam_type}
- 具体场景：{scenario}
- 目标人群：{target_group}
- 发生时间：{incident_date}
- 所属区域：{region}
- 热度等级：{heat}
- 涉及金额：{loss_amount}
- 嫌疑人区域范围：{suspect_region_scope}
- 研判把握度：{suspect_region_confidence}
- 心理弱点：{psychological_trap}
- 数据来源：{source_line}
- 抓取时间：{crawled_at or "未知"}

## 关键话术

{format_list(case.get("key_phrases", []))}

## 危险信号

{format_list(case.get("red_flags", []))}

## 预防措施

{format_list(case.get("counter_measures", []))}

## 应急处理

{format_list(case.get("emergency_actions", []))}

## 嫌疑人区域研判

- 范围判断：{suspect_region_scope}
- 把握度：{suspect_region_confidence}
- 依据：{suspect_region_basis}

## 原始说明

本页由自动化脚本生成，适合作为后续人工审核和整理的基础版本。
"""


def render_latest_page(cases: list[dict]) -> str:
    """Render the latest case summary page."""
    if not cases:
        return """# 最新案例

当前还没有正式入库的案例。

你可以先查看：
- [诈骗场景总览](/scenarios/)
- [人群分类总览](/profiles/)
- [案例库说明](/cases/)
"""

    lines = [
        "# 最新案例",
        "",
        "以下页面由 `data/published/cases.json` 自动生成，适合持续补充和人工审核。",
        "",
        "- [按时间查看](/cases/by-time)",
        "- [按热度查看](/cases/by-heat)",
        "- [按区域查看](/cases/by-region)",
        "",
    ]

    for case in cases:
        title = case.get("title") or "未命名案例"
        summary = case.get("summary") or "暂无摘要。"
        slug = case_slug(case)
        lines.extend(
            [
                f"## [{title}](/cases/generated/{slug})",
                "",
                summary,
                "",
                f"- 诈骗类型：{case.get('scam_type') or '待分类'}",
                f"- 目标人群：{'、'.join(case.get('target_group', []) or ['待分析'])}",
                f"- 所属区域：{case.get('region') or case.get('source_region') or '待识别'}",
                f"- 嫌疑人范围：{case.get('suspect_region_scope') or '暂无法研判'}",
                f"- 热度等级：{case.get('heat_level', '关注')}（{case.get('heat_score', 0)} 分）",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def render_generated_index(cases: list[dict]) -> str:
    """Render the generated directory index page."""
    count = len(cases)
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 自动生成案例页",
        "",
        f"当前共有 {count} 条案例页面，由脚本自动生成。",
        f"最近生成时间：{updated_at}",
        "",
        "- [查看最新案例汇总](/cases/latest)",
        "- [按时间查看](/cases/by-time)",
        "- [按热度查看](/cases/by-heat)",
        "- [按区域查看](/cases/by-region)",
        "",
    ]

    if count == 0:
        lines.append("当前暂无案例详情页。")
    else:
        for case in cases:
            title = case.get("title") or "未命名案例"
            lines.append(f"- [{title}](/cases/generated/{case_slug(case)})")

    return "\n".join(lines).rstrip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_case_pages(cases: list[dict] | None = None) -> None:
    """Generate case list pages and detail pages."""
    cases = ensure_cases_file() if cases is None else cases
    ordered_cases = sorted(
        cases,
        key=lambda case: case.get("incident_date") or case.get("crawled_at", ""),
        reverse=True,
    )

    if GENERATED_DIR.exists():
        shutil.rmtree(GENERATED_DIR)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    for case in ordered_cases:
        write_text(GENERATED_DIR / f"{case_slug(case)}.md", render_case_page(case))

    write_text(DOCS_CASES_DIR / "latest.md", render_latest_page(ordered_cases))
    write_text(GENERATED_DIR / "index.md", render_generated_index(ordered_cases))


if __name__ == "__main__":
    generate_case_pages()
