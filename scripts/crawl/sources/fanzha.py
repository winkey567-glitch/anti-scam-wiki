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
            "source_region": "新源县",
            "source_year": 2025,
            "source_reliability": "official",
            "parser": "xinyuan_latest_five",
        },
        {
            "url": "https://www.cac.gov.cn/2022-04/14/c_1651546285887220.htm",
            "source_name": "国家网信办",
            "source_region": "全国",
            "source_year": 2022,
            "source_reliability": "official",
            "parser": "cac_typical_cases",
        },
        {
            "url": "https://wjw.xinjiang.gov.cn/hfpc/djwlfz/202504/b70103aac65a4b59811bc0fd727418b5.shtml",
            "source_name": "新疆维吾尔自治区卫生健康委员会",
            "source_region": "商水县",
            "source_year": 2025,
            "source_reliability": "official",
            "parser": "seven_recent_cases",
        },
        {
            "url": "https://www.huarong.gov.cn/33159/37006/37008/37049/37355/content_2329542.html",
            "source_name": "华容县人民政府",
            "source_region": "华容县",
            "source_year": 2025,
            "source_reliability": "official",
            "parser": "top_ten_patterns",
        },
        {
            "url": "https://gaj.tl.gov.cn/tlsgaj/c00060/pc/content/content_1976830486581665792.html",
            "source_name": "铜陵市公安局",
            "source_region": "铜陵市",
            "source_year": 2025,
            "source_reliability": "official",
            "parser": "tongling_three_cases",
        },
        {
            "url": "https://gaj.cq.gov.cn/sy_245/bmdt/202507/t20250721_14831822.html",
            "source_name": "重庆市公安局",
            "source_region": "重庆市",
            "source_year": 2025,
            "source_reliability": "official",
            "parser": "cq_top_ten_cases",
        },
        {
            "url": "https://www.hh.gov.cn/info/26121/1190832.htm",
            "source_name": "红河州人民政府",
            "source_region": "红河州",
            "source_year": 2025,
            "source_reliability": "official",
            "parser": "honghe_top_ten_cases",
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

            try:
                cases.extend(parser(response.text, source))
            except Exception as exc:  # noqa: BLE001
                print(f"解析来源失败: {source['url']} -> {exc}")

        return cases

    def xinyuan_latest_five(self, html: str, source: dict) -> list[dict]:
        """Parse the Xinyuan 'latest five cases' article."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"([一二三四五])、([^\n]+?)\n+案例经过\s*(.*?)诈骗手段解析\s*(.*?)(?=(?:[一二三四五]、)|反诈提醒)",
            flags=re.S,
        )

        cases = []
        for _, title, case_body, analysis in pattern.findall(text):
            cases.append(
                self.make_case(
                    source,
                    title.strip(),
                    f"案例经过：{self.clean_block(case_body)}\n\n诈骗手段解析：{self.clean_block(analysis)}",
                )
            )
        return cases

    def cac_typical_cases(self, html: str, source: dict) -> list[dict]:
        """Parse the CAC article with several typical app scam cases."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"([一二三四五六])、(.*?)(?=(?:[一二三四五六]、)|国家网信办有关负责同志表示)",
            flags=re.S,
        )

        cases = []
        for _, block in pattern.findall(text):
            cleaned = self.clean_block(block)
            cases.append(self.make_case(source, self.build_cac_title(cleaned), cleaned))
        return cases

    def seven_recent_cases(self, html: str, source: dict) -> list[dict]:
        """Parse the Shangshui police seven-case article mirrored on Xinjiang site."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"案例([一二三四五六七])[:：]?\s*([^\n]+?)案例介绍\s*(.*?)(?=(?:案例[一二三四五六七])|商水公安温馨提示)",
            flags=re.S,
        )

        cases = []
        for _, title, content in pattern.findall(text):
            cases.append(self.make_case(source, title.strip(), self.clean_block(content)))
        return cases

    def top_ten_patterns(self, html: str, source: dict) -> list[dict]:
        """Parse the 2025 top ten scam patterns article with warning cases."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"([一二三四五六七八九十])、\s*(.*?)(?=(?:[一二三四五六七八九十]、)|全民反诈)",
            flags=re.S,
        )

        cases = []
        for _, block in pattern.findall(text):
            title = self.extract_top_ten_title(block)
            routine = self.extract_between(block, "核心套路：", "警示案例：")
            example = self.extract_between(block, "警示案例：", "防范提醒：")
            reminder = self.extract_between(block, "防范提醒：", "")
            if not title or not routine or not example:
                continue

            content = (
                f"核心套路：{self.clean_block(routine)}\n\n"
                f"警示案例：{self.clean_block(example)}\n\n"
                f"防范提醒：{self.clean_block(reminder)}"
            )
            cases.append(self.make_case(source, title, content))
        return cases

    def tongling_three_cases(self, html: str, source: dict) -> list[dict]:
        """Parse Tongling police three typical recent cases."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"案例([一二三])\s*(.*?)(?=(?:案例[一二三])|警方提醒)",
            flags=re.S,
        )

        cases = []
        for _, block in pattern.findall(text):
            content = self.clean_block(block)
            cases.append(self.make_case(source, self.build_tongling_title(content), content))
        return cases

    def cq_top_ten_cases(self, html: str, source: dict) -> list[dict]:
        """Parse Chongqing police ten high-frequency case types and examples."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"第?[一二三四五六七八九十]+类是(.*?)。(.*?)(?=(?:第?[一二三四五六七八九十]+类是)|当前，随着信息技术)",
            flags=re.S,
        )

        cases = []
        for title, block in pattern.findall(text):
            cleaned_title = title.strip()
            content = self.clean_block(block)
            if cleaned_title and content:
                cases.append(self.make_case(source, cleaned_title, content))
        return cases

    def honghe_top_ten_cases(self, html: str, source: dict) -> list[dict]:
        """Parse Honghe government's ten typical scam cases article."""
        text = self.extract_text(html)
        pattern = re.compile(
            r"([一二三四五六七八九十])、([^\n]+)\n(.*?)(?=(?:[一二三四五六七八九十]、)|$)",
            flags=re.S,
        )

        cases = []
        for _, title, block in pattern.findall(text):
            normalized_title = self.normalize_honghe_title(title.strip())
            content = self.clean_block(block)
            if normalized_title and content and len(content) >= 40:
                cases.append(self.make_case(source, normalized_title, content))
        return cases

    def make_case(self, source: dict, title: str, content: str) -> dict:
        return {
            "title": title,
            "content": content,
            "source_url": source["url"],
            "source_name": source["source_name"],
            "source_region": source.get("source_region", ""),
            "source_year": source.get("source_year"),
            "source_reliability": source["source_reliability"],
            "crawled_at": datetime.now().isoformat(),
        }

    def extract_top_ten_title(self, block: str) -> str:
        """Extract a clean title from a top-ten section block."""
        first_line = self.clean_block(block).split("\n", 1)[0]
        quoted = re.search(r"[“\"']([^”\"']+)[”\"']诈骗", first_line)
        if quoted:
            return f"{quoted.group(1).strip()}诈骗"

        plain = re.search(r"([\u4e00-\u9fa5A-Za-z/]+诈骗)", first_line)
        if plain:
            return plain.group(1).strip()
        return ""

    def build_tongling_title(self, content: str) -> str:
        """Generate a readable title for Tongling cases."""
        if "刷单" in content:
            return "刷单返利诈骗"
        if "股票投资" in content or "炒股软件" in content:
            return "伪造炒股软件诈骗"
        if "增加人气" in content or "搭建账号" in content or "无界趣连" in content:
            return "短视频代运营诈骗"
        return content[:24]

    def normalize_honghe_title(self, title: str) -> str:
        """Normalize Honghe section headings into stable site titles."""
        mapping = {
            "虚假服务类": "虚假服务诈骗",
            "虚假贷款类": "虚假网络贷款诈骗",
            "网络交友类": "婚恋交友诈骗",
            "冒充关闭微信百万保障类": "关闭微信百万保障诈骗",
            "冒充网络客服类": "冒充网络客服诈骗",
            "刷单返利类": "刷单返利诈骗",
            "虚假网络投资理财类": "虚假投资理财诈骗",
            "虚假购物类": "虚假购物诈骗",
            "冒充熟人类": "冒充熟人诈骗",
            "机票退改签类": "机票退改签诈骗",
        }
        return mapping.get(title, title)

    def extract_between(self, text: str, start: str, end: str) -> str:
        """Extract text between two markers."""
        if start not in text:
            return ""
        tail = text.split(start, 1)[1]
        if end and end in tail:
            tail = tail.split(end, 1)[0]
        return tail

    def build_cac_title(self, content: str) -> str:
        """Generate a compact readable title from a CAC case paragraph."""
        if "仿冒APP" in content and "贷款" in content:
            return "仿冒贷款 App 诈骗"
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
        title_elem = soup.select_one("h1, .title, .article-title")
        content_elem = soup.select_one(".article-content, .content, article, .TRS_Editor")
        if not title_elem or not content_elem:
            return None

        return {
            "title": title_elem.get_text(strip=True),
            "content": self.clean_block(content_elem.get_text("\n", strip=True)),
            "source_url": detail_url,
            "source_name": self.name,
            "source_region": "",
            "source_year": None,
            "source_reliability": "official",
            "crawled_at": datetime.now().isoformat(),
        }
