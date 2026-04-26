"""Extract structured fields from raw case text."""

from __future__ import annotations

import json
import os

try:
    import google.generativeai as genai

    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if GENAI_AVAILABLE and GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
else:
    model = None


EXTRACTION_PROMPT = """
请从下面这条“老年人防诈骗案例”中提取结构化信息，并且只返回 JSON。
案例标题：{title}

案例内容：{content}

请输出这些字段：
- title: 更适合站点展示的中文标题
- summary: 100 字以内摘要
- scam_type: 诈骗类型
- scenario: 具体场景
- target_group: 目标人群标签数组
- key_phrases: 骗子常用话术数组
- red_flags: 识别信号数组
- counter_measures: 预防措施数组
- emergency_actions: 已受骗时的应急措施数组
- psychological_trap: 利用的心理弱点

要求：
1. 只输出 JSON，不要输出解释。
2. 如果原文信息不足，请尽量结合上下文合理概括。
3. 所有字段都使用中文。
""".strip()


HEURISTICS = [
    {
        "match": ["校园贷", "征信", "网贷平台", "消除记录"],
        "scam_type": "征信修复 / 校园贷诈骗",
        "scenario": "虚假征信消除",
        "target_group": ["技术懵懂型", "容易焦虑的人群"],
        "key_phrases": ["帮你消除记录", "否则影响征信", "需要先借款转到指定账户"],
        "red_flags": ["能准确说出个人信息", "以征信为由施压", "要求多平台借款后转账"],
        "counter_measures": ["征信问题只通过官方渠道处理", "不按电话指示借款转账", "先联系家人核实"],
        "emergency_actions": ["停止借款和转账", "联系贷款平台和银行", "保存通话证据报警"],
        "psychological_trap": "利用对征信影响的恐惧心理",
    },
    {
        "match": ["贷款", "额度高", "利息低", "银保监会账户", "申请贷款"],
        "scam_type": "贷款诈骗",
        "scenario": "仿冒贷款平台",
        "target_group": ["技术懵懂型", "急需资金的人群"],
        "key_phrases": ["额度高利息低", "先转账验证账户", "解冻后即可放款"],
        "red_flags": ["要求先转账再放款", "下载仿冒贷款 App", "转入所谓监管账户"],
        "counter_measures": ["正规贷款不会先收费", "贷款只走持牌平台", "不向陌生账户做验证转账"],
        "emergency_actions": ["立刻停止转账", "联系银行止付", "保存 App 和转账信息报警"],
        "psychological_trap": "利用资金焦虑和低息诱惑心理",
    },
    {
        "match": ["蛋仔派对", "腾讯会议", "游戏装备", "免费领取"],
        "scam_type": "免费送礼诈骗",
        "scenario": "免费礼品 / 游戏装备诱导",
        "target_group": ["贪小便宜型", "未成年人家庭"],
        "key_phrases": ["免费领取", "扫码就送", "再操作一步就能到账"],
        "red_flags": ["先送小礼品", "要求下载会议软件或陌生 App", "索要银行卡或验证码"],
        "counter_measures": ["不扫陌生码", "不为免费活动绑定支付信息", "涉及验证码立即停止"],
        "emergency_actions": ["解绑银行卡或止付", "卸载可疑软件", "保留页面和聊天记录"],
        "psychological_trap": "利用占便宜和从众心理",
    },
    {
        "match": ["客服", "退款", "扣费", "会员", "百万保险", "共享屏幕"],
        "scam_type": "冒充客服退款诈骗",
        "scenario": "平台扣费 / 退款取消",
        "target_group": ["技术懵懂型", "网购老人"],
        "key_phrases": ["不取消就会自动扣费", "需要下载软件处理", "需要共享屏幕或提供验证码"],
        "red_flags": ["主动来电处理退款", "要求下载陌生 App", "要求共享屏幕或验证码"],
        "counter_measures": ["只在官方 App 内处理退款", "不下载陌生软件", "验证码绝不外泄"],
        "emergency_actions": ["立刻停止操作", "联系银行止付", "保留聊天和转账证据"],
        "psychological_trap": "利用害怕扣费和急于退款的心理",
    },
    {
        "match": ["公安", "公检法", "民警", "立案", "安全账户", "银保监会账户"],
        "scam_type": "冒充公检法诈骗",
        "scenario": "虚假办案 / 安全账户转账",
        "target_group": ["认知衰退型", "容易紧张的老人"],
        "key_phrases": ["你涉嫌违法", "必须转到安全账户", "案件保密不能告诉家人"],
        "red_flags": ["电话办案", "要求保密", "要求转入安全账户"],
        "counter_measures": ["挂断后拨打 110 核实", "任何安全账户都是骗局", "先联系家人确认"],
        "emergency_actions": ["立刻止付", "保存转账记录", "马上报警"],
        "psychological_trap": "利用恐惧和权威压制判断力",
    },
    {
        "match": ["投资", "理财", "炒股", "证券", "收益", "提现失败", "保证金"],
        "scam_type": "投资理财诈骗",
        "scenario": "虚假投资平台",
        "target_group": ["盲目投资型", "有积蓄的老人"],
        "key_phrases": ["内幕消息", "稳赚高收益", "缴纳保证金后即可提现"],
        "red_flags": ["高收益低风险", "先小额盈利后诱导加码", "提现时不断加收费用"],
        "counter_measures": ["投资前核实平台资质", "高收益默认高风险", "大额投资先与家人确认"],
        "emergency_actions": ["停止继续投入", "保存平台和转账记录", "立即报警"],
        "psychological_trap": "利用快速获利和沉没成本心理",
    },
    {
        "match": ["刷单", "返利", "任务", "垫资", "返现", "连单"],
        "scam_type": "刷单返利诈骗",
        "scenario": "垫资返利陷阱",
        "target_group": ["贪小便宜型", "想做兼职补贴家用的人群"],
        "key_phrases": ["动动手指就能赚钱", "先垫资后返现", "再做一单就能提现"],
        "red_flags": ["先返小钱建立信任", "金额越来越大", "提现被卡住要求继续补钱"],
        "counter_measures": ["任何先垫资兼职都不参与", "不要继续补钱", "保留聊天和支付记录"],
        "emergency_actions": ["停止转账", "联系平台和银行", "尽快报警"],
        "psychological_trap": "利用小利诱惑和回本执念",
    },
    {
        "match": ["代买", "礼盒", "老师添加好友", "垫付", "转账截图"],
        "scam_type": "代买垫付诈骗",
        "scenario": "熟人身份引导代买",
        "target_group": ["热心助人型", "小商户"],
        "key_phrases": ["帮我先代买一下", "货到了马上给你结款", "已经转账给你了"],
        "red_flags": ["用熟人或老师身份接近", "要求先垫付", "转账截图无法核验"],
        "counter_measures": ["先核实对方身份", "不为陌生订单垫资", "收款到账前不发货不代买"],
        "emergency_actions": ["保留聊天和转账截图", "联系银行止付", "及时报警"],
        "psychological_trap": "利用助人和信任心理",
    },
]


