"""Generate timeline, region, hotness, and insight pages from cases."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_CASES_DIR = ROOT_DIR / "docs" / "cases"
DOCS_INSIGHTS_DIR = ROOT_DIR / "docs" / "insights"


def format_currency(amount: float) -> str:
    if amount >= 10000:
        return f"{amount / 10000:.1f} 万元"
    if amount > 0:
        return f"{int(amount)} 元"
    return "未披露"


def case_link(case: dict) -> str:
    return f"/cases/generated/{case.get('id', 'unknown-case')}"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_by_time(cases: list[dict]) -> str:
    groups: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        key = case.get("incident_month") or "未识别时间"
        groups[key].append(case)

    ordered_keys = sorted(groups.keys(), reverse=True)
    lines = [
        "# 按时间查看案例",
        "",
        "以下列表按案例发生时间归类，适合快速查看最近高发的诈骗类型。",
        "",
    ]

    for key in ordered_keys:
        lines.append(f"## {key}")
        lines.append("")
        for case in groups[key]:
            lines.append(
                f"- [{case.get('title', '未命名案例')}]({case_link(case)})"
                f" | {case.get('scam_type', '待分类')}"
                f" | {case.get('region') or '地区待识别'}"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_by_region(cases: list[dict]) -> str:
    groups: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        key = case.get("region") or case.get("source_region") or "未识别地区"
        groups[key].append(case)

    ordered = sorted(groups.items(), key=lambda item: (len(item[1]), item[0]), reverse=True)
    lines = [
        "# 按区域查看案例",
        "",
        "以下列表按地区归类，便于观察本地或相近区域更常见的诈骗套路。",
        "",
    ]

    for region, items in ordered:
        type_counter = Counter(case.get("scam_type", "待分类") for case in items)
        suspect_counter = Counter(case.get("suspect_region_scope", "暂无法研判") for case in items)
        lines.append(f"## {region}（{len(items)} 条）")
        lines.append("")
        lines.append(f"- 高频类型：{', '.join(name for name, _ in type_counter.most_common(3))}")
        lines.append(f"- 常见嫌疑人范围：{suspect_counter.most_common(1)[0][0]}")
        lines.append("")
        for case in items[:12]:
            lines.append(f"- [{case.get('title', '未命名案例')}]({case_link(case)})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_by_heat(cases: list[dict]) -> str:
    hottest = sorted(
        cases,
        key=lambda item: (
            item.get("heat_score", 0),
            item.get("loss_amount_cny", 0),
            item.get("incident_date", ""),
        ),
        reverse=True,
    )

    lines = [
        "# 按热度查看案例",
        "",
        "热度综合考虑了损失金额、近期性、诈骗类型和受骗人群，仅用于站内快速研判。",
        "",
    ]

    for case in hottest:
        lines.extend(
            [
                f"## [{case.get('title', '未命名案例')}]({case_link(case)})",
                "",
                f"- 热度等级：{case.get('heat_level', '关注')}（{case.get('heat_score', 0)} 分）",
                f"- 损失金额：{format_currency(case.get('loss_amount_cny', 0))}",
                f"- 所属地区：{case.get('region') or case.get('source_region') or '待识别'}",
                f"- 诈骗类型：{case.get('scam_type') or '待分类'}",
                f"- 嫌疑人范围：{case.get('suspect_region_scope') or '暂无法研判'}",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def build_trend_summary(cases: list[dict]) -> tuple[list[str], list[str], list[str], list[str]]:
    sorted_cases = sorted(
        cases,
        key=lambda item: item.get("incident_date") or item.get("crawled_at", ""),
        reverse=True,
    )
    recent_cases = sorted_cases[:12]

    recent_counter = Counter(case.get("scam_type", "待分类") for case in recent_cases)
    overall_counter = Counter(case.get("scam_type", "待分类") for case in sorted_cases)
    region_counter = Counter(case.get("region") or case.get("source_region") or "未识别地区" for case in sorted_cases)
    suspect_counter = Counter(case.get("suspect_region_scope", "暂无法研判") for case in sorted_cases)

    findings = [
        f"当前样本中出现最多的诈骗类型是“{name}”，共 {count} 条。"
        for name, count in overall_counter.most_common(3)
    ]

    predictions: list[str] = []
    for scam_type, recent_count in recent_counter.most_common(5):
        overall_count = overall_counter.get(scam_type, 0)
        recent_share = recent_count / max(len(recent_cases), 1)
        overall_share = overall_count / max(len(sorted_cases), 1)
        if recent_count >= 2 and recent_share >= overall_share:
            predictions.append(
                f"短期内“{scam_type}”仍可能持续活跃，建议优先更新对应场景页和家庭提醒话术。"
            )

    if not predictions:
        predictions.append("当前样本波动不大，近期仍以退款客服、投资理财、刷单返利等通用高发类型为主。")

    warnings: list[str] = []
    for region, count in region_counter.most_common(6):
        region_cases = [
            case
            for case in sorted_cases
            if (case.get("region") or case.get("source_region") or "未识别地区") == region
        ]
        avg_heat = sum(case.get("heat_score", 0) for case in region_cases) / max(len(region_cases), 1)
        top_type = Counter(case.get("scam_type", "待分类") for case in region_cases).most_common(1)[0][0]
        suspect_scope = Counter(case.get("suspect_region_scope", "暂无法研判") for case in region_cases).most_common(1)[0][0]

        if count >= 10 or avg_heat >= 84:
            level = "红色"
        elif count >= 5 or avg_heat >= 70:
            level = "橙色"
        else:
            level = "黄色"

        warnings.append(
            f"{level}预警：{region} 当前样本 {count} 条，主导类型为“{top_type}”，常见嫌疑人范围为“{suspect_scope}”，平均热度 {avg_heat:.0f} 分。"
        )

    suspect_findings = [
        f"高频嫌疑人活动范围：{scope}（{count} 条）"
        for scope, count in suspect_counter.most_common(4)
    ]
    return findings, predictions, warnings, suspect_findings


def render_insights_index(cases: list[dict]) -> str:
    findings, predictions, warnings, suspect_findings = build_trend_summary(cases)
    lines = [
        "# 趋势研判中心",
        "",
        "以下内容由案例库自动汇总生成，用于站内趋势观察、区域预警和快速研判。",
        "",
        "- [诈骗趋势分析](/insights/trends)",
        "- [区域预警](/insights/regions)",
        "- [按时间查看案例](/cases/by-time)",
        "- [按热度查看案例](/cases/by-heat)",
        "- [按区域查看案例](/cases/by-region)",
        "",
        "## 重点观察",
        "",
    ]
    lines.extend(f"- {item}" for item in findings[:3])
    lines.extend(["", "## 嫌疑人范围研判", ""])
    lines.extend(f"- {item}" for item in suspect_findings[:4])
    lines.extend(["", "## 短期预测", ""])
    lines.extend(f"- {item}" for item in predictions[:3])
    lines.extend(["", "## 区域预警", ""])
    lines.extend(f"- {item}" for item in warnings[:5])
    lines.extend(
        [
            "",
            "> 以上结论为基于已收录案例的自动研判，不等同于官方警情通报，也不能替代线下侦查结论。",
            "",
        ]
    )
    return "\n".join(lines)


def render_trends(cases: list[dict]) -> str:
    findings, predictions, _, suspect_findings = build_trend_summary(cases)
    type_counter = Counter(case.get("scam_type", "待分类") for case in cases)
    lines = [
        "# 诈骗趋势分析",
        "",
        f"最近更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 样本结论",
        "",
    ]
    lines.extend(f"- {item}" for item in findings)
    lines.extend(["", "## 类型分布", ""])
    lines.extend(f"- {name}：{count} 条" for name, count in type_counter.most_common(12))
    lines.extend(["", "## 嫌疑人范围分布", ""])
    lines.extend(f"- {item}" for item in suspect_findings)
    lines.extend(["", "## 自动预测", ""])
    lines.extend(f"- {item}" for item in predictions)
    lines.extend(
        [
            "",
            "> 预测逻辑基于案例数量、近期性、损失金额、诈骗类型聚集，以及嫌疑人活动范围线索的自动分析。",
            "",
        ]
    )
    return "\n".join(lines)


def render_regions(cases: list[dict]) -> str:
    _, _, warnings, suspect_findings = build_trend_summary(cases)
    region_counter = Counter(case.get("region") or case.get("source_region") or "未识别地区" for case in cases)
    lines = [
        "# 区域预警",
        "",
        "以下预警基于当前已收录案例的区域分布、平均热度以及嫌疑人范围线索，仅作站内提示参考。",
        "",
        "## 预警结论",
        "",
    ]
    lines.extend(f"- {item}" for item in warnings)
    lines.extend(["", "## 嫌疑人活动范围高频判断", ""])
    lines.extend(f"- {item}" for item in suspect_findings)
    lines.extend(["", "## 区域样本数量", ""])
    lines.extend(f"- {region}：{count} 条" for region, count in region_counter.most_common(12))
    lines.append("")
    return "\n".join(lines)


def generate_case_reports(cases: list[dict]) -> None:
    """Generate case classification and insight pages."""
    ordered_cases = sorted(
        cases,
        key=lambda case: case.get("incident_date") or case.get("crawled_at", ""),
        reverse=True,
    )
    write_text(DOCS_CASES_DIR / "by-time.md", render_by_time(ordered_cases))
    write_text(DOCS_CASES_DIR / "by-region.md", render_by_region(ordered_cases))
    write_text(DOCS_CASES_DIR / "by-heat.md", render_by_heat(ordered_cases))
    write_text(DOCS_INSIGHTS_DIR / "index.md", render_insights_index(ordered_cases))
    write_text(DOCS_INSIGHTS_DIR / "trends.md", render_trends(ordered_cases))
    write_text(DOCS_INSIGHTS_DIR / "regions.md", render_regions(ordered_cases))
