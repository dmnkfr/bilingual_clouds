import pandas as pd
from pymed import PubMed

def scrape_pubmed(query: str,
                  email: str):
    
    pubmed = PubMed(tool="WordCloudTrends", email=email)
    
    query_string = f'("{query}"[All Fields]) AND (1950:2023[pdat])'

    print("Scraping PubMed...")
    results = pubmed.query(query_string, max_results=9998)
    articles = []
    article_info = []

    for article in results:
        article_dict = article.toDict()
        articles.append(article_dict)
    print("Tidying data...")
    for article in articles:
        pubmedId = article['pubmed_id'].partition('\n')[0]
        article_info.append({u'title':article['title'],
                        u'publication_date':article['publication_date']})
    
    pd.DataFrame.from_dict(article_info).to_csv ('./data/all_titles.csv') 
    print("Done.")