def detect_heuristic(title: str, content: str) -> dict:
    """Return a rule-based fallback classification."""
    text = f"{title}\n{content}"
    for item in HEURISTICS:
        if any(keyword in text for keyword in item["match"]):
            return item

    return {
        "scam_type": "待分类",
        "scenario": "待识别",
        "target_group": ["待分析"],
        "key_phrases": [],
        "red_flags": [],
        "counter_measures": [],
        "emergency_actions": [],
        "psychological_trap": "待分析",
    }


def fallback_case_info(title: str, content: str) -> dict:
    """Return a useful local fallback when no model is available."""
    snippet = content[:100].strip()
    if snippet and len(content) > 100:
        snippet += "..."

    heuristic = detect_heuristic(title, content)

    return {
        "title": title,
        "summary": snippet,
        "scam_type": heuristic["scam_type"],
        "scenario": heuristic["scenario"],
        "target_group": heuristic["target_group"],
        "key_phrases": heuristic["key_phrases"],
        "red_flags": heuristic["red_flags"],
        "counter_measures": heuristic["counter_measures"],
        "emergency_actions": heuristic["emergency_actions"],
        "psychological_trap": heuristic["psychological_trap"],
    }


def parse_json_response(text: str) -> dict:
    """Accept either pure JSON or fenced JSON."""
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.split("```", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(cleaned)


def extract_case_info(title: str, content: str) -> dict:
    """Extract structured case information."""
    if not GENAI_AVAILABLE or not GOOGLE_API_KEY or model is None:
        return fallback_case_info(title, content)

    prompt = EXTRACTION_PROMPT.format(title=title, content=content[:2000])

    try:
        response = model.generate_content(prompt)
        return parse_json_response(response.text)
    except json.JSONDecodeError:
        result = fallback_case_info(title, content)
        result["raw_response"] = getattr(response, "text", "")
        result["scam_type"] = "解析失败"
        return result
    except Exception:
        result = fallback_case_info(title, content)
        result["scam_type"] = result["scam_type"] or "提取失败"
        return result
