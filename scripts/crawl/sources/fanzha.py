"""Fetch anti-scam cases from public official articles."""

from __future__ import annotations

from datetime import datetime
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class FanZhaSpider:
    """Fetch public case lists and curated official case articles."""

    name = "官方公开反诈案例"
    base_url = "https://www.cac.gov.cn"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        ),
        "Referer": "https://www.cac.gov.cn/",
    }
    curated_sources = [
        {
            "url": "https://www.xinyuan.gov.cn/xinyuan/fangdxzp/202504/a209279cf4074fee9a6c65f1bbfce998.shtml",
            "source_name": "新源县人民政府",
            "source_reliability": "official",
            "parser": "xinyuan_latest_five",
        },
        {
            "url": "https://www.cac.gov.cn/2022-04/14/c_1651546285887220.htm",
            "source_name": "国家网信办",
            "source_reliability": "official",
            "parser": "cac_typical_cases",
        },
    ]

    def fetch_cases(self) -> list[dict]:
        """Fetch multiple structured raw cases from curated sources."""
        cases: list[dict] = []

        for source in self.curated_sources:
            try:
                response = requests.get(source["url"], headers=self.headers, timeout=30)
                response.raise_for_status()
                response.encoding = response.apparent_encoding or "utf-8"
            except requests.RequestException as exc:
                print(f"抓取来源失败: {source['url']} -> {exc}")
                continue

            parser = getattr(self, source["parser"], None)
            if parser is None:
                continue

            cases.extend(parser(response.text, source))

        return cases

    def xinyuan_latest_five(self, html: str, source: dict) -> list[dict]:
        """Parse the Xinyuan 'latest five cases' article."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"([一二三四五])、([^\n]+?)\n+案例\s*(.*?)诈骗手段解析\s*(.*?)(?=(?:[一二三四五]、)|反诈提醒)",
            flags=re.S,
        )

        cases = []
        for _, title, case_body, analysis in pattern.findall(text):
            cases.append(
                {
                    "title": title.strip(),
                    "content": (
                        f"案例经过：{self.clean_block(case_body)}\n\n"
                        f"诈骗手段解析：{self.clean_block(analysis)}"
                    ),
                    "source_url": source["url"],
                    "source_name": source["source_name"],
                    "source_reliability": source["source_reliability"],
                    "crawled_at": datetime.now().isoformat(),
                }
            )

        return cases

    def cac_typical_cases(self, html: str, source: dict) -> list[dict]:
        """Parse the CAC article with six typical APP scam cases."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"([一二三四五六])、(.*?)(?=(?:[一二三四五六]、)|国家网信办有关负责同志表示)",
            flags=re.S,
        )

        cases = []
        for _, block in pattern.findall(text):
            cleaned = self.clean_block(block)
            title = self.build_cac_title(cleaned)
            cases.append(
                {
                    "title": title,
                    "content": cleaned,
                    "source_url": source["url"],
                    "source_name": source["source_name"],
                    "source_reliability": source["source_reliability"],
                    "crawled_at": datetime.now().isoformat(),
                }
            )

        return cases

    def build_cac_title(self, content: str) -> str:
        """Generate a compact readable title from a CAC case paragraph."""
        if "仿冒APP" in content and "贷款" in content:
            return "仿冒贷款 APP 诈骗"
        if "返现" in content or "连单任务" in content:
            return "任务返现 / 刷单诈骗"
        if "电商客服" in content or "退款" in content:
            return "冒充电商客服退款诈骗"
        if "民警" in content or "安全账户" in content:
            return "冒充公检法安全账户诈骗"
        if "炒股广告" in content or "投资操作" in content:
            return "仿冒证券投资诈骗"
        if "校园贷" in content or "征信" in content:
            return "校园贷 / 征信修复诈骗"
        return content[:28]

    def extract_text(self, html: str) -> str:
        """Extract readable page text."""
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n", strip=True)
        return self.clean_block(text)

    def clean_block(self, text: str) -> str:
        """Normalize whitespace and digit line-break splits."""
        text = text.replace("\xa0", " ")
        text = re.sub(r"(?<=\d)\n(?=\d)", "", text)
        text = re.sub(r"\n{2,}", "\n", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.strip()

    def fetch_list(self, page: int = 1) -> list[dict]:
        """Fetch a generic case list page when available."""
        url = f"{self.base_url}/case/{page}"

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
        except requests.RequestException as exc:
            print(f"抓取列表失败: {exc}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".case-item") or soup.select(".list-item") or soup.select("article")

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
        """Fetch a single fallback detail page."""
        if not url:
            return None

        detail_url = urljoin(self.base_url, url)

        try:
            response = requests.get(detail_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
        except requests.RequestException as exc:
            print(f"抓取详情失败: {exc}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select_one("h1, .title, .article-title")
        content = soup.select_one(".content, .article-content, .detail, article")

        text_content = self.clean_block(content.get_text("\n", strip=True)) if content else ""
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
