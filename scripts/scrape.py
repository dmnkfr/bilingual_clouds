from pymed import PubMed


# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="MyTool", email="dominik.freunberger@gmail.com")

# Create a GraphQL query in plain text
query = '("bilingual*"[All Fields]) AND (1980:2023[pdat])'

## PUT YOUR SEARCH TERM HERE ##

results = pubmed.query(query, max_results=10000)
articleList = []
articleInfo = []

for article in results:
# Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
# We need to convert it to dictionary with available function
    articleDict = article.toDict()
    articleList.append(articleDict)

# Generate list of dict records which will hold all article details that could be fetch from PUBMED API
for article in articleList:
#Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
    pubmedId = article['pubmed_id'].partition('\n')[0]
    # Append article info to dictionary 
    articleInfo.append({u'title':article['title'],
                       u'publication_date':article['publication_date']})

# Generate Pandas DataFrame from list of dictionaries
articlesPD = pd.DataFrame.from_dict(articleInfo)
#export_csv = df.to_csv (r'C:\Users\YourUsernam\Desktop\export_dataframe.csv', index = None, header=True) 

#Print first 10 rows of dataframe
print(articlesPD.head(10))