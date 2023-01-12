import pandas as pd
from pymed import PubMed


# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="MyTool", email=mail)

# Create a GraphQL query in plain text
query = '("bilingual*"[All Fields]) AND (1980:2023[pdat])'

## PUT YOUR SEARCH TERM HERE ##

results = pubmed.query(query, max_results=10000)
articles = []
article_info = []

for article in results:
# Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
# We need to convert it to dictionary with available function
    article_dict = article.toDict()
    articles.append(article_dict)

# Generate list of dict records which will hold all article details that could be fetch from PUBMED API
for article in articles:
#Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
    pubmedId = article['pubmed_id'].partition('\n')[0]
    # Append article info to dictionary 
    article_info.append({u'title':article['title'],
                       u'publication_date':article['publication_date']})

# Generate Pandas DataFrame from list of dictionaries
pd.DataFrame.from_dict(article_info).to_csv ('./data/all_titles.csv') 
