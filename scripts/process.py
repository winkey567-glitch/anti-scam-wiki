"""Fetch, structure, analyze, and publish anti-scam cases."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

try:
    from crawl.sources.fanzha import FanZhaSpider
    from ai.extractor import extract_case_info
    from generate_case_pages import generate_case_pages
    from generate_case_reports import generate_case_reports
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from crawl.sources.fanzha import FanZhaSpider
    from ai.extractor import extract_case_info
    from generate_case_pages import generate_case_pages
    from generate_case_reports import generate_case_reports


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PUBLISHED_DIR = DATA_DIR / "published"
RAW_FETCH_LIMIT = 5
REGION_PATTERN = re.compile(r"([\u4e00-\u9fa5]{2,12}(?:省|市|州|县|区))")

TITLE_TYPE_RULES = [
    (["投资", "理财", "炒股", "证券"], "投资理财诈骗"),
    (["婚恋", "恋爱", "交友"], "婚恋交友诈骗"),
    (["刷单返利"], "刷单返利诈骗"),
    (["退改签", "机票"], "机票退改签诈骗"),
    (["客服", "百万保障"], "冒充客服退款诈骗"),
    (["购物", "服务"], "虚假购物服务诈骗"),
    (["贷款"], "贷款诈骗"),
    (["领导", "熟人"], "冒充领导 / 熟人诈骗"),
    (["公检法", "民警", "安全账户"], "冒充公检法诈骗"),
    (["短视频", "代运营"], "短视频代运营诈骗"),
    (["游戏", "装备", "交易"], "游戏交易诈骗"),
]

MANUAL_TITLE_OVERRIDES = [
    (
        ["投资", "理财", "炒股", "证券"],
        {
            "scam_type": "投资理财诈骗",
            "scenario": "虚假投资平台",
            "target_group": ["盲目投资型", "有积蓄的老年人"],
            "key_phrases": ["内幕消息", "稳赚高收益", "缴纳保证金后即可提现"],
            "red_flags": ["高收益低风险", "先小额盈利后诱导加码", "提现时不断加收费用"],
            "counter_measures": ["投资前核实平台资质", "高收益默认高风险", "大额投资先与家人确认"],
            "emergency_actions": ["停止继续投入", "保存平台和转账记录", "立即报警"],
            "psychological_trap": "利用快速获利和沉没成本心理",
        },
    ),
    (
        ["婚恋", "恋爱", "交友"],
        {
            "scam_type": "婚恋交友诈骗",
            "scenario": "情感关系诱导转账",
            "target_group": ["单身人群", "空巢独居型"],
            "key_phrases": ["我对你是真心的", "包裹被扣需要交税", "先帮我周转一下"],
            "red_flags": ["短时间建立亲密关系", "很快开始谈钱", "以包裹、就医或困难为由索要转账"],
            "counter_measures": ["陌生关系涉及金钱一律先停", "先核实真实身份和现实关系", "与家人沟通后再决定"],
            "emergency_actions": ["停止继续付款", "保留聊天和账户信息", "及时报警"],
            "psychological_trap": "利用情感依赖和同情心",
        },
    ),
    (
        ["刷单返利"],
        {
            "scam_type": "刷单返利诈骗",
            "scenario": "垫资返利陷阱",
            "target_group": ["贪小便宜型", "想做兼职补贴家用的人群"],
            "key_phrases": ["动动手指就能赚钱", "先垫资后返现", "再做一单就能提现"],
            "red_flags": ["先返小钱建立信任", "金额越来越大", "提现被卡住要求继续补钱"],
            "counter_measures": ["任何先垫资兼职都不参与", "不要继续补钱", "保留聊天和支付记录"],
            "emergency_actions": ["停止转账", "联系平台和银行", "尽快报警"],
            "psychological_trap": "利用小利诱惑和回本执念",
        },
    ),
    (
        ["客服", "百万保障", "退改签"],
        {
            "scam_type": "冒充客服退款诈骗",
            "scenario": "平台扣费 / 退款取消",
            "target_group": ["技术懵懂型", "网购老年人"],
            "key_phrases": ["不取消就会自动扣费", "需要下载软件处理", "需要共享屏幕或提供验证码"],
            "red_flags": ["主动来电处理退款", "要求下载陌生 App", "要求共享屏幕或验证码"],
            "counter_measures": ["只在官方 App 内处理退款", "不下载陌生软件", "验证码绝不外泄"],
            "emergency_actions": ["立即停止操作", "联系银行止付", "保留聊天和转账证据"],
            "psychological_trap": "利用害怕扣费和急于退款的心理",
        },
    ),
    (
        ["购物", "服务", "代购"],
        {
            "scam_type": "虚假购物服务诈骗",
            "scenario": "脱离平台私下交易",
            "target_group": ["网购人群", "热衷抢票和代购的人群"],
            "key_phrases": ["内部渠道更便宜", "私下转账省手续费", "下单后马上帮你处理"],
            "red_flags": ["要求脱离平台私聊", "承诺特殊渠道或内部票", "要求直接转到个人账户"],
            "counter_measures": ["交易只走官方平台", "不信低价内部渠道", "不为抢票代购私下转账"],
            "emergency_actions": ["停止继续支付", "保留聊天和订单信息", "联系平台和警方"],
            "psychological_trap": "利用稀缺感和捡漏心理",
        },
    ),
]

REGION_CANONICAL = {
    "商水县": "商水县",
    "新源县": "新源县",
    "华容县": "华容县",
    "铜陵市": "铜陵市",
    "重庆市": "重庆市",
    "红河州": "红河州",
    "全国": "全国",
}

HIGH_RISK_TYPES = {
    "冒充客服退款诈骗",
    "刷单返利诈骗",
    "投资理财诈骗",
    "冒充公检法诈骗",
    "贷款诈骗",
    "婚恋交友诈骗",
    "机票退改签诈骗",
}

HIGH_RISK_GROUPS = {"未成年人家庭", "空巢独居型", "认知衰退型"}

SUSPECT_OVERSEAS_CLUES = [
    "境外",
    "海外",
    "国外",
    "缅北",
    "东南亚",
    "柬埔寨",
    "菲律宾",
    "老挝",
    "Telegram",
    "WhatsApp",
]

SUSPECT_REMOTE_CLUES = [
    "远程控制",
    "共享屏幕",
    "会议APP",
    "聊天平台",
    "社交平台",
    "短视频平台",
    "投资平台",
    "直播间",
    "下载APP",
    "线上指导",
]

SUSPECT_LOCAL_CLUES = [
    "同城",
    "附近",
    "上门",
    "学校老师",
    "奶茶店",
    "店内",
]

REMOTE_SCAM_TYPES = {
    "冒充客服退款诈骗",
    "投资理财诈骗",
    "刷单返利诈骗",
    "婚恋交友诈骗",
    "机票退改签诈骗",
    "短视频代运营诈骗",
}


def case_identity(case: dict) -> str:
    """Build a stable identity using source url plus title."""
    title = case.get("title", "").strip()
    source_url = case.get("source_url", "").strip()
    if title or source_url:
        return f"{source_url}|{title}"
    return case.get("raw_content", case.get("content", "")).strip()


def generate_id(title: str, source_url: str, content: str) -> str:
    """Create a stable short id for a case."""
    seed = f"{source_url.strip()}|{title.strip()}"
    if not seed.strip("|"):
        seed = content
    return hashlib.md5(seed.encode("utf-8")).hexdigest()[:8]


def extract_incident_date(text: str, source_year: int | None) -> str:
    """Extract a normalized incident date."""
    full = re.search(r"(20\d{2})年(\d{1,2})月(\d{1,2})日", text)
    if full:
        year, month, day = full.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    year_month = re.search(r"(20\d{2})年(\d{1,2})月", text)
    if year_month:
        year, month = year_month.groups()
        return f"{int(year):04d}-{int(month):02d}-01"

    current_year = re.search(r"今年(\d{1,2})月(\d{1,2})日", text)
    if current_year and source_year:
        month, day = current_year.groups()
        return f"{source_year:04d}-{int(month):02d}-{int(day):02d}"

    current_year_month = re.search(r"今年(\d{1,2})月", text)
    if current_year_month and source_year:
        month = current_year_month.group(1)
        return f"{source_year:04d}-{int(month):02d}-01"

    month_only = re.search(r"(?<!\d)(\d{1,2})月(\d{1,2})日", text)
    if month_only and source_year:
        month, day = month_only.groups()
        return f"{source_year:04d}-{int(month):02d}-{int(day):02d}"

    return ""


def normalize_region_name(region: str, source_region: str, content: str) -> str:
    """Collapse noisy place strings into stable regional labels."""
    text = " ".join(part for part in [region, source_region, content] if part)
    for keyword, canonical in REGION_CANONICAL.items():
        if keyword in text:
            return canonical

    region = region.strip()
    region = re.sub(r"^(家住|居住在|位于|来自)", "", region)
    region = re.sub(r"(老城区|新城区|城区)$", "", region)
    return region or source_region


def extract_region(text: str, fallback_region: str) -> str:
    """Extract a meaningful region label."""
    for region in REGION_PATTERN.findall(text):
        if region in {"网站", "公安局", "人民政府"}:
            continue
        if region.startswith("家住"):
            region = region.replace("家住", "", 1)
        if region.startswith("位于"):
            region = region.replace("位于", "", 1)
        return normalize_region_name(region, fallback_region, text)
    return normalize_region_name("", fallback_region, text)


def collect_region_mentions(text: str) -> list[str]:
    """Collect canonical place mentions that appear in case details."""
    mentions: list[str] = []
    for region in REGION_PATTERN.findall(text):
        normalized = normalize_region_name(region, "", text)
        if normalized and normalized not in mentions:
            mentions.append(normalized)
    return mentions


def infer_suspect_region(
    text: str,
    victim_region: str,
    source_region: str,
    scam_type: str,
) -> dict:
    """Infer a coarse suspect activity range from public case details."""
    mentions = collect_region_mentions(text)
    external_mentions = [
        name for name in mentions if name and name not in {victim_region, source_region, "全国"}
    ]

    overseas_hits = [clue for clue in SUSPECT_OVERSEAS_CLUES if clue in text]
    if overseas_hits:
        return {
            "suspect_region_scope": "疑似境外或境外协同网络团伙",
            "suspect_region_confidence": "中",
            "suspect_region_basis": f"案情提到：{'、'.join(overseas_hits[:3])}",
        }

    if len(external_mentions) >= 2:
        return {
            "suspect_region_scope": f"疑似跨省流窜，活动范围可能涉及{'、'.join(external_mentions[:3])}",
            "suspect_region_confidence": "中",
            "suspect_region_basis": "案情同时出现多个异地地名，更像跨区域网络作案。",
        }

    if external_mentions:
        return {
            "suspect_region_scope": f"疑似异地作案，可能与{external_mentions[0]}有关",
            "suspect_region_confidence": "低",
            "suspect_region_basis": "案情出现了受害地之外的地名线索，但公开信息仍不足以锁定具体位置。",
        }

    remote_hits = [clue for clue in SUSPECT_REMOTE_CLUES if clue in text]
    if remote_hits or scam_type in REMOTE_SCAM_TYPES:
        basis = "、".join(remote_hits[:3]) if remote_hits else "诈骗类型更常见于异地网络作案"
        return {
            "suspect_region_scope": "疑似跨区域远程网络作案",
            "suspect_region_confidence": "低",
            "suspect_region_basis": f"案情依赖线上联系、远控或平台引流等特征：{basis}",
        }

    local_hits = [clue for clue in SUSPECT_LOCAL_CLUES if clue in text]
    if local_hits:
        return {
            "suspect_region_scope": "疑似本地或周边市县配合作案",
            "suspect_region_confidence": "低",
            "suspect_region_basis": f"案情出现“{'、'.join(local_hits[:3])}”等本地接触线索。",
        }

    fallback_region = victim_region or source_region or "具体区域待研判"
    return {
        "suspect_region_scope": f"暂无法从公开细节锁定，倾向{fallback_region}外部的网络化作案",
        "suspect_region_confidence": "低",
        "suspect_region_basis": "公开案情更多反映受害场景和诈骗手法，缺少可直接指向嫌疑人物理位置的线索。",
    }


def extract_source_date(source_url: str, source_year: int | None) -> str:
    """Infer a month-level date from the source article URL when needed."""
    full = re.search(r"/(20\d{2})-(\d{2})/(\d{2})/", source_url)
    if full:
        year, month, day = full.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    compact = re.search(r"/(20\d{2})(\d{2})/", source_url)
    if compact:
        year, month = compact.groups()
        return f"{int(year):04d}-{int(month):02d}-01"

    if source_year:
        return f"{source_year:04d}-01-01"
    return ""


def extract_loss_amount(text: str) -> float:
    """Extract the largest loss amount in RMB."""
    amounts: list[float] = []
    for value, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(万元|元)", text):
        amount = float(value)
        if unit == "万元":
            amount *= 10000
        amounts.append(amount)
    return max(amounts) if amounts else 0.0


def build_heat_score(
    scam_type: str,
    loss_amount_cny: float,
    incident_date: str,
    target_group: list[str],
) -> tuple[int, str]:
    """Create a simple hotness score and label."""
    score = 35

    if loss_amount_cny >= 500000:
        score += 35
    elif loss_amount_cny >= 100000:
        score += 25
    elif loss_amount_cny >= 50000:
        score += 18
    elif loss_amount_cny >= 10000:
        score += 10
    elif loss_amount_cny > 0:
        score += 4

    if scam_type in HIGH_RISK_TYPES:
        score += 8

    if any(group in HIGH_RISK_GROUPS for group in target_group):
        score += 5

    if incident_date.startswith("2025-"):
        score += 6
    elif incident_date.startswith("2024-"):
        score += 3

    score = min(score, 100)
    if score >= 85:
        return score, "极高"
    if score >= 70:
        return score, "高"
    if score >= 55:
        return score, "中"
    return score, "关注"


def enrich_case(raw_case: dict, extracted: dict) -> dict:
    """Add analysis metadata used for filters and reports."""
    title = raw_case.get("title", "").strip()
    content = raw_case.get("content", "").strip()
    text = f"{title}\n{content}"
    source_year = raw_case.get("source_year")
    incident_date = extract_incident_date(text, source_year) or extract_source_date(
        raw_case.get("source_url", ""),
        source_year,
    )
    loss_amount_cny = extract_loss_amount(text)
    target_group = extracted.get("target_group", []) or []
    region = extract_region(text, raw_case.get("source_region", ""))
    suspect_region = infer_suspect_region(
        text,
        region,
        raw_case.get("source_region", ""),
        extracted.get("scam_type", ""),
    )
    heat_score, heat_level = build_heat_score(
        extracted.get("scam_type", ""),
        loss_amount_cny,
        incident_date,
        target_group,
    )

    return {
        "source_region": raw_case.get("source_region", ""),
        "source_year": source_year,
        "incident_date": incident_date,
        "incident_month": incident_date[:7] if incident_date else "",
        "region": region,
        "loss_amount_cny": round(loss_amount_cny, 2),
        "heat_score": heat_score,
        "heat_level": heat_level,
        "raw_content": content,
        **suspect_region,
    }


def apply_manual_title_overrides(title: str, extracted: dict) -> dict:
    """Stabilize key labels for common high-frequency titles."""
    for keywords, override in MANUAL_TITLE_OVERRIDES:
        if any(keyword in title for keyword in keywords):
            return {**extracted, **override}
    return extracted


def process_case(raw_case: dict) -> dict:
    """Turn raw scraped content into a structured case record."""
    title = raw_case.get("title", "").strip()
    content = raw_case.get("content", "").strip()
    extracted = apply_manual_title_overrides(title, extract_case_info(title, content))
    enriched = enrich_case(raw_case, extracted)

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
        **enriched,
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
    """Upsert cases by identity so existing entries get refreshed."""
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
        key=lambda item: item.get("incident_date") or item.get("crawled_at", ""),
        reverse=True,
    )
    return ordered, inserted, updated


def normalize_case_labels(case: dict) -> dict:
    """Apply final title- and region-based cleanup before publishing."""
    title = (case.get("title") or "").strip()
    case["region"] = normalize_region_name(
        case.get("region") or "",
        case.get("source_region") or "",
        case.get("raw_content") or case.get("content") or "",
    )

    for keywords, scam_type in TITLE_TYPE_RULES:
        if any(keyword in title for keyword in keywords):
            case["scam_type"] = scam_type
            break

    if not case.get("incident_month"):
        incident_date = case.get("incident_date") or ""
        if incident_date:
            case["incident_month"] = incident_date[:7]
        else:
            fallback_time = case.get("crawled_at") or ""
            case["incident_month"] = fallback_time[:7] if len(fallback_time) >= 7 else ""

    return case


def normalize_cases(cases: list[dict]) -> list[dict]:
    """Remove obviously broken records and de-duplicate by identity."""
    cleaned: list[dict] = []
    seen: set[str] = set()

    for case in cases:
        title = (case.get("title") or "").strip()
        if title in {"", "诈骗", "案例"}:
            continue

        case = normalize_case_labels(case)
        identity = case_identity(case)
        if identity in seen:
            continue

        seen.add(identity)
        cleaned.append(case)

    return cleaned


def main() -> None:
    """Run fetch, structure, merge, and publish."""
    print("开始抓取诈骗案例数据...")

    spider = FanZhaSpider()
    raw_cases: list[dict]

    if hasattr(spider, "fetch_cases"):
        raw_cases = spider.fetch_cases()
        print(f"从官方文章来源中提取到 {len(raw_cases)} 条案例。")
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
    all_cases = normalize_cases(all_cases)

    print(f"新增 {inserted} 条案例。")
    print(f"刷新 {updated} 条已有案例。")

    save_json(cases_file, all_cases)
    print(f"发布数据已保存到: {cases_file}")
    print(f"当前累计案例数: {len(all_cases)}")

    generate_case_pages(all_cases)
    generate_case_reports(all_cases)
    print("案例文档页与分析页已生成。")


if __name__ == "__main__":
    main()
