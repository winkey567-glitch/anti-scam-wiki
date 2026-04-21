"""使用 Gemini 将原始案例内容整理成结构化字段。"""

from __future__ import annotations

import json
import os

try:
    import google.generativeai as genai

    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None
    print("警告: 未安装 google-generativeai，将使用本地兜底模板。")


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if GENAI_AVAILABLE and GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
else:
    model = None


EXTRACTION_PROMPT = """
请从下面这条“老年人诈骗案例”中提取结构化信息，并只返回 JSON。

案例标题：
{title}

案例内容：
{content}

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


def fallback_case_info(title: str, content: str) -> dict:
    """在未配置 API 或模型失败时返回基础结构。"""
    snippet = content[:100].strip()
    if snippet and len(content) > 100:
        snippet += "..."

    return {
        "title": title,
        "summary": snippet,
        "scam_type": "待分类",
        "scenario": "待识别",
        "target_group": ["待分析"],
        "key_phrases": [],
        "red_flags": [],
        "counter_measures": [],
        "emergency_actions": [],
        "psychological_trap": "待分析",
    }


def parse_json_response(text: str) -> dict:
    """兼容纯 JSON 和 ```json 包裹的返回。"""
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.split("```", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(cleaned)


def extract_case_info(title: str, content: str) -> dict:
    """提取案例结构化信息。"""
    if not GENAI_AVAILABLE or not GOOGLE_API_KEY or model is None:
        print("使用本地兜底模板生成结构化字段。")
        return fallback_case_info(title, content)

    prompt = EXTRACTION_PROMPT.format(title=title, content=content[:2000])

    try:
        response = model.generate_content(prompt)
        return parse_json_response(response.text)
    except json.JSONDecodeError:
        print("模型返回内容不是有效 JSON，已退回兜底模板。")
        result = fallback_case_info(title, content)
        result["raw_response"] = getattr(response, "text", "")
        result["scam_type"] = "解析失败"
        return result
    except Exception as exc:
        print(f"AI 提取失败: {exc}")
        result = fallback_case_info(title, content)
        result["scam_type"] = "提取失败"
        return result
