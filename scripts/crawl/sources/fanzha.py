"""
国家反诈中心爬虫
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class FanZhaSpider:
    name = "国家反诈中心"
    base_url = "https://www.12321.cn"
    
    def fetch_list(self, page=1):
        """获取案例列表"""
        url = f"{self.base_url}/case/{page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            cases = []
            # 根据实际页面结构调整选择器
            items = soup.select('.case-item') or soup.select('.list-item') or soup.select('article')
            
            for item in items:
                title_elem = item.select_one('.title, h2, h3, a')
                date_elem = item.select_one('.date, .time, .meta')
                link_elem = item.select_one('a')
                
                if title_elem and link_elem:
                    cases.append({
                        'title': title_elem.text.strip(),
                        'url': link_elem.get('href', ''),
                        'date': date_elem.text.strip() if date_elem else '',
                        'source': self.name
                    })
            return cases
        except Exception as e:
            print(f"抓取失败: {e}")
            return []
    
    def fetch_detail(self, url):
        """获取案例详情"""
        if not url.startswith('http'):
            url = self.base_url + url
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 提取内容
            title = soup.select_one('h1, .title, .article-title')
            content = soup.select_one('.content, .article-content, .detail, article')
            
            return {
                'title': title.text.strip() if title else '',
                'content': content.text.strip() if content else '',
                'source_url': url,
                'source_name': self.name,
                'source_reliability': 'official',
                'crawled_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"详情抓取失败: {e}")
            return None
