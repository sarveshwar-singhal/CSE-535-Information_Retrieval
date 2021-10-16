'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self, token_count = 0):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.token_count = token_count

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        for t in tokenized_document:
            self.add_to_index(t, doc_id)

    def add_to_index(self, term_, doc_id_):
        # invt_index = self.inverted_index
        if self.inverted_index.get(term_):
            a = self.inverted_index[term_]
            if a.find_an_element(doc_id_):
                add = a.find_an_element(doc_id_)
                add.freq += 1
            else:
                a.insert_at_end(doc_id_)
        else:
            a = LinkedList()
            a.insert_at_end(doc_id_)
            self.inverted_index[term_] = a
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        # raise NotImplementedError

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        for i in self.inverted_index.keys():
            ll = self.inverted_index[i]
            ll.add_skip_connections()
        """ For each postings list in the index, add skip pointers.
            To be implemented."""

    def calculate_tf_idf(self, doc_count):
        for key in self.inverted_index.keys():
            val = self.inverted_index[key]
            val.idf = doc_count/val.length
            # print(self.inverted_index[key].idf)
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
