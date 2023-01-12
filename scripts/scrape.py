import pandas as pd
from pymed import PubMed

pubmed = PubMed(tool="MyTool", email=email)

query = '("bilingual*"[All Fields]) AND (1950:2023[pdat])'

results = pubmed.query(query, max_results=10000)
articles = []
article_info = []

for article in results:
    article_dict = article.toDict()
    articles.append(article_dict)

for article in articles:
    pubmedId = article['pubmed_id'].partition('\n')[0]
    article_info.append({u'title':article['title'],
                       u'publication_date':article['publication_date']})

pd.DataFrame.from_dict(article_info).to_csv ('./data/all_titles.csv') 
