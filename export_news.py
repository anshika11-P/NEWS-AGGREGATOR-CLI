import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def export_news(news, file_type):

    if not news:
        raise ValueError("No news available!")

    dataframe = pd.DataFrame(news)

    if file_type == "csv":

        filename = BASE_DIR / "news_export.csv"

        dataframe.to_csv(
            filename,
            index=False,
            encoding="utf-8-sig"
        )

    elif file_type in ["excel", "xlsx"]:

        filename = BASE_DIR / "news_export.xlsx"

        dataframe.to_excel(filename, index=False)

    else:
        raise ValueError("Choose csv or excel.")

    return filename.name