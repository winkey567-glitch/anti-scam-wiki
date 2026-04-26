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
ENABLE_AI_EXTRACTION = os.getenv("ENABLE_AI_EXTRACTION", "").strip().lower() in {"1", "true", "yes"}

if GENAI_AVAILABLE and GOOGLE_API_KEY and ENABLE_AI_EXTRACTION:
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
        "match": ["1688", "向日葵远程控制", "店铺信息未及时更新", "月收款额度已达上限"],
        "scam_type": "虚假购物 / 远程控制诈骗",
        "scenario": "假客服链接和远程操控",
        "target_group": ["电商经营者", "技术懵懂型"],
        "key_phrases": ["订单异常需要联系客服", "下载远程控制软件处理", "账户冻结需解除"],
        "red_flags": ["脱离平台到 QQ 或电话沟通", "要求下载远程控制软件", "链接跳转假客服页面"],
        "counter_measures": ["只在官方平台内处理订单异常", "绝不安装远程控制软件", "异常订单先联系平台官方客服"],
        "emergency_actions": ["立刻断网并卸载远控软件", "修改支付密码", "联系银行止付报警"],
        "psychological_trap": "利用商家急于成交和怕丢单心理",
    },
    {
        "match": ["裸聊", "露骨话题", "线下上门服务", "封口费"],
        "scam_type": "色情服务 / 裸聊敲诈诈骗",
        "scenario": "交友诱导和敲诈转账",
        "target_group": ["独居人群", "情感空虚人群"],
        "key_phrases": ["免费上门服务", "完成任务后安排见面", "不给钱就曝光"],
        "red_flags": ["陌生交友 App 主动露骨聊天", "以任务名义要求转账", "威胁曝光或失联"],
        "counter_measures": ["不安装陌生交友软件", "不参与任何色情服务交易", "遭遇威胁先报警不转账"],
        "emergency_actions": ["停止继续付款", "保存聊天截图", "尽快报警求助"],
        "psychological_trap": "利用好奇心、羞耻感和害怕曝光心理",
    },
    {
        "match": ["游戏装备", "和平精英", "游戏账号", "点卡", "限量皮肤"],
        "scam_type": "游戏交易诈骗",
        "scenario": "非官方游戏道具交易",
        "target_group": ["未成年人家庭", "游戏用户"],
        "key_phrases": ["免费送装备", "低价卖皮肤账号", "账户冻结需充值解冻"],
        "red_flags": ["脱离官方平台交易", "要求用家长手机操作", "以解冻保证金名义收费"],
        "counter_measures": ["只走官方交易渠道", "家长设备不交给孩子处理陌生活动", "拒绝任何先充值解冻要求"],
        "emergency_actions": ["解绑银行卡或止付", "保留聊天和支付记录", "及时报警"],
        "psychological_trap": "利用免费获得和低价捡漏心理",
    },
    {
        "match": ["领导", "熟人", "董事长", "合同保证金", "AI换脸", "拟声"],
        "scam_type": "冒充领导 / 熟人诈骗",
        "scenario": "熟人身份伪装转账",
        "target_group": ["财务人员", "重关系信任的人群"],
        "key_phrases": ["紧急转一笔款", "这是领导交代的", "不要走正常流程"],
        "red_flags": ["只发消息不接电话", "绕开审批流程", "突然要求大额转账"],
        "counter_measures": ["转账前电话或当面核实", "坚持审批流程", "涉及领导指令也先复核"],
        "emergency_actions": ["立刻联系收款行止付", "同步通知公司和警方", "保留聊天和转账证据"],
        "psychological_trap": "利用权威服从和熟人信任心理",
    },
    {
        "match": ["USDT", "安全钱包", "钱包地址", "交易所客服", "购买价值25万元"],
        "scam_type": "虚拟货币诈骗",
        "scenario": "虚拟币验资 / 保全转账",
        "target_group": ["投资人群", "技术懵懂型"],
        "key_phrases": ["购买 USDT 验资", "转到安全钱包保全资产", "配合调查升级认证"],
        "red_flags": ["要求购买虚拟币转指定地址", "把验资包装成安全流程", "以客服或公检法身份催促"],
        "counter_measures": ["任何验资保全都不通过虚拟币进行", "陌生钱包地址不转账", "先向平台官方核实"],
        "emergency_actions": ["停止继续购买转币", "保存钱包地址和聊天记录", "立即报警"],
        "psychological_trap": "利用技术门槛和资产焦虑心理",
    },
    {
        "match": ["助学金", "奖学金", "手续费", "激活费", "教育局"],
        "scam_type": "助学金诈骗",
        "scenario": "假冒教育补助发放",
        "target_group": ["学生家庭", "信息核验能力弱的人群"],
        "key_phrases": ["已获得助学金", "先缴手续费激活", "打到指定账户后发放"],
        "red_flags": ["发钱前先收费", "电话要求转账激活", "不通过学校官方渠道通知"],
        "counter_measures": ["只通过学校官方渠道办理", "国家奖助学金不会先收费", "先联系老师或学校核实"],
        "emergency_actions": ["停止转账", "保留电话和转账截图", "及时报警"],
        "psychological_trap": "利用对福利机会的期待和信息差",
    },
    {
        "match": ["军官", "寄送包裹", "关税", "网恋对象", "恋爱关系", "贴心男友"],
        "scam_type": "婚恋交友诈骗",
        "scenario": "情感关系诱导转账",
        "target_group": ["单身人群", "孤独空巢型"],
        "key_phrases": ["我对你是真心的", "包裹被扣需要交税", "先帮我周转一下"],
        "red_flags": ["短时间建立亲密关系", "很快开始谈钱", "以包裹、就医或困难为由索要转账"],
        "counter_measures": ["陌生关系涉及金钱一律先停", "先核实真实身份和现实关系", "与家人沟通后再决定"],
        "emergency_actions": ["停止继续付款", "保留聊天和账户信息", "及时报警"],
        "psychological_trap": "利用情感依赖和同情心理",
    },
    {
        "match": ["演唱会", "内部门票", "私下转账", "代购", "特殊服务"],
        "scam_type": "虚假购物服务诈骗",
        "scenario": "脱离平台私下交易",
        "target_group": ["网购人群", "热衷抢票和代购的人群"],
        "key_phrases": ["内部渠道更便宜", "私下转账省手续费", "下单后马上帮你处理"],
        "red_flags": ["要求脱离平台私聊", "承诺特殊渠道或内部票", "要求直接转到个人账户"],
        "counter_measures": ["交易只走官方平台", "不信低价内部渠道", "不为抢票代购私下转账"],
        "emergency_actions": ["停止继续支付", "保留聊天和订单信息", "联系平台和警方"],
        "psychological_trap": "利用稀缺感和捡漏心理",
    },
    {
        "match": ["航班", "改签", "航空公司客服", "机票", "退改签"],
        "scam_type": "机票退改签诈骗",
        "scenario": "假客服退改签 / 理赔",
        "target_group": ["出行人群", "技术懵懂型"],
        "key_phrases": ["航班取消需要改签", "马上办理赔付", "下载软件处理退改签"],
        "red_flags": ["陌生来电主动赔付", "要求下载会议或控制软件", "引导共享屏幕或转账验证"],
        "counter_measures": ["只通过航空公司官方渠道改签", "不下载陌生软件", "不提供验证码和银行卡信息"],
        "emergency_actions": ["立刻停止操作", "联系银行止付", "保存通话和订单信息报警"],
        "psychological_trap": "利用行程受影响的焦虑和急迫心理",
    },
    {
        "match": ["增加人气", "搭建账号", "无界趣连", "直播时"],
        "scam_type": "短视频代运营诈骗",
        "scenario": "账号运营 / 引流服务骗局",
        "target_group": ["小商户", "短视频用户"],
        "key_phrases": ["帮你涨粉引流", "付费搭建账号", "远程指导就能变现"],
        "red_flags": ["先收费后服务", "要求下载远程工具或陌生软件", "承诺快速涨粉变现"],
        "counter_measures": ["账号运营服务只走正规平台", "不轻信私信代运营承诺", "不安装远程控制软件"],
        "emergency_actions": ["停止转账", "保存聊天和软件信息", "修改账户密码并报警"],
        "psychological_trap": "利用急于获客和快速变现心理",
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

    title_overrides = [
        (["投资", "理财", "炒股", "证券"], "投资理财诈骗"),
        (["婚恋", "恋爱"], "婚恋交友诈骗"),
        (["机票", "退改签", "航班"], "机票退改签诈骗"),
    ]
    for keywords, scam_type in title_overrides:
        if any(keyword in title for keyword in keywords):
            for item in HEURISTICS:
                if item["scam_type"] == scam_type:
                    return item

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
