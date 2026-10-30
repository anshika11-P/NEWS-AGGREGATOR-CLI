import requests
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime


RSS_FEEDS = {
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "BBC Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "BBC Business": "https://feeds.bbci.co.uk/news/business/rss.xml"
}


def fetch_news():

    all_news = []

    for source, url in RSS_FEEDS.items():

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            root = ET.fromstring(response.content)

            for item in root.findall(".//item"):

                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()

                description = item.findtext(
                    "description", ""
                ).strip()

                pub_date = item.findtext("pubDate", "").strip()

                if not title or not link:
                    continue

                try:
                    published = parsedate_to_datetime(
                        pub_date
                    ).isoformat()
                except (ValueError, TypeError, OverflowError):
                    published = pub_date

                all_news.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "source": source,
                    "published": published
                })

            print("Fetched:", source)

        except requests.RequestException as error:
            print("Error:", error)

        except ET.ParseError:
            print("RSS data could not be read.")

    unique_news = {}

    for article in all_news:
        unique_news[article["link"]] = article

    return list(unique_news.values())