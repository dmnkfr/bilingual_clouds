####################
### Imports
####################
 
## Standard Libraries
import pandas as pd
from tqdm import tqdm
import string

## External Libraries
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

####################
### Tokenizer
####################

class WordTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, 
                 lowercase=True, 
                 remove_stopwords=True,
                 lemmatize=True):
        """
        A transformer for tokenizing and preprocessing text data. The following steps are performed:
        
        1. If 'clean_text' is True, text is cleaned using the 'clean_text' method.
        2. If 'lowercase' is True, all text is converted to lowercase.
        3. Text is tokenized into a list of words.
        4. If 'remove_stopwords' is True, stopwords are removed from the list of words.
        5. If 'remove_punctuation' is True, all non-alphabetic words are removed from the list of words.
        6. If 'lemmatize' is True, words are lemmatized using the appropriate lemmatizer for the specified language.
        
        Parameters
        ----------
        lowercase: bool, default=True
            Whether to convert all text to lowercase.
        remove_stopwords: bool, default=True
            Whether to remove stopwords from the list of words.
        lemmatize: bool, default=True
            Whether to lemmatize the words in the list.

        Attributes
        ----------
        stop_words: set
            Set of stopwords for the specified language.
        lemmatizer: WordNetLemmatizer
            A WordNet lemmatizer for English.
            
        Methods
        -------
        fit(self, X, y=None):
            Returns self.
        transform(self, X):
            Tokenizes and preprocesses text data.
        """
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, X, y=None):
        """
        """
        return self

    def transform(self, X):
        """
        """
        tokens = []
        with tqdm(total=len(X), desc='Tokenizing text') as pbar:
            for x in X:
                pbar.update(1)
                if type(x) == str:
                    if self.lowercase:
                        x = x.lower()
                    x = ''.join(c for c in x if c not in string.punctuation)
                    tokens.append(x.split())
                else:
                    tokens.append([])
        if self.remove_stopwords:
            tokens = [[t for t in x if t not in self.stop_words] for x in tokens if type(x) == list]
            print("Stopwords removed.")
        if self.lemmatize:
            tokens = [[self.lemmatizer.lemmatize(t) for t in x] for x in tokens if type(x) == list]
            print("Tokens lemmatized using the English lemmatizer.")

        print("Done.")
        return tokens

    def write_data(self, 
                   data, 
                   file_path):
        """
        
        """
        print("Writing data...")
        data.to_csv(file_path, index=False)
