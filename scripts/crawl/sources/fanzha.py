"""国家反诈相关案例页面抓取器。"""

from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class FanZhaSpider:
    """抓取公开案例列表和详情。"""

    name = "国家反诈中心"
    base_url = "https://www.12321.cn"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        )
    }

    def fetch_list(self, page: int = 1) -> list[dict]:
        """获取案例列表。"""
        url = f"{self.base_url}/case/{page}"

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = "utf-8"
        except requests.RequestException as exc:
            print(f"抓取列表失败: {exc}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = (
            soup.select(".case-item")
            or soup.select(".list-item")
            or soup.select("article")
        )

        cases: list[dict] = []
        for item in items:
            title_elem = item.select_one(".title, h2, h3, a")
            date_elem = item.select_one(".date, .time, .meta")
            link_elem = item.select_one("a")

            if not title_elem or not link_elem:
                continue

            href = link_elem.get("href", "").strip()
            if not href:
                continue

            cases.append(
                {
                    "title": title_elem.get_text(strip=True),
                    "url": urljoin(self.base_url, href),
                    "date": date_elem.get_text(strip=True) if date_elem else "",
                    "source": self.name,
                }
            )

        return cases

    def fetch_detail(self, url: str) -> dict | None:
        """获取单条案例详情。"""
        if not url:
            return None

        detail_url = urljoin(self.base_url, url)

        try:
            response = requests.get(detail_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = "utf-8"
        except requests.RequestException as exc:
            print(f"抓取详情失败: {exc}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select_one("h1, .title, .article-title")
        content = soup.select_one(".content, .article-content, .detail, article")

        text_content = content.get_text("\n", strip=True) if content else ""
        if not text_content:
            return None

        return {
            "title": title.get_text(strip=True) if title else "",
            "content": text_content,
            "source_url": detail_url,
            "source_name": self.name,
            "source_reliability": "official",
            "crawled_at": datetime.now().isoformat(),
        }
