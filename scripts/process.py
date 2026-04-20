"""
数据处理主流程
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime

# 导入爬虫和AI模块
try:
    from crawl.sources.fanzha import FanZhaSpider
    from ai.extractor import extract_case_info
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from crawl.sources.fanzha import FanZhaSpider
    from ai.extractor import extract_case_info

# 数据目录
DATA_DIR = Path(__file__).parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
PUBLISHED_DIR = DATA_DIR / 'published'

def generate_id(content: str) -> str:
    """生成唯一ID"""
    return hashlib.md5(content.encode()).hexdigest()[:8]

def deduplicate(new_cases: list, existing_cases: list) -> list:
    """去重"""
    existing_ids = {c['id'] for c in existing_cases}
    return [c for c in new_cases if c['id'] not in existing_ids]

def process_case(raw_case: dict) -> dict:
    """处理单个案例"""
    # AI提取结构化信息
    extracted = extract_case_info(
        raw_case.get('title', ''),
        raw_case.get('content', '')
    )
    
    # 合并信息
    case = {
        'id': generate_id(raw_case.get('content', '')),
        'source_url': raw_case.get('source_url', ''),
        'source_name': raw_case.get('source_name', ''),
        'source_reliability': raw_case.get('source_reliability', 'community'),
        'crawled_at': raw_case.get('crawled_at', datetime.now().isoformat()),
        'processed_at': datetime.now().isoformat(),
        'status': 'pending_review',  # 待审核
        'content_lifecycle': 'new',
        **extracted
    }
    
    return case

def main():
    """主流程"""
    print("开始抓取数据...")
    
    # 1. 抓取数据
    spider = FanZhaSpider()
    list_items = spider.fetch_list(page=1)
    print(f"获取到 {len(list_items)} 条列表")
    
    raw_cases = []
    for item in list_items[:5]:  # 先抓5个测试
        print(f"抓取详情: {item['title'][:30]}...")
        detail = spider.fetch_detail(item['url'])
        if detail:
            raw_cases.append(detail)
    
    print(f"成功抓取 {len(raw_cases)} 条详情")
    
    # 保存原始数据
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_file = RAW_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(raw_cases, f, ensure_ascii=False, indent=2)
    print(f"原始数据保存到: {raw_file}")
    
    # 2. AI处理
    print("开始AI处理...")
    processed_cases = []
    for case in raw_cases:
        print(f"处理: {case['title'][:30]}...")
        processed = process_case(case)
        processed_cases.append(processed)
    
    # 3. 去重
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
    cases_file = PUBLISHED_DIR / 'cases.json'
    
    if cases_file.exists():
        with open(cases_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    else:
        existing = []
    
    new_cases = deduplicate(processed_cases, existing)
    print(f"新增 {len(new_cases)} 个案例（去重后）")
    
    # 4. 保存（待审核状态）
    all_cases = existing + new_cases
    with open(cases_file, 'w', encoding='utf-8') as f:
        json.dump(all_cases, f, ensure_ascii=False, indent=2)
    
    print(f"数据保存到: {cases_file}")
    print(f"总计 {len(all_cases)} 个案例")

if __name__ == '__main__':
    main()
