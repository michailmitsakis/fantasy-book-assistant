import os
import pandas as pd
import minsearch

DATA_PATH = os.getenv("DATA_PATH", "../data/data.csv")

def load_index(data_path=DATA_PATH):

    df = pd.read_json("../data/data.json")
    documents = df.to_dict(orient="records")

    # Create and fit the index with enriched metadata fields
    index = minsearch.Index(
        text_fields=[
            'book_name',
            'author_name',
            'series_name',
            'subgenres',
            'themes',
            'summary',
            'publisher',
            'target_audience',
            'pacing',
            'tone',
            'writing_style',
            'setting_type',
            'technology_focus',
            'content_warnings'
        ],
        keyword_fields=[
            'id',
            'series_position',
            'page_count',
            'publication_year'
        ]
    )

    index.fit(documents)
    return index