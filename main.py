import pandas as pd
import numpy as np
import datetime as dt
from scripts.tokenizer import WordTokenizer
from scripts.wordcloud import WordCloudGenerator

additional_stopwords = [
                        "bilingual",
                       "bilingualism",
                       "bilinguals",
                       #"bilingually",
                       #"monolingual",
                       "monolingualbilingual",
                       "language",
                       #"study"
                       ]

tokenizer = WordTokenizer(lemmatize=False)

def main():
    data = pd.read_csv("./data/all_titles.csv")

    data['decade'] = np.floor_divide(pd.DatetimeIndex(data['publication_date']).year, 10).astype(int) * 10

    data["tokens"] = tokenizer.transform(data["title"])

    make_wordcloud = WordCloudGenerator(stopwords=additional_stopwords)

    for decade in list(data["decade"].unique()):
        make_wordcloud.generate_wordcloud(data["tokens"][data["decade"]==decade].tolist(), f"./output/{decade}s.png")

if __name__ == '__main__':
    main()
