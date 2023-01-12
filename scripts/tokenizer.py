####################
### Imports
####################
 
## Standard Libraries
import pandas as pd
from tqdm import tqdm

## External Libraries
import re
import emoji
import contractions
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
import spacy
import spellchecker


####################
### Tokenizer
####################

class WordTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, 
                 lowercase=True, 
                 remove_stopwords=True,
                 lemmatize=True,
                 clean_text=True,
                 language='english'):
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
        clean_text: bool, default=True
            Whether to clean the text using the 'clean_text' method.
        remove_punctuation: bool, default=True
            Whether to remove non-alphabetic words from the list of words.
        language: str, default='english'
            The language to use for lemmatization and stopword removal. Currently supported languages are 'english' and 'swedish'.
            
        Attributes
        ----------
        stop_words: set
            Set of stopwords for the specified language.
        lemmatizer: WordNetLemmatizer
            A WordNet lemmatizer for English.
        nlp: spacy language model
            A spaCy language model for Swedish.
            
        Methods
        -------
        fit(self, X, y=None):
            Returns self.
        transform(self, X):
            Tokenizes and preprocesses text data.
        clean_text(self, data, fix_emojis=True, fix_contractions=True, remove_strange_fonts=True, remove_punct=True, replace_numbers=True):
            Cleans text data.
        """
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.clean = clean_text
        self.lemmatize = lemmatize
        self.language = language
        self.stop_words = set(stopwords.words(self.language))
        self.lemmatizer = WordNetLemmatizer()
        self.nlp = spacy.load(f'./models/sv_core_news_sm')

    def fit(self, X, y=None):
        """
        """
        return self

    def transform(self, X):
        """
        """
        if self.clean:
            X = self.clean_text(X)
        tokens = []
        with tqdm(total=len(X), desc='Tokenizing text') as pbar:
            for x in X:
                pbar.update(1)
                if type(x) == str:
                    if self.lowercase:
                        x = x.lower()
                    tokens.append(x.split())
                else:
                    tokens.append(x)
        if self.remove_stopwords:
            tokens = [[t for t in x if t not in self.stop_words] for x in tokens if type(x) == list]
            print("Stopwords removed.")
        if self.lemmatize:
            if self.language == 'english':
                tokens = [[self.lemmatizer.lemmatize(t) for t in x] for x in tokens if type(x) == list]
                print("Tokens lemmatized using the English lemmatizer.")
            if self.language == 'swedish':
                tokens = [[self.nlp(t)[0].lemma_ for t in x] for x in tokens if type(x) == list]
                print("Tokens lemmatized using the Swedish lemmatizer.")
        print("Done.")
        return tokens


    def clean_text(self,
                   X,
                   fix_emojis=True,
                   fix_contractions=True,
                   remove_strange_fonts=False,
                   remove_punct=True,
                   replace_numbers=True
                   ):
        """
        Cleans text data.

        Args:
            X (list): List of strings to be cleaned.
            fix_emojis (bool): If True, emojis are replaced by words.
            fix_contractions (bool): If True, contractions are expanded.
            remove_strange_fonts (bool): If True, non-Latin fonts are removed.
            remove_punct (bool): If True, all non-alphanumeric characters are removed.
            replace_numbers (bool): If True, digits are replaced by the word "number".
        
        Returns:
            list: List of cleaned strings.
        """
        print("Cleaning text...")
        # translate emojis
        if fix_emojis:
            X = [emoji.demojize(x) if type(x) == str else x for x in X]
    
        # fix contractions
        if fix_contractions:
            X = [contractions.fix(x) if type(x) == str else x for x in X]

        # remove strange fonts
        if remove_strange_fonts:
            X = [re.sub(r'[^\x00-\x7f]', r'', x) if type(x) == str else x for x in X]
        
        # remove punctuation
        if remove_punct:
            X = [re.sub(r'[^\w\s]','',x) if type(x) == str else x for x in X]
        
        # replace numbers with "number"
        if replace_numbers:
            X = [re.sub(r"\d+", "number",x) if type(x) == str else x for x in X]
    
        # replace underscores with space (for emojis)
        X = [x.replace('_', ' ') if type(x) == str else x for x in X]
        
        # strip leading and trailing spaces
        X = [x.strip() if type(x) == str else x for x in X]
        print("Text cleaned.")
        return X

    def correct_spelling(self, 
                        X):
        """
        """
        print("Correcting spelling...")
        
        spell = spellchecker.SpellChecker()

        X = [[spell.correction(x) for x in sublist] for sublist in X]
        X = [i for i in X if i is not None]
        X = [list(filter(lambda x: x is not None, sublist)) for sublist in X]
        print("Spelling corrected.")
        return X

    def write_data(self, 
                   data, 
                   file_path):
        """
        
        """
        print("Writing data...")
        data.to_csv(file_path, index=False)
