
####################
# Imports
####################

# Standard Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# External Libraries
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

path_to_font = "./www/BreeSerif-Regular.ttf"
mask = np.array(Image.open(r"./www/square.png"))

####################
# Word Cloud Generator
####################


class WordCloudGenerator:
    def __init__(self,
                 background_color='white',
                 color_func=lambda *args, **kwargs: "black",
                 font_path=path_to_font,
                 collocations=True,
                 stopwords=None,
                 prefer_horizontal=1,
                 mask=mask,
                 width=800,
                 height=800,
                 random_state=42,
                 max_words=75,
                 min_font_size=8,
                 max_font_size=None
                 ):
        """
        Initialize the word cloud generator with various parameters for customizing the generated word cloud.

        Parameters:
        - background_color (str): The color of the background of the generated word cloud.
        - color_func (function): The function used to color the words in the generated word cloud.
        - font_path (str): The file path to the font to be used in the generated word cloud.
        - collocations (bool): Whether to include collocations (two words frequently occurring together) in the generated word cloud.
        - prefer_horizontal (float): The preference for horizontal layout, where 0 is no preference, 1 is maximum preference, and -1 is minimum preference.
        - mask (numpy array or None): The mask image to use for the generated word cloud. If None, no mask will be used.
        - width (int): The width of the generated word cloud in pixels.
        - height (int): The height of the generated word cloud in pixels.
        - random_state (int): The random state used for generating the word cloud.
        - max_words (int): The maximum number of words to include in the word cloud.
        - min_font_size (int): The minimum font size for the words in the generated word cloud.
        - max_font_size (int or None): The maximum font size for the words in the generated word cloud. If None, the font size will be dynamically determined based on the frequencies of the words.
        """
        self.background_color = background_color
        self.color_func = color_func
        self.font_path = font_path
        self.collocations = collocations
        self.stopwords = stopwords
        self.prefer_horizontal = prefer_horizontal
        self.mask = mask
        self.width = width
        self.height = height
        self.random_state = random_state
        self.max_words = max_words
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size

    def generate_wordcloud(self,
                           tokens,
                           file_path):
        """
        Generate a wordcloud from a list of tokens and save it to the specified file path.

        Parameters:
        - tokens (list): A list of tokens to include in the wordcloud. Can be a flat list or a list of lists.
        - file_path (str): The file path where the generated wordcloud should be saved.
        """
        if not isinstance(tokens, list):
            raise ValueError("'tokens' must be a list.")

        if any(isinstance(i, list) for i in tokens):
            tokens = [item for sublist in tokens for item in sublist]
            print("Token list flattened.")

        print("Generating wordcloud...")
        wordcloud = WordCloud(background_color=self.background_color,
                              color_func=self.color_func,
                              font_path=self.font_path,
                              collocations=self.collocations,
                              prefer_horizontal=self.prefer_horizontal,
                              mask=self.mask,
                              width=self.width,
                              height=self.height,
                              random_state=self.random_state,
                              max_words=self.max_words,
                              min_font_size=self.min_font_size,
                              max_font_size=self.max_font_size
                              )
        wordcloud.generate(" ".join(tokens))
        wordcloud.to_file(file_path)
        print("Saving wordcloud to file...")
        print("Done.")

