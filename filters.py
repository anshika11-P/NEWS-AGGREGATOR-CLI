from datetime import date as Date


def filter_news(news, keyword=None, source=None, date=None):

    results = news

    if keyword:
        keyword = keyword.lower()

        results = [
            item for item in results
            if keyword in item["title"].lower()
            or keyword in item["description"].lower()
        ]

    if source:
        source = source.lower()

        results = [
            item for item in results
            if source in item["source"].lower()
        ]

    if date:
        try:
            Date.fromisoformat(date)
        except ValueError:
            print("Invalid date format!")
            return []

        results = [
            item for item in results
            if item["published"].startswith(date)
        ]

    return results