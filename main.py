import pandas as pd
import numpy as np
import datetime as dt
import argparse

from scripts.tokenizer import WordTokenizer
from scripts.wordcloud import WordCloudGenerator
from scripts.scrape import scrape_pubmed

if __name__ == '__main__':

    parser = argparse.ArgumentParser('main.py')
    parser.add_argument('-e', '--email', type=str, help='Email address for PubMed account')
    parser.add_argument('-q', '--query', type=str, default="bilingual*", help='Keyword for PubMed query; wildcards (*) recommended')
    parser.add_argument('-s', '--stopwords', type=str, nargs="+", help='Additional stopwords')

    args = parser.parse_args()

    tokenizer = WordTokenizer(lemmatize=False)
    scrape_pubmed(query = args.query, email = args.email)
    data = pd.read_csv("./data/all_titles.csv")

    data['decade'] = np.floor_divide(pd.DatetimeIndex(data['publication_date']).year, 10).astype(int) * 10
    data["tokens"] = tokenizer.transform(data["title"])

    make_wordcloud = WordCloudGenerator(stopwords=args.stopwords)

    for decade in list(data["decade"].unique()):
        make_wordcloud.generate_wordcloud(data["tokens"][data["decade"]==decade].tolist(), f"./output/{decade}s.png")

    print("Finished! Check your wordclouds in the output folder.")




