"""
使用Gemini API提取结构化信息
"""
import os
import json
from datetime import datetime

# 尝试导入google.generativeai，如果没有则给出提示
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("警告: google.generativeai未安装，将使用模拟模式")

# 配置API密钥
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
if GENAI_AVAILABLE and GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

EXTRACTION_PROMPT = """请从以下老年人诈骗案例中提取结构化信息，返回JSON格式：

案例标题：{title}
案例内容：{content}

请提取以下字段（中文）：
- title: 案例标题（场景化，如"我妈差点把验证码报给快递客服"）
- summary: 一句话摘要（50字以内）
- scam_type: 诈骗类型（如冒充客服、冒充公检法、保健品诈骗等）
- scenario: 具体场景（如快递退款、医保冻结、免费体检等）
- target_group: 目标人群标签列表（从以下选择：孤独空巢型、健康焦虑型、贪小便宜型、盲目投资型、认知衰退型、热衷社交型、技术懵懂型）
- key_phrases: 关键话术列表（骗子常用的话术）
- red_flags: 危险信号列表（识别要点）
- counter_measures: 防范措施列表
- emergency_actions: 紧急处理措施列表（如果已经受骗）
- psychological_trap: 利用的心理弱点（一句话）

只返回JSON，不要其他内容。"""

def extract_case_info(title: str, content: str) -> dict:
    """提取案例结构化信息"""
    
    # 如果没有API密钥或库未安装，返回模拟数据
    if not GENAI_AVAILABLE or not GOOGLE_API_KEY:
        print("模拟模式：返回结构化模板")
        return {
            "title": title,
            "summary": content[:50] + "..." if len(content) > 50 else content,
            "scam_type": "待分类",
            "scenario": "待识别",
            "target_group": ["待分析"],
            "key_phrases": [],
            "red_flags": [],
            "counter_measures": [],
            "emergency_actions": [],
            "psychological_trap": "待分析"
        }
    
    try:
        prompt = EXTRACTION_PROMPT.format(title=title, content=content[:2000])
        response = model.generate_content(prompt)
        
        # 解析JSON响应
        result = json.loads(response.text)
        return result
    except json.JSONDecodeError:
        # 如果返回的不是纯JSON，尝试提取
        text = response.text
        if '```json' in text:
            json_str = text.split('```json')[1].split('```')[0]
            return json.loads(json_str)
        # 如果还是失败，返回原始内容
        return {
            "title": title,
            "summary": content[:100] + "...",
            "scam_type": "解析失败",
            "raw_response": text
        }
    except Exception as e:
        print(f"AI提取失败: {e}")
        return {
            "title": title,
            "summary": content[:100] + "...",
            "scam_type": "提取失败"
        }
