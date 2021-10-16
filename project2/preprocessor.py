'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        # text_li = re.findall('[A-Z|a-z|0-9]*',text)
        # text = []
        # text = "this is the simplest. simplest simplest simplest He\'s the man I am the king!@#$%^&*()"
        # text = "种àa string withé fuünny charactersß."
        # for term in text_li:
        #     if len(term) > 0:
        #         text.append(term.lower())
        # text = " ".join(text)
        # print(text)
        # text = 'acb'
        text = text.encode("ascii", "replace")
        # print(text)
        text = text.decode()
        text = text.lower()
        if text[-1] == '\n':
            text=text[:-1]
        #stopword removal
        text = text.split(" ")
        text = [i for i in text if i not in self.stop_words]
        text = " ".join(text)

        #other char removal
        text_li = re.findall('[A-Z|a-z|0-9]*',text)
        pre_stem_text = []
        for term in text_li:
            if len(term) > 0:
                pre_stem_text.append(term.lower())
        stem_text = []
        ps = PorterStemmer()
        # stem_text = ps.stem(word=text)
        for i in range(len(pre_stem_text)):
            stem_text.append(ps.stem(pre_stem_text[i]))
        # print(text)
        # text = text.lower()
        # print(stem_text,end="") #remove
        # raise NotImplementedError
        return stem_text
